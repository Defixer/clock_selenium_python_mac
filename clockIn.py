from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import time
import json
import os
from datetime import datetime, timedelta

browser = webdriver.Chrome('/usr/local/bin/chromedriver')
cron_file = '/Users/crmonlinegraph/Documents/Scripts/clock_selenium_python_mac/cron.bak'
client_secret = "/Users/crmonlinegraph/Documents/Scripts/client_secret.json"
timeout = 5

def sign_in_creds():	
	with open(client_secret) as json_file:
		data = json.load(json_file)

	username = browser.find_element_by_id('username')
	print("Username entered")
	time.sleep(2)
	username.send_keys(data["username"])
	password = browser.find_element_by_id('password')
	password.send_keys(data["password"])
	print("Password entered")
	time.sleep(2)
	sign_in = browser.find_element_by_name('commit')
	sign_in.click()
	print("Sign In clicked")

def execute_update_cron():
	choice = Mbox("Clock In", "Proceed with updating cron?")
	if choice == 0:
		time_period = {		
			"FMT": "%H:%M:%S",
			"today": datetime.now().strftime("%Y-%m-%d")
		}
		time_period["in"] = datetime.now().strftime(time_period["FMT"])
		time_period = calculate_time_out(time_period)	
		cron_instance = "{} {} * * 1-5 ./Users/crmonlinegraph/Documents/Scripts/clock_selenium_python_mac/runClockOut.sh".format(time_period["minutes"], time_period["hours"])
		footer = "\n#Date\t  | {}\n#Time In  | {}\n#Time Out | {}\n".format(time_period["today"], time_period["in"], time_period["out"])

		file = open(cron_file, 'w+')
		file.write(cron_instance)
		file.write(footer)
		file.close()	

		print("Cron Updated")
		os.system("crontab {}".format(cron_file))
		os.system("crontab -l")
	else:
		print("User selected 'Cancel'. Script terminates.")
		
def calculate_time_out(time_period):
	time_period["out"] = datetime.strptime(time_period["in"], time_period["FMT"])
	time_period["out"] += timedelta(hours=9)
	time_period["out"] = time_period["out"].strftime(time_period["FMT"])	
	time_period["minutes"] = time_period["out"].split(":")[1]
	time_period["hours"] = time_period["out"].split(":")[0]
	return time_period

def Mbox(title, message):
	message_box = '\'Tell application "System Events" to display dialog "{}" with title "{}"\''.format(message, title)
	return os.system('osascript -e {}'.format(message_box))

def press_any_key():
	input("Press any key...")
	browser.quit()

def get_element(element_id):
	i = 0
	while True:
		try:
			element = WebDriverWait(browser, timeout).until(EC.presence_of_element_located((By.ID, element_id)))
			print("Element fetched: {}".format(element.text))
			break
		except TimeoutException:
			if i > 6:
				print("Loading took too much time! Check network connection")
				press_any_key()
			else:
				print("Retrying ({})".format(i))
			i+=1

def myMain():	
	browser.get("https://crmonline.payrollhero.com/dashboard") #go to website	
	get_element('require_account_id')
	sign_in_creds()
	get_element('footer-logo')
	browser.get("https://crmonline.payrollhero.com/my_clock")
	execute_update_cron()
	press_any_key()
	
myMain()












