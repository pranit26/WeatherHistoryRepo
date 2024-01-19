from django.urls import path
from weather.views import registerUser,userAuthentication,protected_view,getHourlyData

urlpatterns = [
    path('register_user/', registerUser, name='registerUser'),
    path('authenticate_user/',userAuthentication, name='authenticateUser'),
    path('protected_view/',protected_view, name='protectedView'),
    path('get_hourly_data/',getHourlyData, name='getHourlyData')
]