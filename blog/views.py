from django.shortcuts import render, redirect#, get_object_or_404
from django.http import HttpResponseRedirect
from .forms import  UploadFileForm
from .grib import Grib
import os
from django.conf import settings


def handle_input_file(f):
    filepath = os.getenv('TMP_LOCATION') + 'destination.grb'
    with open(filepath, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    return Grib(filepath)


def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                grbs = handle_input_file(request.FILES['file'])
                return render(request, 'blog/grib_stats.html', {'grbs': grbs})
            except:
                return render(request, 'blog/grib_stats.html', {'grbserror': "There was a problem with your file. Are you sure it's in GRIB2 format?"})
        else:
            return render(request, 'blog/grib_stats.html', {'grbserror': "There was a problem validating your file."})

    else:
        form = UploadFileForm()
    return render(request, 'blog/index.html', {'form': form})


def grib_stats(request):
    sample_grb = Grib(os.path.join(settings.BASE_DIR, '../GribFile'))
    return render(request, 'blog/grib_stats.html', {'grbs': sample_grb})


def create_netcdf(request):
    if request.method == 'POST':
        return render(request, 'blog/netcdf_success.html', {'posted': request.POST})
