import time

from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement

from getstudentData import driver as driver1

from utilty import create_driver_Session, eleID, eleXpath, read_json, if_present, if_present_id

# launch another session for email verification

driver2: WebDriver


# login to gmail
def loginToGmail(username, password):
    driver1.get('https://mail.google.com/mail/u/0/#inbox')
    eleID('identifierId', driver1).send_keys(username)
    eleID('identifierNext', driver1).click()
    eleXpath('//input[@name="password"]', driver1).send_keys(password)
    eleID('passwordNext', driver1).click()
    eleXpath('//*[@href="https://mail.google.com/mail/u/0/#inbox"]', driver1)
    time.sleep(1)


# read otp
def read_otp(name):
    eleXpath('//input[@aria-label="Search mail"]', driver1).clear()
    eleXpath('//input[@aria-label="Search mail"]', driver1).send_keys(name)
    time.sleep(4)
    eleXpath('//button[@aria-label="Search mail"]', driver1).click()
    time.sleep(1)
    i = 1
    while if_present("(//*[starts-with(text(),'Verification Hi')])", driver1) is False:
        if i > 10:
            break
        time.sleep(i)
        i += 1
        eleXpath('//button[@aria-label="Search mail"]', driver1).click()

    full_text: str = eleXpath("(//*[starts-with(text(),'Verification Hi')])", driver1).text
    delete_mail()
    full_text_split = full_text.replace('.', '').split()
    for text in full_text_split:
        if text.isdigit():
            return text


def delete_mail():
    action = ActionChains(driver1)
    action.move_to_element(eleXpath("(//*[starts-with(text(),'Verification Hi')])", driver1)).perform()
    try:
        a = len(driver1.find_elements_by_xpath('(//*[@data-tooltip="Delete"])'))
        eleXpath(f'(//*[@data-tooltip="Delete"])[{a}]', driver1).click()
    except Exception as exc:
        eleXpath(f'(//*[@data-tooltip="Delete"])[{a}]', driver1).click()


# login as student
def std_login(username, password):
    global driver2
    driver2 = create_driver_Session()
    driver2.get('https://www.pmgdisha.in/app/login')
    eleID('inputEmail', driver2).send_keys(username)
    eleID('lgpass1', driver2).send_keys(password)
    eleXpath('//*[@value="Login"]', driver2).click()
    while True:
        if if_present("//*[contains(text(),'Please enter correct password.')]", driver2):
            eleID('inputEmail', driver2).send_keys(username)
            eleID('lgpass1', driver2).send_keys('Icebrst@1')
            eleXpath('//*[@value="Login"]', driver2).click()
            break
        if if_present("//*[contains(text(),'Your password has expired.')]", driver2):
            eleID('password0', driver2).send_keys(password)
            eleID('newPassword', driver2).send_keys('Icebrst@1')
            eleID('confirmPassword', driver2).send_keys('Icebrst@1')
            eleXpath('//*[@type="submit"]', driver2).click()
            eleID('inputEmail', driver2).send_keys(username)
            eleID('lgpass1', driver2).send_keys('Icebrst@1')
            eleXpath('//*[@value="Login"]', driver2).click()
            break
        if if_present(f"//*[contains(text(),'{username}')]", driver2):
            break;
    # click agree button need try catch
    eleXpath(f"//*[contains(text(),'{username}')]", driver2)
    try:
        eleID('agreeButton', driver2, 3).click()
        time.sleep(1)
    except:
        pass

    try:
        eleXpath("//*[contains(text(),'OK')]", driver2).click()
        time.sleep(1)
    except:
        pass
    # click ok button need try catch


# edit email
def edit_mail(mail):
    email: str = eleID('emailId', driver2).get_attribute('value')
    if email.replace('.', '') == 'atsbetulpmgdisha@gmailcom':
        eleID('verifyOTP', driver2).click()
        time.sleep(1)
        eleID('resendOTP', driver2).click()
        return email
    try:
        eleID('edit-fields', driver2).click()
    except:
        pass
    eleID('emailId', driver2).clear()
    eleID('emailId', driver2).send_keys(mail)
    eleID('save-chnge', driver2).click()
    time.sleep(1)
    if if_present('//*[contains(text(),"Student could not saved successfully")]', driver2):
        eleID('emailId', driver2).clear()
        return 'email already used'
    eleID('verifyOTP', driver2).click()
    return mail


# verify email
def verify_email(otp):
    eleID('otp', driver2).send_keys(otp)
    eleXpath("//*[text()='Submit']", driver2).click()


