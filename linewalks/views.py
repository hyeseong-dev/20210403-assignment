import re
import json
from math                   import ceil

from django.http            import JsonResponse
from django.views           import View
from django.db.models       import Q
from django.db              import IntegrityError


from decorator              import query_debugger
from linewalks.models       import (
    Person,
    VisitOccurrence,
    ConditionOccurrence,
    Concept,
    Death,
    DrugExposure

)


class PatientView(View):
    """
    성, 인종, 민족 환자수를 분류하여 해당 카테고리의 환자 수를 제공함은 물론 전체 환자 수와 사망자 수에 대한 정보 역시 제공하는 API
    """
    @query_debugger
    def get(self, request):
        queryset = Person.objects.all().\
            values('gender_concept_id','race_source_value', 'ethnicity_source_value')
        
        results = {
            '전체 환자 수'   : '{:,}'.format(queryset.count() )+'명', 
            '성별 환자 수'   :  {
                '남성' : '{:,}'.format(queryset.filter(gender_concept_id=8507).count())+'명',
                '여성' : '{:,}'.format(queryset.filter(gender_concept_id=8532).count())+'명',
            },
            '인종별 환자 수' : {
                '아시아인' : '{:,}'.format(queryset.filter(race_source_value='asian').count())+'명', 
                '흑인'     : '{:,}'.format(queryset.filter(race_source_value='black').count())+'명',
                '백인'     : '{:,}'.format(queryset.filter(race_source_value='white').count())+'명',
            },
            '민족별 환자 수' : {
                '히스패닉'   : '{:,}'.format(queryset.filter(ethnicity_source_value='hispanic').count())+'명',
                '비히스패닉' : '{:,}'.format(queryset.filter(ethnicity_source_value='nonhispanic').count())+'명',
            },
            '사망 환자 수'   : '{:,}'.format(Death.objects.count())+'명'
        }
        if results:
            return JsonResponse({'결과':results}, status=200)
        return JsonResponse({'message':'INVALID_REQUEST'}, status=400)


class VisitView(View):
    """
    방문 유형(입원/외래/응급), 성, 인종, 민족, 연령대로 분류하여 방문자수 정보를 제공하는 API
    """
    @query_debugger
    def get(self, request):
        queryset = VisitOccurrence.objects.select_related('person')
        
        results = {
            '방문유형'   :  {
                '입원' : '{:,}'.format(queryset.filter(visit_concept_id=9201).count())+'명',
                '외래' : '{:,}'.format(queryset.filter(visit_concept_id=9202).count())+'명',
                '응급' : '{:,}'.format(queryset.filter(visit_concept_id=9203).count())+'명',
            },
            '성별 방문 수'   :  {
                '남성' : '{:,}'.format(queryset.filter(person__gender_concept_id=8507).count())+'명',
                '여성' : '{:,}'.format(queryset.filter(person__gender_concept_id=8532).count())+'명',
            },
            '인종별 방문 수' : {
                '히스패닉'   : '{:,}'.format(queryset.filter(person__ethnicity_source_value='hispanic').count())+'명',
                '비히스패닉' : '{:,}'.format(queryset.filter(person__ethnicity_source_value='nonhispanic').count())+'명',
            },
            '연령대별 방문 수'   : {
                f'{idx*10}~{idx*10+9}' : '{:,}'\
                .format(queryset.filter(person__year_of_birth__range=(key-9, key)).count())+'명'                                                               
                for idx,key in enumerate(list(range(2011,1921,-10)),1)
            }
        }
        if results:
            return JsonResponse({'결과':results}, status=200)
        return JsonResponse({'message':'INVALID_REQUEST'}, status=400)


class ConceptListView(View):
    '''
    concept_id의 정보를 얻을 수 있는 API입니다.
    - 쿼리 파라미터를 이용 
        + 검색 기능   
        + 키워드 검색   
    '''
    @query_debugger
    def get(self,request):
        page = int(request.GET.get('page', 1))

        PAGE_SIZE = 50
        limit  = page * PAGE_SIZE  
        offset = limit - PAGE_SIZE 
        
        concepts   = Concept.objects.values('concept_id', 'concept_name')
        people     = Person.objects.values('gender_concept_id','ethnicity_source_value')
        drugs      = DrugExposure.objects.values('drug_concept_id')
        conditions = ConditionOccurrence.objects.values('condition_concept_id')

        results = {}

        results['persons'] = [{
            'gender_concept_id'      : p['gender_concept_id'],
            'ethnicity_source_value' : p['ethnicity_source_value'],
        }for p in people[offset:limit]]

        results['concepts'] = [{
            'concept_id'    : c['concept_id'],
            'concept_name'  : c['concept_name'],
        }for c in concepts[offset:limit]]
        
        results['conditions'] = [{
            'condition_concept_id'    : c['condition_concept_id'],
        }for c in conditions[offset:limit]]

        results['drugs'] = [{
            'drug_concept_id'    : d['drug_concept_id'],
        }for d in drugs[offset:limit]]
        
        
        if results:
            return JsonResponse({
                "페이지" : f'{page} / {ceil(concepts.count()/PAGE_SIZE)}',
                '총 조회 건수': {
                    'people'     :'{:,}'.format(people.count())+' 건',
                    'concepts'   :'{:,}'.format(concepts.count())+' 건',
                    'drugs'      :'{:,}'.format(drugs.count())+' 건',
                    'conditions' :'{:,}'.format(conditions.count())+' 건',
                },
                '결과':results,
                }, status=200)
        return JsonResponse({'message':'INVALID_REQUEST'}, status=400)


