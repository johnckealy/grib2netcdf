import pygrib
from os import path
from first import first
import re
import netCDF4 as nc4
import os
import string
import random
from django.conf import settings
from first import first

TMP_DIR = os.getenv('TMP_LOCATION')
SAMPLE_FILE = os.path.join(settings.BASE_DIR, '../GribFile')






class GribField:
    def __init__(self, id, grb):
        self.gribfield_obj = grb
        self.name = grb.name
        self.shortName = grb.shortName
        self.paramId = grb.paramId
        self.units = self.get_units(grb.units)
        self.raw_units = grb.units
        self.id = "gribid-{}-{}-{}".format(grb.level, grb.paramId, grb.typeOfLevel)
        self.typeOfLevel = grb.typeOfLevel
        self.level = "{}".format(grb.level)
        if self.level == "0 unknown" or self.level == "1 unknown":
            self.level = "-"
        # print(grb.parameterNumber)

    def get_units(self, units):
        units = re.sub("kg\*\*-1", "kg<sup>-1</sup>", units)
        units = re.sub("s\*\*-1", "s<sup>-1</sup>", units)
        units = re.sub("s\*\*-2", "s<sup>-2</sup>", units)
        units = re.sub("m\*\*-1", "m<sup>-1</sup>", units)
        units = re.sub("m\*\*-2", "m<sup>-2</sup>", units)
        units = re.sub("m\*\*2", "m<sup>2</sup>", units)
        return units

    def get_data(self):
        return self.gribfield_obj.data()[0]

    def get_latlons(self):
        return self.gribfield_obj.latlons()

    def get_timestamps(self):
        return self.gribfield_obj.analDate, self.gribfield_obj.validDate


class Grib:
    def __init__(self, filepath):
        self.filepath = filepath
        self.filename = self.get_filename(filepath)
        self.grbs_obj = pygrib.open(filepath)
        self.validDate = first(self.grbs_obj).validDate
        self.strvalidDate = self.validDate.strftime("%Y-%m-%d %H:%M:%S")
        self.forecastTime = first(self.grbs_obj).forecastTime
        self.all = []
        self.parse_grib(self.grbs_obj)

    def parse_grib(self, grbs):
        id = 1
        for grb in grbs:
            gribfield = GribField(id, grb)
            self.all.append(gribfield)
            id += 1

    def get_filename(self, filepath):
        return path.basename(filepath)

    def find(self, id):
        for gribfield in self.all:
            if id == gribfield.id:
                return gribfield






class NetCDF:

    def __init__(self, post_object):
        self.post_object = post_object
        self.grbs_obj = self.read_grib()
        self.lons = first(self.grbs_obj.all).get_latlons()[1]
        self.lats = first(self.grbs_obj.all).get_latlons()[0]
        self.analDate = first(self.grbs_obj.all).get_timestamps()[0]
        self.validDate = first(self.grbs_obj.all).get_timestamps()[1]
        self.create_netcdf()

    def _id_generator(self, size=9, chars=string.ascii_uppercase + string.digits):
        return ''.join(random.choice(chars) for _ in range(size))

    def read_grib(self):
        if self.post_object['sample'] == 'True':
            return Grib(SAMPLE_FILE)
        else:
            print('generated id ############################   ', self._id_generator())
            return Grib(TMP_DIR + 'destination.grb')

    def create_netcdf(self):
        f = nc4.Dataset(TMP_DIR + 'output.nc', 'w', format='NETCDF4')
        f.createDimension('x', len(self.lons[0,:]))
        f.createDimension('y', len(self.lons[:,0]))

        # time stamps
        anal_date = f.createVariable("analysis_date", 'f4', ('y', 'x'))
        anal_date[:,:] = self.analDate.timestamp()
        anal_date.units = "seconds since 1970-1-1"
        anal_date.long_form = self.analDate.strftime("%Y-%m-%d %H:%M:%S UTC")
        valid_date = f.createVariable("valid_time", 'f4', ('y', 'x'))
        valid_date[:,:] = self.validDate.timestamp()
        valid_date.units = "seconds since 1970-1-1"
        valid_date.long_form = self.validDate.strftime("%Y-%m-%d %H:%M:%S UTC")

        # lat and lon
        lons = f.createVariable("longitude", 'f4', ('y', 'x'))
        lons[:,:] = self.lons
        lons.long_name = "Longitude"
        lons.units = "degrees longitude"
        lats = f.createVariable("latitude", 'f4', ('y', 'x'))
        lats[:,:] = self.lats
        lats.long_name = "Latitude"
        lats.units = "degrees latitude"

        # data fields
        counter_id = 0
        for id in self.post_object:
            if "gribid" in id:
                gribfield = self.grbs_obj.find(id)
                field_data = gribfield.get_data()
                field_var = f.createVariable("{}_{}".format(gribfield.shortName, counter_id), 'f4', ('y', 'x'))
                field_var.long_name = gribfield.name
                field_var.level = gribfield.level
                field_var.type_of_level = gribfield.typeOfLevel
                field_var.units = gribfield.raw_units
                field_var[:,:] = field_data
                counter_id += 1

        f.description = "Created by grib2netcdf.com"
        f.close()
