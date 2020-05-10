from django.urls import path
from . import views

app_name = 'blog'
urlpatterns = [
    path('', views.upload_file, name='upload'),
    path('grib', views.grib_stats, name='grib'),
    path('netcdf', views.create_netcdf, name='netcdf'),
]
