This is a sample selenium script for Clocking In and Out for mac

## Requirements
* Python 2.7 or later
* Selenium
* Selenium Chrome Webdriver

## Installation of Webdrivers
[Driver Installation](http://selenium-python.readthedocs.io/installation.html)  
_put all webdrivers in __/usr/local/bin___

##### Best practices
`browser = browser(/usr/local/bin/chromedriver/)`

## Installing python
```
$ brew install python
```

## Installing pip
```
$ sudo easy_install pip
```

## Creating virtual environment
```
$ python -m virtual [environment_name] 
```  
_it will create a virtual environment with your current python installed; if it's `Python 3.7` it will already have `pip` as well_
_it will be created to the current directory that terminal is in_  

## Activating/Deactivating virtual environment
```
$ source /[virtual_env_directory]/bin/activate
$ deactivate
```
##### Adding aliases
```
$ sudo nano ~/.bash_profile
$ alias venvpy2.7="source /[virtual_env_directory]/bin/activate"
#Ctrl+O to save
#Ctrl+X to exit
$ source ~/.bash_profile #to activate your updated bash_profile

$ venvpy2.7 will automatically activate your virtual environment
(venvpy2.7) $ #virtual environment name should be included in the prompt when it is activated
```

## Installing Selenium
`$ pip install selenium`
