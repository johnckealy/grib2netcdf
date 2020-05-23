from django.test import TestCase
from django.test import LiveServerTestCase
from .grib import Grib, GribField
from django.conf import settings
import os
from first import first

from selenium import webdriver
from selenium.webdriver.common.keys import Keys


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





class AccountTestCase(LiveServerTestCase):

    def setUp(self):
        self.selenium = webdriver.Firefox(executable_path='/home/jokea/code/johnckealy/django/geckodriver')
        super(AccountTestCase, self).setUp()

    def tearDown(self):
        self.selenium.quit()
        super(AccountTestCase, self).tearDown()

    # def test_upload(self):
    #     selenium = self.selenium
    #     selenium.get('http://127.0.0.1:8000')
    #     # username = selenium.find_element_by_id('id_username')
    #     # password = selenium.find_element_by_id('id_password')
    #     # uploadElement = selenium.find_element_by_xpath("//input[@type='text' and class='form-control']")
    #     uploadElement = selenium.find_element_by_class_name("buttonText")
    #     uploadElement.send_keys("/home/jokea/code/johnckealy/django/grib2netcdf/GribFile");
    #
    #     selenium.page_source
    #     assert 'User Authenicated' in selenium.page_source