class SearchView(View):
    """
    각 테이블의 row를 조회하는 API를 구현합니다.
        - concept id와 concept name 매칭
            + concept의 의미를 알 수 있게 이름을 함께 return합니다.
        - Pagination 기능
        - 특정 컬럼 검색 기능
            + 키워드 검색
    """
    @query_debugger
    def get(self, request):

        page = int(request.GET.get('page', 1))
        PAGE_SIZE = 50
        limit  = page * PAGE_SIZE
        offset = limit - PAGE_SIZE
        
        results = {}
        people =  Person.objects.filter(
                Q(person_id              = request.GET.get('person_id'))|
                Q(gender_concept_id      = request.GET.get('gender_concept_id'))|
                Q(race_concept_id        = request.GET.get('race_concept_id'))|
                Q(ethnicity_source_value = request.GET.get('ethnicity_source_value'))|
                Q(birth_datetime         = request.GET.get('birth_datetime'))
            )
        visit_occurrences = VisitOccurrence.objects.filter(
                Q(person_id            = request.GET.get('person_id'))|
                Q(visit_occurrence_id  = request.GET.get('visit_occurrence_id'))|
                Q(visit_concept_id     = request.GET.get('visit_concept_id'))|
                Q(visit_start_datetime = request.GET.get('visit_start_datetime'))|
                Q(visit_end_datetime   = request.GET.get('visit_end_datetime'))
            )

        condition_occurrences= ConditionOccurrence.objects.filter(
                Q(person_id                = request.GET.get('person_id'))|
                Q(condition_occurrence_id  = request.GET.get('condition_occurrence_id'))|
                Q(condition_concept_id     = request.GET.get('condition_concept_id'))|
                Q(condition_start_datetime = request.GET.get('condition_start_datetime'))|
                Q(condition_end_datetime   = request.GET.get('condition_end_datetime'))
            )
        drug_exposures = DrugExposure.objects.filter(
                Q(person_id                    = request.GET.get('person_id'))|
                Q(drug_concept_id              = request.GET.get('drug_concept_id'))|
                Q(visit_occurrence_id          = request.GET.get('visit_occurrence_id'))|
                Q(drug_exposure_start_datetime = request.GET.get('drug_exposure_start_datetime'))|
                Q(drug_exposure_end_datetime   = request.GET.get('drug_exposure_end_datetime'))
            )[offset:limit] 

        results['people'] = [{   
            'person_id'             : p.person_id,
            'gender_concept_id'     : p.gender_concept_id,
            'birth_datetime'        : p.birth_datetime,
            'race_concept_id'       : p.race_concept_id ,
            'ethnicity_concept_id'  : p.ethnicity_concept_id,
            }for p in people[offset:limit] ]


        results['visit_occurrences'] = [{
            'person_id'             : v.person_id,   
            'visit_occurrence_id'   : v.visit_occurrence_id,
            'visit_concept_id'      : v.visit_concept_id,
            'visit_start_datetime'  : v.visit_start_datetime,
            'visit_end_datetime'    : v.visit_end_datetime,
            }for v in visit_occurrences[offset:limit] ]

        results['condition_occurrences'] = [{
            'person_id'                : c.person_id,  
            'condition_concept_id'     : c. condition_concept_id,
            'condition_start_datetime' : c. condition_start_datetime,
            'condition_end_datetime'   : c. condition_end_datetime,
            'visit_occurrence_id'      : c. visit_occurrence_id,
            }for c in condition_occurrences[offset:limit] ]

        results['drug_exposures'] = [{   
            'person_id'                    : d.person_id,      
            'drug_concept_id'              : d.drug_concept_id,
            'drug_exposure_start_datetime' : d.drug_exposure_start_datetime,
            'drug_exposure_end_datetime'   : d.drug_exposure_end_datetime,
            'visit_occurrence_id'          : d.visit_occurrence_id,
            }for d in drug_exposures[offset:limit] ]
                
        pcnt = people.count()
        vcnt = visit_occurrences.count()
        dcnt = drug_exposures.count()
        ccnt  = condition_occurrences.count()
        max_page = max(pcnt, vcnt, dcnt,ccnt)

        if results:
            return JsonResponse({
            'message':'SUCCESS',
            "페이지" : f'{page} / {ceil(max_page/PAGE_SIZE)}',
            '조회 건수': {
                'people'     :'{:,}'.format(pcnt)+' 건',
                'concepts'   :'{:,}'.format(vcnt)+' 건',
                'drugs'      :'{:,}'.format(dcnt)+' 건',
                'conditions' :'{:,}'.format(cnt)+' 건',
            },
            '결과':results}, status=200)
        return JsonResponse({'message':'INVALID_REQUEST'}, status=400)
                        