from django.shortcuts import render, redirect#, get_object_or_404
from django.http import HttpResponseRedirect, FileResponse
from django.core.files.storage import FileSystemStorage
from .forms import  UploadFileForm
from .grib import Grib, NetCDF
import os
from django.conf import settings



TMP_DIR = os.getenv('TMP_LOCATION')
SAMPLE_FILE = os.path.join(settings.BASE_DIR, '../GribFile')

def handle_input_file(f):
    with open(TMP_DIR+'destination.grb', 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            handle_input_file(request.FILES['file'])
            return redirect('/grib')
        else:
            return render(request, 'blog/grib_stats.html', {'grbserror': "There was a problem validating your file."})
    else:
        form = UploadFileForm()
    return render(request, 'blog/index.html', {'form': form})


def grib(request):
    try:
        grbs = Grib(TMP_DIR+'destination.grb')
        return render(request, 'blog/grib_stats.html', {'grbs': grbs, 'sample': False})
    except:
        return render(request, 'blog/grib_stats.html', {'grbserror': "There was a problem with your file. Are you sure it's in GRIB2 format?"})


def sample_grib(request):
    sample_grbs = Grib(SAMPLE_FILE)
    return render(request, 'blog/grib_stats.html', {'grbs': sample_grbs, 'sample': True})


def create_netcdf(request):
    if request.method == 'POST':
        NetCDF(request.POST)

    redirect('/download_netcdf')    

    render(request, 'blog/netcdf_success.html', {'netcdf_filepath': netcdf_filepath})
