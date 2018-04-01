from django.test import TestCase
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.firefox.webdriver import WebDriver
from django.test import TestCase, Client


# Create your tests here.

class ViewReportPage(StaticLiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.selenium = WebDriver()
        cls.selenium.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def test_access_the_website(self):
        self.selenium.get('%s%s' % (self.live_server_url, '/reports/'))


class BasicTest(TestCase):

    def test_response(self):
        response = self.client.get('/reports/')
        self.assertEqual(response.status_code, 200)

    def test_response_detail(self):
        response = self.client.get('/reports/E00246/')
        self.assertIn('E00246', response)



