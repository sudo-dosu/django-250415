from rest_framework.urlpatterns import format_suffix_patterns
from django.urls import path
from .views import *

app_name = 'api'

urlpatterns = [
    # path('example/', example, name='example'),
]
urlpatterns = format_suffix_patterns(urlpatterns)
