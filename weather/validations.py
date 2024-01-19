
import re
from datetime import datetime


def register_user_validator(data):
    user_registration_error = 'User registration failed.'


    if not data.get("username"):
        return False, f"{user_registration_error} Username field is required and it Cannot be Null.", data

    if not isinstance(data.get("username"), str):
        return False, f"{user_registration_error} Username field must be string.", data

    if data.get("username").isalpha() == False:
        return False, f"{user_registration_error} Username field should only contain alphabets.", data

    if len(data.get("username")) > 250 or len(data.get("username")) < 1:
        return False, f"{user_registration_error} Length of Username should be between 1 to 250.", data
    
    if not data.get("password"):
        return False, f"{user_registration_error} Password field is required and it Cannot be Null.", data

    if not isinstance(data.get("password"), str):
        return False, f"{user_registration_error} Password field must be string.", data

    if len(data.get("password")) > 20 or len(data.get("password")) < 8:
        return False, f"{user_registration_error} Length of Password should be between 8 to 20.", data
    

    if data.get("password"):
        pattern = re.compile(r'^(?=.*[!@#$%^&*()_+{}\[\]:;<>,.?~\\/\-])(?=.*[A-Z])(?=.*[0-9])(?=.*[a-z]).{8,}$')
        if not pattern.match(data.get("password")):
            return False, f'''{user_registration_error} Username must contain one special symbols('!@#$%^&*_+\\:;<>,.?~-'),one integer,one capital letter.''', data
        
    if not data.get("confirm_password"):
        return False, f"{user_registration_error} Password field is required and it Cannot be Null.", data

    if data.get("password") != data.get("confirm_password"):
        return False, f"{user_registration_error} Confirm password does't match with password.", data
   
    return True, "Validation successful.", data



def user_authenticate_validator(data):
    user_authentication_error = 'User authentication failed.'

    if not data.get("username"):
        return False, f"{user_authentication_error} Username field is required and it Cannot be Null.", data

    if not isinstance(data.get("username"), str):
        return False, f"{user_authentication_error} Username field must be string.", data

    if data.get("username").isalpha() == False:
        return False, f"{user_authentication_error} Username field should only contain alphabets.", data

    if len(data.get("username")) > 250 or len(data.get("username")) < 1:
        return False, f"{user_authentication_error} Enter correct username.", data
    
    if not data.get("password"):
        return False, f"{user_authentication_error} Password field is required and it Cannot be Null.", data

    if not isinstance(data.get("password"), str):
        return False, f"{user_authentication_error} Password field must be string.", data

    if len(data.get("password")) > 20 or len(data.get("password")) < 8:
        return False, f"{user_authentication_error} Enter correct Password.", data    
   
    return True, "Validation successful.", data

def param_validator(data):
    weather_error = 'Weather report is not available for input data.'

    if not data.get("latitude"):
        return False, f"{weather_error} Please enter latitude in integer or float.", data
    
    if not data.get("longitude"):
        return False, f"{weather_error} Please enter longitude in integer or float.", data

    if not isinstance(data.get("latitude"), (float, int)):
        return False, f"{weather_error} Latitude must be a float or an integer.", data

    if not isinstance(data.get("longitude"), (float, int)):
        return False, f"{weather_error} Longitude must be a float or an integer.", data
    
    if not (-90 <= data.get("latitude") <= 90) or not (-180 <= data.get("longitude") <= 180):
        return False, f"{weather_error} Invalid latitude or longitude. Latitude must be between -90 and 90, and longitude between -180 and 180.", data
    
    if not data.get("start_date"):
        return False, f"{weather_error} Please enter date in YYYY-MM-DD format.", data
    
    if not data.get("end_date"):
        return False, f"{weather_error} Please enter date in YYYY-MM-DD format.", data

    date_format = "%Y-%m-%d"

    try:
        print(data.get("start_date"),data.get("end_date"))
        start_date = datetime.strptime(data.get("start_date"), date_format)
        end_date = datetime.strptime(data.get("end_date"), date_format)

    except Exception as e:
        return False, f"{weather_error} Invalid date format. Please use YYYY-MM-DD. {e}", data

    if start_date >= end_date:
        return False, f"{weather_error} Please enter end date greater than start date.", data
    
    if start_date.date() > datetime.now().date() or end_date.date()>=datetime.now().date():
        return False, f"{weather_error} Please enter end date or start date less than todays date.", data
   
    return True, "Validation successful.", data
