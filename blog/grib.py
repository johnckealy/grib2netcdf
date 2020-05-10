import pygrib
from os import path
from first import first
import re

class GribField:
    def __init__(self, id, grb):
        self.name = grb.name
        self.units = self.get_units(grb.units)
        self.typeOfLevel = grb.typeOfLevel
        self.level = "{} {}".format(grb.level, grb.unitsOfFirstFixedSurface)
        if self.level == "0 unknown" or self.level == "1 unknown":
            self.level = "-"
        self.id = id

    def get_units(self, units):
        units = re.sub("kg\*\*-1", "kg<sup>-1</sup>", units)
        units = re.sub("s\*\*-1", "s<sup>-1</sup>", units)
        units = re.sub("s\*\*-2", "s<sup>-2</sup>", units)
        units = re.sub("m\*\*-1", "m<sup>-1</sup>", units)
        units = re.sub("m\*\*-2", "m<sup>-2</sup>", units)
        units = re.sub("m\*\*2", "m<sup>2</sup>", units)
        return units

class Grib:
    def __init__(self, filepath):
        self.filepath = filepath
        self.filename = self.get_filename(filepath)
        grbs = pygrib.open(filepath)
        self.validDate = first(grbs).validDate
        self.forecastTime = first(grbs).forecastTime
        self.all = []
        self.parse_grib(grbs)

    def parse_grib(self, grbs):
        id = 1
        for grb in grbs:
            gribfield = GribField(id, grb)
            self.all.append(gribfield)
            id += 1

    def get_filename(self, filepath):
        return path.basename(filepath)
