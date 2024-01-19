from django.test import SimpleTestCase
from django.urls import reverse,resolve
from weather.views import registerUser,userAuthentication,protected_view,getHourlyData

class TestUrls(SimpleTestCase):

    def test_registerUser_urls_resolves(self):
        url =reverse('registerUser')
        self.assertEqual(resolve(url).func,registerUser)

    def test_userAuthentication_urls_resolves(self):
        url =reverse('authenticateUser')
        self.assertEqual(resolve(url).func,userAuthentication)
        
    def test_protectedView_urls_resolves(self):
        url =reverse('protectedView')
        self.assertEqual(resolve(url).func,protected_view)   

    def test_list_getHourlyData_resolves(self):
        url =reverse('getHourlyData')
        self.assertEqual(resolve(url).func,getHourlyData)    
