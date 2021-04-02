from django.db import models


class Concept(models.Model):
    concept_id       = models.IntegerField(primary_key=True)
    concept_name     = models.CharField(max_length=255, blank=True, null=True)
    domain_id        = models.CharField(max_length=20, blank=True, null=True)
    vocabulary_id    = models.CharField(max_length=20, blank=True, null=True)
    concept_class_id = models.CharField(max_length=20, blank=True, null=True)
    standard_concept = models.CharField(max_length=1, blank=True, null=True)
    concept_code     = models.CharField(max_length=50, blank=True, null=True)
    valid_start_date = models.DateField(blank=True, null=True)
    valid_end_date   = models.DateField(blank=True, null=True)
    invalid_reason   = models.CharField(max_length=1, blank=True, null=True)

    class Meta:
        db_table = 'concept'


class ConditionOccurrence(models.Model):
    person                        = models.ForeignKey('linewalks.Person', on_delete=models.CASCADE, blank=True, null=True, related_name='condition_occurrence')
    visit_occurrence              = models.ForeignKey('linewalks.VisitOccurrence', on_delete=models.CASCADE, blank=True, null=True,related_name='condition_occurrence')
    condition_occurrence_id       = models.BigIntegerField(primary_key=True)
    condition_concept_id          = models.IntegerField(blank=True, null=True)
    condition_start_date          = models.DateField(blank=True, null=True)
    condition_start_datetime      = models.DateTimeField(blank=True, null=True)
    condition_end_date            = models.DateField(blank=True, null=True)
    condition_end_datetime        = models.DateTimeField(blank=True, null=True)
    condition_type_concept_id     = models.IntegerField(blank=True, null=True)
    condition_status_concept_id   = models.IntegerField(blank=True, null=True)
    stop_reason                   = models.CharField(max_length=20, blank=True, null=True)
    provider_id                   = models.BigIntegerField(blank=True, null=True)
    visit_detail_id               = models.BigIntegerField(blank=True, null=True)
    condition_source_value        = models.CharField(max_length=50, blank=True, null=True)
    condition_source_concept_id   = models.IntegerField(blank=True, null=True)
    condition_status_source_value = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        db_table = 'condition_occurrence'


class Death(models.Model):
    person                  = models.ForeignKey('linewalks.Person', on_delete=models.CASCADE, blank=True, null=True,related_name='death')
    death_date              = models.DateField(blank=True, null=True)
    death_datetime          = models.DateTimeField(blank=True, null=True)
    death_type_concept_id   = models.IntegerField(blank=True, null=True)
    cause_concept_id        = models.BigIntegerField(blank=True, null=True)
    cause_source_value      = models.IntegerField(blank=True, null=True)
    cause_source_concept_id = models.BigIntegerField(blank=True, null=True)

    class Meta:
        db_table = 'death'


class DrugExposure(models.Model):
    person                       = models.ForeignKey('linewalks.Person', on_delete=models.CASCADE, blank=True, null=True,related_name='drug_exposure')
    visit_occurrence             = models.ForeignKey('linewalks.VisitOccurrence', on_delete=models.CASCADE, blank=True, null=True,related_name='drug_exposure')
    drug_exposure_id             = models.BigIntegerField(primary_key=True)
    drug_concept_id              = models.IntegerField(blank=True, null=True)
    drug_exposure_start_date     = models.DateField(blank=True, null=True)
    drug_exposure_start_datetime = models.DateTimeField(blank=True, null=True)
    drug_exposure_end_date       = models.DateField(blank=True, null=True)
    drug_exposure_end_datetime   = models.DateTimeField(blank=True, null=True)
    verbatim_end_date            = models.DateField(blank=True, null=True)
    drug_type_concept_id         = models.IntegerField(blank=True, null=True)
    stop_reason                  = models.CharField(max_length=20, blank=True, null=True)
    refills                      = models.IntegerField(blank=True, null=True)
    quantity                     = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    days_supply                  = models.IntegerField(blank=True, null=True)
    sig                          = models.TextField(blank=True, null=True)
    route_concept_id             = models.IntegerField(blank=True, null=True)
    lot_number                   = models.CharField(max_length=50, blank=True, null=True)
    provider_id                  = models.BigIntegerField(blank=True, null=True)
    visit_detail_id              = models.BigIntegerField(blank=True, null=True)
    drug_source_value            = models.CharField(max_length=50, blank=True, null=True)
    drug_source_concept_id       = models.IntegerField(blank=True, null=True)
    route_source_value           = models.CharField(max_length=50, blank=True, null=True)
    dose_unit_source_value       = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        db_table = 'drug_exposure'


class Person(models.Model): 
    person_id                   = models.BigIntegerField(primary_key=True,)
    gender_concept_id           = models.IntegerField(blank=True, null=True)
    year_of_birth               = models.IntegerField(blank=True, null=True)
    month_of_birth              = models.IntegerField(blank=True, null=True)
    day_of_birth                = models.IntegerField(blank=True, null=True)
    birth_datetime              = models.DateTimeField(blank=True, null=True)
    race_concept_id             = models.IntegerField(blank=True, null=True)
    ethnicity_concept_id        = models.IntegerField(blank=True, null=True)
    location_id                 = models.BigIntegerField(blank=True, null=True)
    provider_id                 = models.BigIntegerField(blank=True, null=True)
    care_site_id                = models.BigIntegerField(blank=True, null=True)
    person_source_value         = models.CharField(max_length=50, blank=True, null=True)
    gender_source_value         = models.CharField(max_length=50, blank=True, null=True)
    gender_source_concept_id    = models.IntegerField(blank=True, null=True)
    race_source_value           = models.CharField(max_length=50, blank=True, null=True)
    race_source_concept_id      = models.IntegerField(blank=True, null=True)
    ethnicity_source_value      = models.CharField(max_length=50, blank=True, null=True)
    ethnicity_source_concept_id = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = 'person'


class VisitOccurrence(models.Model):
    person                        = models.ForeignKey('linewalks.Person', on_delete=models.CASCADE, blank=True, null=True, related_name='visit_occurrence')
    visit_occurrence_id           = models.BigIntegerField(primary_key=True,)
    visit_concept_id              = models.IntegerField(blank=True, null=True)
    visit_start_date              = models.DateField(blank=True, null=True)
    visit_start_datetime          = models.DateTimeField(blank=True, null=True)
    visit_end_date                = models.DateField(blank=True, null=True)
    visit_end_datetime            = models.DateTimeField(blank=True, null=True)
    visit_type_concept_id         = models.IntegerField(blank=True, null=True)
    provider_id                   = models.BigIntegerField(blank=True, null=True)
    care_site_id                  = models.BigIntegerField(blank=True, null=True)
    visit_source_value            = models.CharField(max_length=50, blank=True, null=True)
    visit_source_concept_id       = models.IntegerField(blank=True, null=True)
    admitted_from_concept_id      = models.IntegerField(blank=True, null=True)
    admitted_from_source_value    = models.CharField(max_length=50, blank=True, null=True)
    discharge_to_source_value     = models.CharField(max_length=50, blank=True, null=True)
    discharge_to_concept_id       = models.IntegerField(blank=True, null=True)
    preceding_visit_occurrence_id = models.BigIntegerField(blank=True, null=True)

    class Meta:
        db_table = 'visit_occurrence'
