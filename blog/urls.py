from django.urls import path
from . import views

app_name = 'blog'
urlpatterns = [
    path('', views.upload_file, name='upload'),
    path('sample_grib', views.sample_grib, name='sample_grib'),
    path('grib', views.grib, name='grib'),
    path('netcdf', views.create_netcdf, name='netcdf'),
]
