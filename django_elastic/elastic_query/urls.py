from django.urls import path
from elastic_query import views


urlpatterns = [
    path("", views.QueryCompute)
]
