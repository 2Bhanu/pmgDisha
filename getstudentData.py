from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.remote.webelement import WebElement
import time
from selenium.webdriver.support.ui import Select

from utilty import create_driver_Session, eleXpath, eleID, store_student_id_password

driver = create_driver_Session()


# login as admin
def admin_login(username, password):
    driver.get('https://www.pmgdisha.in/app/login')
    eleID('inputEmail', driver).send_keys(username)
    eleID('lgpass1', driver).send_keys(password)
    eleXpath('//*[@value="Login"]', driver).click()
    eleXpath("//button[contains(text(),'OK')]", driver).click()

    # go to student list page set page count
    driver.get('https://www.pmgdisha.in/app/trainingCenter/studentsummary')
    time.sleep(1)
    select = Select(driver.find_element_by_id('pageSize'))
    select.select_by_value('50')
    time.sleep(1)


# get unverified email student numbers and store their credentials
def get_unverified_Emails():
    unverifiedemails = driver.find_elements_by_xpath(
        "//tr[.//span[contains(text(),' Email Verified')]//*[@class='fa fa-times close-check']]")
    if len(unverifiedemails) > 0:
        store_student_id_password(find_id_password(unverifiedemails))


studentData: dict = {}


def find_id_password(elements: list[WebElement]):
    global studentData
    for element in elements:
        name = element.find_element_by_xpath('.//td[2]//span[1]').text
        print(name)
        element.find_element_by_xpath(".//img[contains(@src,"
                                      "'passkey')]").click()
        driver.switch_to.alert.accept()
        try:
            if driver.find_element_by_xpath("//*[@for='stdusername']").text == '':
                time.sleep(1)
        except:
            time.sleep(1)
        username = driver.find_element_by_xpath("//*[@for='stdusername']").text
        password = driver.find_element_by_xpath("//*[@for='stdpassword']").text
        eleXpath("//*[@class='modal-dialog']//*[contains(text(),'OK')]", driver).click()
        time.sleep(3)
        studentData.update({name: [username, password]})
    return studentData


def next_page() -> bool:
    if eleXpath("//*[@class='currPage']", driver).text == eleXpath("//*[@class='totalPage']", driver).text:
        return False
    driver.execute_script("arguments[0].click()", eleXpath('//*[@class="changePageNumber _next"][@data-increment="1"]',
                                                           driver))
    time.sleep(2)
    return True


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
