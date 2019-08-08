#!/usr/local/bin/python
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
import subprocess
import tkinter
import tkinter.messagebox

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
	time.sleep(5)
	os.system("crontab -r")
	message_box = Mbox("Clock In", "Proceed with updating cron?")
	if message_box["choice"] == True:
		time_period = {		
			"FMT": "%H:%M:%S",
			"today": datetime.now().strftime("%Y-%m-%d")
		}
		time_period["in"] = datetime.now().strftime(time_period["FMT"])
		time_period = calculate_time_out(time_period)
		print("{}:{}".format(time_period["hours"], time_period["minutes"]))	
		cron_instance = "{} {} * * 1-5 sh /Users/crmonlinegraph/Documents/Scripts/clock_selenium_python_mac/runClockOut.sh".format(time_period["minutes"], time_period["hours"])
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
		
def run_desktime():
	subprocess.call(["/bin/bash","-c","open /Applications/DeskTime.app"])

def calculate_time_out(time_period):
	time_period["out"] = datetime.strptime(time_period["in"], time_period["FMT"])
	time_period["out"] += timedelta(hours=9)
	time_period["out"] += timedelta(minutes=1)
	time_period["out"] = time_period["out"].strftime(time_period["FMT"])	
	time_period["minutes"] = time_period["out"].split(":")[1]
	time_period["hours"] = time_period["out"].split(":")[0]
	if int(time_period["hours"]) < 15:
		print("max at 3")
		time_period["hours"] = "15"
		time_period["minutes"] = "0"
		time_period["out"] = "15:00:00"
	elif (int(time_period["hours"]) == 17 and int(time_period["minutes"]) > 30) or int(time_period["hours"]) >= 18:
		print("max at 5:30")
		time_period["hours"] = "17"
		time_period["minutes"] = "30"
		time_period["out"] = "17:30:00"
	print("time period to be returned: {}:{}".format(time_period["hours"], time_period["minutes"]))
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

def set_desktop_background():	
	black_bg = "/Users/crmonlinegraph/Documents/Scripts/black_bg.png"
	backgrounds = [black_bg, black_bg]
	SET_DESKTOP_IMAGE_WRAPPER = """/usr/bin/osascript<<END
	tell application "System Events"
	{}
	end tell
	END"""

	SET_DESKTOP_IMAGE = """
	set currDesktop to desktop {idx}
	set currDesktop's picture to "{image_path}"
	"""

	script_contents = ""
	for i, img in enumerate(backgrounds):
		idx = i+1
		script_contents += SET_DESKTOP_IMAGE.format(idx=idx, image_path=img)

	script = SET_DESKTOP_IMAGE_WRAPPER.format(script_contents)
	try:
		subprocess.check_call(script, shell=True)
	except Exception as e:
		pass

def is_weekday():
	if datetime.today().weekday() < 5:
		print(datetime.today().weekday())
		return True
	return False

def myMain():	
	os.system("Python used: python -V")
	weekday = is_weekday()
	if weekday:
		run_desktime()
		browser.get("https://crmonline.payrollhero.com/dashboard") #go to website	
		get_element('require_account_id')
		sign_in_creds()
		get_element('footer-logo')
		browser.get("https://crmonline.payrollhero.com/my_clock")
		execute_update_cron()
		run_desktime()
	set_desktop_background()
	press_any_key()
	
myMain()












