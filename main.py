import time
from emailverification import loginToGmail, std_login, edit_mail, verify_email, read_otp, quitdriver, \
    email_id_verification, ifalreadyverfied, outcomeform
from getstudentData import admin_login, get_unverified_Emails, next_page, studentData
from utilty import read_json, update_json
import logging

logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)

userdata = read_json('userData.json')

# login as admin and get all student data with unverifed emails
a: bool = True
admin_login(userdata['pmgDishauser'], userdata['pmgDishapswd'])
while a:
    get_unverified_Emails()
    a = next_page()

studentData: dict = read_json('studentData.json')
mailJson: dict = read_json('email.json')
mail: list = list(read_json('email.json').keys())
loginToGmail(userdata['gmail_user_name'], userdata['gmail_password'])
processed: dict = {}
i = 0
for name in studentData.keys():
    usedmail = 'email already used'
    try:
        std_login(studentData[name][0], studentData[name][1])
        while usedmail == 'email already used':
            if i == len(mail):
                raise ValueError('Email Exhausted')
            usedmail = edit_mail(mail[i])
            if usedmail == 'email already used':
                i += 1
        if usedmail == mail[i]:
            i += 1

        processed[usedmail] = [name, "pending"]
        verify_email(read_otp(name))
        if email_id_verification() is False:
            raise ValueError(f"verification failed for {name} and {mail[i]}")
        processed[usedmail] = [name, "completed"]
        print(f'veified for student {name} and {mail[i]} has been utilised')
        time.sleep(1)
        quitdriver()
    except ValueError as error:
        time.sleep(2)
        quitdriver()
        if str(error) == 'Email Exhausted':
            raise Exception('Email Exausted , Please add more unused emails')
    except Exception as exc:
        time.sleep(2)
        logger.exception(exc)
        quitdriver()

update_json('processed.json', processed)