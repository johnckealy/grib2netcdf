from django.shortcuts import render, redirect#, get_object_or_404
from django.http import HttpResponseRedirect, FileResponse
from django.core.files.storage import FileSystemStorage
from .forms import  UploadFileForm
from .grib import Grib, NetCDF, TMP_DIR, SAMPLE_FILE
import os
from django.conf import settings


def about(request):
    return render(request, 'blog/about.html')


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


def netcdf(request):
    if request.method == 'POST':
        NetCDF(request.POST)
    return render(request, 'blog/netcdf.html')


def serve_netcdf_file(request):
    fs = FileSystemStorage(TMP_DIR)
    response = FileResponse(fs.open('output.nc', 'rb'))
    return response
