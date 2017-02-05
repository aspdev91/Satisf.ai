import sys, traceback, os, string, psutil, signal
import csv
import time
import json
import random
import operator
import subprocess
from datetime import datetime
from selenium import webdriver
import selenium.common.exceptions as selexc
from seamlessCredentials import getCred
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

credentials = getCred()
print(credentials)
chromeOptions = webdriver.ChromeOptions()
# To disable images 
# prefs = {"profile.managed_default_content_settings.images":2}
driver = webdriver.Chrome('./chromedriver.exe',chrome_options=chromeOptions)
driver.get('https://www.seamless.com/')


# lines = sys.stdin.readlines()
# #Since our input would only be having one line, parse our JSON data from that
# output = json.loads(lines[0])
# print(output)

# print(json.loads({'hello':'hello'}))


def loginSeamless():

	# Locates login credential input boxes
	
	driver.find_element_by_xpath('//*[@id="Site"]/ghs-main-nav/div/div[5]/div/button').click()
	WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="Site"]/div[1]/div/div/section/div[2]/div[2]/div/div/div[1]/form/div[1]/div[2]/div[1]/input')))
	email = driver.find_element_by_xpath('//*[@id="Site"]/div[1]/div/div/section/div[2]/div[2]/div/div/div[1]/form/div[1]/div[2]/div[1]/input')
	password = driver.find_element_by_xpath('//*[@id="Site"]/div[1]/div/div/section/div[2]/div[2]/div/div/div[1]/form/div[2]/div[2]/div[1]/input')

	# Enters password

	try:
		email.send_keys(credentials['username'])
		password.send_keys(credentials['password'])
		password.send_keys(Keys.RETURN)
		time.sleep(8)
	except:
		print('Failed Login')
		return

def searchRestaurant():

	# Waits until fully loaded
	try:

		WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="ghs-outerWrapper"]/div[2]/div/ghs-homepage/div/div/div/div[1]/form/ghs-start-order-form/div/div[2]/div[3]/input')))
		
		# Search restaurant for command

		searchRestaurant = driver.find_element_by_xpath('//*[@id="ghs-outerWrapper"]/div[2]/div/ghs-homepage/div/div/div/div[1]/form/ghs-start-order-form/div/div[2]/div[3]/input')
		driver.find_element_by_xpath('//*[@id="ghs-outerWrapper"]/div[2]/div/ghs-homepage/div/div/div/div[1]/form/ghs-start-order-form/div/div[1]/ghs-order-method/span[2]/label').click()
		searchRestaurant.send_keys("Home Made Taqueria")
		searchRestaurant.send_keys(Keys.RETURN)

		# Click on first search results
		# WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="ghs-search-results-restaurantId-270423"]/div[1]/div[2]/div[1]/h5/a/span')))	
		# driver.find_element_by_xpath('//*[@id="ghs-search-results-restaurantId-270423"]/div[1]/div[2]/div[1]/h5/a/span').click()
		driver.get('https://www.seamless.com/menu/home-made-taqueria-45-09-34th-ave-long-island-city/270948')
	
	except (selexc.TimeoutException, selexc.NoSuchElementException) as e:

		print("Encountered issues searching for restaurant")	

def placeOrder():

	try:
		driver.get('https://www.seamless.com/menu/home-made-taqueria-45-09-34th-ave-long-island-city/270948')
		# Find menu item and enter options
		
		WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="Item13161155"]/div/div[1]/div[2]/h6/span')))
		driver.find_element_by_xpath('//*[@id="Item13161155"]/div/div[1]/div[2]/h6/span').click()
		time.sleep(10)
		WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="Site"]/div[1]/div/div/section/div/ghs-menu-item-add/form/div[1]/ghs-menu-item-options/div/div[1]/ghs-menu-item-choice/div[2]/div[1]/div/span/label/div[2]/span')))
		driver.find_element_by_xpath('//*[@id="Site"]/div[1]/div/div/section/div/ghs-menu-item-add/form/div[1]/ghs-menu-item-options/div/div[1]/ghs-menu-item-choice/div[2]/div[1]/div/span/label/div[2]/span').click()
		driver.find_element_by_xpath('//*[@id="Site"]/div[1]/div/div/section/div/ghs-menu-item-add/form/div[1]/ghs-menu-item-options/div/div[2]/ghs-menu-item-choice/div[2]/div[1]/div/span/label/div[1]').click()

		# Add to Bag and checkout

		driver.find_element_by_xpath('//*[@id="Site"]/div[1]/div/div/section/div/ghs-menu-item-add/form/div[2]/div/div/button/span[1]/span[1]').click()
	except (selexc.TimeoutException, selexc.NoSuchElementException) as e:

		print("Encountered issues adding item to bag")	


	# For pickup if Seamless asks

	try:
	
		WebDriverWait(driver, 3).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="Site"]/div[1]/div/div/ghs-global-cart-simplified-edit/div/div[1]/div[2]/div/a[2]')))
		driver.find_element_by_xpath('//*[@id="Site"]/div[1]/div/div/ghs-global-cart-simplified-edit/div/div[1]/div[2]/div/a[2]').click()
		driver.find_element_by_xpath('//*[@id="Site"]/div[1]/div/div/ghs-global-cart-simplified-edit/div/div[3]/button[1]').click()
	
	except (selexc.TimeoutException, selexc.NoSuchElementException) as e:
	
		print("Seamless never asked about pickup or delivery")	

	# Say no to  extra offers

	try:
	
		WebDriverWait(driver, 3).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="Site"]/div[1]/div/div/section/div/ghs-menu-item-cross-sell/div/div[2]/div/div/button')))
		driver.find_element_by_xpath('//*[@id="Site"]/div[1]/div/div/section/div/ghs-menu-item-cross-sell/div/div[2]/div/div/button').click()
	
	except (selexc.TimeoutException, selexc.NoSuchElementException) as e:
	
		print('Woohoo, no pushy extra offers')
		
	# Checkout and review transaction

	time.sleep(1)
	WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="ghs-cart-checkout-button"]/span[1]')))
	driver.find_element_by_xpath('//*[@id="ghs-cart-checkout-button"]/span[1]').click()
	WebDriverWait(driver, 12).until(EC.visibility_of_element_located((By.XPATH,'//*[@id="ghs-checkout-review-submit"]')))
	driver.find_element_by_xpath('//*[@id="ghs-checkout-review-submit"]').click()
	# time.sleep(1000)

loginSeamless()
# searchRestaurant()
placeOrder()


