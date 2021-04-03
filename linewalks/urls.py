from django.contrib import admin
from django.urls    import path

from linewalks      import views
from linewalks      import models

urlpatterns = [
        path('static/patients/', views.PatientView.as_view()),
        path('static/visitors/',   views.VisitView.as_view())  ,
        path('concept/',        views.ConceptListView.as_view()), # queryParameter
        path('search/',        views.SearchView.as_view())  ,
]
