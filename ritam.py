from urllib import response
import requests
import csv
from appium import webdriver
from appium.webdriver.common.mobileby import MobileBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os
import time
import os
from datetime import datetime
  # Import the csv module
# File path for the CSV file
csv_file_path = "crediantial.csv"  # Make sure the CSV file is in the same folder as your script

# Function to read credentials from the CSV file
def read_credentials_from_csv(file_path):
    try:
        with open(file_path, 'r', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                username = row['username']
                access_key = row['accesskey']
                yield username, access_key  # Yield each set of credentials
    except FileNotFoundError:
        print(f"CSV file '{file_path}' not found.")
        exit(1)
    except Exception as e:
        print(f"Error reading CSV file: {e}")
        exit(1)
#==============================================================================
#URL for the LambdaTest API
url = "https://manual-api.lambdatest.com/app/upload/realDevice"

# Rest of your code remains the same from here onwards...
file_path = "amazon-india-shopping-26-16-2-350.apk"
app_name = "appname"

# Create a dictionary for the form data
data = {
    "name": app_name,
}

# Create a dictionary for the file to be uploaded
files = {
    "appFile": (file_path, open(file_path, "rb")),
}
#===================================================================================
# Loop through each set of credentials from the CSV file
for username, access_key in read_credentials_from_csv(csv_file_path):
    # Construct the authentication header
    auth = (username, access_key)

    #Send the POST request
    response = requests.post(url, auth=auth, data=data, files=files)

    #Check the response status code and handle accordingly
    response.status_code=200
    if response.status_code == 200:
        print(response.text)
        print("File uploaded successfully!")
        response_data = response.json()
        app_url = response_data.get('app_url')
        if app_url:
            current_datetime = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
            print(f"{username} is and App ID: {app_url}")
            capability = {
                "lt:options": {
                    "w3c": True,
                    "platformName": "android",
                    "deviceName": "Galaxy S22 Ultra 5G",
                    "platformVersion": "12",
                    "isRealMobile": True,
                    "build": "Android APP Automation",
                    "name": "Proverbial Test"+current_datetime,
                    "network": False,
                    "visual": True,
                    "video": True,
                    "app":app_url,
                    "devicelog":True,
                    "crashlog":True

                }
        }
        try:
            driver = webdriver.Remote(desired_capabilities=capability, command_executor="https://" +
                                  username+":"+access_key+"@mobile-hub.lambdatest.com/wd/hub")
            colorElement = WebDriverWait(driver, 20).until(EC.element_to_be_clickable(
                (MobileBy.ID, "com.lambdatest.proverbial:id/color")))
            colorElement.click()

            textElement = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((MobileBy.ID, "com.lambdatest.proverbial:id/Text")))
            textElement.click()

            toastElement = WebDriverWait(driver, 20).until(EC.element_to_be_clickable(
                (MobileBy.ID, "com.lambdatest.proverbial:id/toast")))
            toastElement.click()

            notification = WebDriverWait(driver, 20).until(EC.element_to_be_clickable(
                (MobileBy.ID, "com.lambdatest.proverbial:id/notification")))
            notification.click()

            geolocation = WebDriverWait(driver, 20).until(EC.element_to_be_clickable(
                (MobileBy.ID, "com.lambdatest.proverbial:id/geoLocation")))
            geolocation.click()
            time.sleep(5)

            driver.back()

            home = WebDriverWait(driver, 20).until(EC.element_to_be_clickable(
                (MobileBy.ID, "com.lambdatest.proverbial:id/buttonPage")))
            home.click()

            speedTest = WebDriverWait(driver, 20).until(EC.element_to_be_clickable(
                (MobileBy.ID, "com.lambdatest.proverbial:id/speedTest")))
            speedTest.click()
            time.sleep(5)

            driver.back()

            browser = WebDriverWait(driver, 20).until(EC.element_to_be_clickable(
                (MobileBy.ID, "com.lambdatest.proverbial:id/webview")))
            browser.click()

            url_1 = WebDriverWait(driver, 20).until(EC.element_to_be_clickable(
                (MobileBy.ID, "com.lambdatest.proverbial:id/url")))
            url_1.send_keys("https://www.lambdatest.com")

            find = WebDriverWait(driver, 20).until(EC.element_to_be_clickable(
                (MobileBy.ID, "com.lambdatest.proverbial:id/find")))
            find.click()
            driver.quit()
        except:
            driver.quit()
    else:
        print(f"Failed to upload file. Status code: {response.status_code}")
        print(response.text)
    
