This is a sample selenium script for Clocking In and Out for mac

## Requirements
* Python
* Selenium
* Selenium Chrome Webdriver

## Installation of Webdrivers
[Driver Installation](http://selenium-python.readthedocs.io/installation.html)
//put all webdrivers in _/usr/local/bin_

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
$ python -m virtual env
```

## Activating/Deactivating virtual environment
```
$ source /[env directory]/bin/activate
$ deactivate
```
##### Adding aliases
```
$ sudo nano ~/.bash_profile
$ alias venvpy2.7="source /[env directory]/bin/activate"
//Ctrl+O to save
//Ctrl+X to exit
$ source ~/.bash_profile //to activate your updated bash_profile

$ venvpy2.7 will automatically activate your virtual environment
```

## Installing Selenium
`$ pip install selenium`

