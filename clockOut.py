from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import time
import json
import os
import tkinter
import tkinter.messagebox
import subprocess

browser = webdriver.Chrome('/usr/local/bin/chromedriver')
cron_file = '/Users/crmonlinegraph/Documents/Scripts/clock_selenium_python_mac/cron.bak'
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
	window = tkinter.Tk()
	window.withdraw()
	message_box = {
		"window": window
	}	
	choice = tkinter.messagebox.askokcancel(title, message)
	message_box["choice"] = choice
	return message_box

def press_any_key():
	input("Press any key...")
	browser.quit()

def remove_cron_instances():
	os.system("crontab -r")
	os.system("crontab -l")

def shutdown():
	while 1:
		i=0
		try:
			message_box = Mbox("Clock Out", "Would you like to shutdown (Y/N)? ")
			if message_box["choice"] == True:
				remove_cron_instances()
				message_box["window"].destroy()
				browser.quit()
				MBox("Clock Out", "You have timed out. System shutting down...")
				print("Shutdown: Yes")
				time.sleep(3)
				os.system("pkill -u $USER")
				time.sleep(3)
				os.system("echo {} | sudo -S shutdown -h now".format(client_secret["local_pass"]))				
			else:		
				Mbox("Clock Out", "You have timed out and will not shutdown computer")
				print("Shutdown: No")
				time.sleep(3)
				message_box["window"].destroy()
				break
		except EOFError:
			i+=1

def myMain():	
	os.system("python -V")
	time_period = get_time_in_out()
	message_box = Mbox("Clock Out", "Would you like to clock out?\n\n{}\n{}".format(time_period["in"], time_period["out"]))
	if message_box["choice"] == True:	
		print("Clock Out: Yes")	
		browser.get("https://crmonline.payrollhero.com/dashboard") #go to website			
		get_element('content')
		sign_in_creds()
		get_element('footer-logo')
		browser.get("https://crmonline.payrollhero.com/my_clock")
		shutdown()
	else:
		print("Clock Out: No")
		time.sleep(3)
	remove_cron_instances()
	message_box["window"].destroy()
	browser.quit()
		
myMain()

