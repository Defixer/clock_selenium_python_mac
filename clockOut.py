from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import time
import json
import os

browser = webdriver.Chrome('/usr/local/bin/chromedriver')
cron_file = '/Users/crmonlinegraph/Documents/Scripts/cron.bak'
client_secret = "/Users/crmonlinegraph/Documents/Scripts/client_secret.json"
timeout = 5

def get_element(element_attrib):
	i = 0
	while True:
		try:
			element = WebDriverWait(browser, timeout).until(EC.presence_of_element_located((By.ID, element_attrib)))
			print("Element fetched: {}".format(element.text))
			return element
			break
		except TimeoutException:
			if i > 6:
				print("Loading took too much time! Check network connection")
				press_any_key()
			else:
				print("Retrying ({})".format(i))
			i+=1

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

def get_time_in_out():
	time_period = {}
	lines = [line.rstrip('\n') for line in open(cron_file)]
	for line in lines:
		print(line)
		if "In" in line:
			time_period["in"] = line
		if "Out" in line:
			time_period["out"] = line
	return time_period
		
def Mbox(title, message):
	message_box = '\'Tell application "System Events" to display dialog "{}" with title "{}"\''.format(message, title)
	return os.system('osascript -e {}'.format(message_box))

def press_any_key():
	input("Press any key...")
	browser.close()

def shutdown():
	choice = input("Shutdown PC (Y/N)? ")
	if choice.upper() == "Y":
		print("You have timed out. System shutting down...")
		time.sleep(3)
		os.system("sudo shutdown -h now")
	else:		
		print("You have timed out and will not shutdown computer")
		time.sleep(3)

def myMain():	
	time_period = get_time_in_out()
	choice = Mbox("Clock Out", "Would you like to clock out?\n\n{}\n{}".format(time_period["in"], time_period["out"]))
	if choice == 0:		
		browser.get("https://crmonline.payrollhero.com/dashboard") #go to website			
		get_element('content')
		sign_in_creds()
		get_element('footer-logo')
		press_any_key()
		shutdown()
		
myMain()