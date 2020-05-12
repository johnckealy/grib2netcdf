from django.urls import path
from . import views

app_name = 'blog'
urlpatterns = [
    path('', views.upload_file, name='upload'),
    path('about', views.about, name='about'),
    path('sample_grib', views.sample_grib, name='sample_grib'),
    path('grib', views.grib, name='grib'),
    path('netcdf', views.netcdf, name='netcdf'),
    path('serve_netcdf_file', views.serve_netcdf_file, name='serve_netcdf_file')
]