def email_id_verification():
    if if_present('//*[@id="emailVerificationSuccess"]', driver2) == False:
        return False
    return True


def log_out():
    action = ActionChains(driver1)
    action.move_to_element(eleXpath('//*[@class="proflilink"]', driver2)).perform()
    eleXpath("//*[text()='Log out']", driver2).click()
    time.sleep(1)


def quitdriver():
    driver2.quit()


def ifalreadyverfied():
    return if_present_id('verifyOTP', driver2)

def outcomeform():
    driver2= create_driver_Session()
    driver2.get('https://www.pmgdisha.in/app/student/transactions')
    eleXpath('//*[@class="dash-in-title clearfix"]//*[contains(text(),"Transactions")]', driver2)
    if if_present("//*[contains(text(),'Minimum 3 transaction')]",driver2):
        return
    try:
     eleXpath("//*[contains(text(),' Fill Outcome Form')]",driver2).click()
     for ele in driver2.find_elements_by_xpath('//*[@value="false"]'):
         ele.click()
     # xpath for yes - //*[@class="radioTransactionDiv"][.//*[text()=' Use Digital Locker:']]//*[@value="true"]
     eleXpath("//*[@class='radioTransactionDiv'][.//*[text()=' Use Digital Locker:']]//*[@value='true']",
              driver2).click()
     # click ok - //*[@type="button"][contains(text(),'OK')]
     eleXpath('//*[@type="button"][contains(text(),"OK")]', driver2).click()
    except:
        pass


    # xpath for no - //*[@value="false"]

    # make payment //*[contains(text(),'Make Payment')]
    eleXpath("//*[contains(text(),'Make Payment')]",driver2).click()
    # initiate payment - id startTxnId
    eleID('startTxnId',driver2).click()
    # send paymentdemo@vpa to //*[@placeholder="Enter VPA"]
    eleXpath('//*[@placeholder="Enter VPA"]', driver2).send_keys('paymentdemo@vpa')
    # id - continue
    eleID('continue',driver2).click()
    # //*[@name='8'] , do this with 7,6,5
    eleXpath("//*[@name='8']",driver2).click()
    eleXpath("//*[@name='7']",driver2).click()
    eleXpath("//*[@name='6']",driver2).click()
    eleXpath("//*[@name='5']",driver2).click()
    # //*[@class="PINbutton enter"]
    eleXpath('//*[@class="PINbutton enter"]',driver2).click()
    # check for this to appear //*[@class="alert alert-success"] - extra time 10 second
    eleXpath('//*[@class="alert alert-success"]')
    # click //*[text()="Perform Another Transaction"]
    eleXpath('//*[text()="Perform Another Transaction"]').click()
    # initiate payment - id startTxnId
    eleID('startTxnId',driver2).click()
    # send paymentdemo@vpa to //*[@placeholder="Enter VPA"]
    eleXpath('//*[@placeholder="Enter VPA"]',driver2).send_keys('paymentdemo@vpa')

    eleID('continue',driver2).click()
    # //*[@name='8'] , do this with 7,6,5
    eleXpath("//*[@name='8']",driver2).click()
    eleXpath("//*[@name='7']",driver2).click()
    eleXpath("//*[@name='6']",driver2).click()
    eleXpath("//*[@name='5']",driver2).click()
    # //*[@class="PINbutton enter"]
    eleXpath('//*[@class="PINbutton enter"]',driver2).click()
    # check for this to appear //*[@class="alert alert-success"] - extra time 10 second
    eleXpath('//*[@class="alert alert-success"]',driver2)

    eleXpath('//*[text()="Perform Another Transaction"]',driver2).click()
    # initiate payment - id startTxnId
    eleID('startTxnId',driver2).click()
    # send paymentdemo@vpa to //*[@placeholder="Enter VPA"]
    eleXpath('//*[@placeholder="Enter VPA"]',driver2).send_keys('paymentdemo@vpa')

    eleID('continue',driver2).click()
    # //*[@name='8'] , do this with 7,6,5
    eleXpath("//*[@name='8']",driver2).click()
    eleXpath("//*[@name='7']",driver2).click()
    eleXpath("//*[@name='6']",driver2).click()
    eleXpath("//*[@name='5']", driver2).click()
    # //*[@class="PINbutton enter"]
    eleXpath('//*[@class="PINbutton enter"]', driver2).click()
    # check for this to appear //*[@class="alert alert-success"] - extra time 10 second
    eleXpath('//*[@class="alert alert-success"]', driver2)


