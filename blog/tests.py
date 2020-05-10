from django.test import TestCase
from .grib import Grib, GribField
from django.conf import settings
import os
from first import first

class GribModelTests(TestCase):

    def setUp(self):
        self.grib = Grib(os.path.join(settings.BASE_DIR, '../GribFile'))


    def test_get_filename(self):
        self.assertEqual(self.grib.filename, "GribFile")


    def test_get_units(self):
        units = self.grib.all[1].get_units("kg**-1")
        self.assertEqual(units, "kg<sup>-1</sup>")

        units = self.grib.all[1].get_units("s**-1kgkg**-1")
        self.assertEqual(units, "s<sup>-1</sup>kgkg<sup>-1</sup>")
