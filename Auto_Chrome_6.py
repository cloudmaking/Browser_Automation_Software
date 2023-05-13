import subprocess
from tkinter import *
from tkinter import filedialog
import re
import os
import sys
import time
import platform

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ExpectedConditions
import chromedriver_autoinstaller


class Autochrome:
	def __init__(self):
		self.browser_port = int(8080)
		self.operating_system = platform.system()
		self.main_directory = os.getcwd()

	def open_chrome_profile(self):
		while True:
			try:
				self.profile_location = filedialog.askdirectory(initialdir = self.main_directory,title = "Select Chrome Profile Folder")
				if self.profile_location == "":
					print("No profile selected")
					continue
				else:
					if self.operating_system == "Windows":
						cmd = ['start', 'chrome', f'--remote-debugging-port={self.browser_port}', f'--user-data-dir={self.profile_location}']
						subprocess.Popen(cmd, shell=True)
					elif self.operating_system == "Darwin": 
						cmd = f"open -a /Applications/Google\ Chrome.app --args \ --remote-debugging-port={self.browser_port} \ --user-data-dir={self.profile_location}"
						subprocess.Popen(cmd, shell=True)
					else:
						cmd = ['google-chrome',f'--remote-debugging-port={self.browser_port}', f'--user-data-dir={self.profile_location}']
						subprocess.Popen(cmd , shell=True)
					print("Opening debug browser on port {port_num}".format(port_num=self.browser_port))
					break
			except:
				print("Error opening browser")
				time.sleep(1)

	def connect_to_browser(self):
		chromedriver_autoinstaller.install()
		op = webdriver.ChromeOptions()
		op.add_experimental_option("debuggerAddress", f"localhost:{self.browser_port}")
		self.driver = webdriver.Chrome(options=op)
		self.wait = WebDriverWait(self.driver, 10)
		print(f"Connected to browser on port {self.browser_port}")

	def run_preset_script(self):
		self.file_location = filedialog.askopenfilename(initialdir = self.main_directory, title = "Select Preset file", filetypes = (("python files", "*.py"), ("text files","*.txt"), ("all files","*.*")))
	
		if not self.file_location: 
			print("No file selected")
			return
	
		print("Running preset script: " + self.file_location)
		try:
			exec(open(self.file_location).read())
		except Exception as e:
			print(f"An error occurred while executing the script: {e}")
			return
	
		print("-------------------------")
		print("Script Execution Complete")
		print("-------------------------")


	def open_command_tester(self):
		self.root = Tk()
		self.root.title("Command Tester for AutoChrome 6 - By: @Cloudmaking")
		self.root.geometry("700x400")
		print("\n-------------------------")
		print("Welcome to the Command tester for AutoChrome.")
		print("This GUI's is for testing your selectors e.g. XPATH or CSS")
		print("The selectors can be found by right clicking an element in your browser and clicking inspect.")
		print("For more instructions visit my website:")
		print("https://www.aliraza.cloud/chrome-automation")
		print("\nCustom Functions:")
		print("- xpath_and_click(code, fail_message= \"Xpath not found\")")
		print("- css_and_click(code, fail_message= \"CSS not found\")")
		print("- xpath_and_key(code, keys, fail_message= \"CSS not found\")")
		print("- css_and_key(code, keys, fail_message= \"CSS not found\")")
		print("- go_to(url)")
		print("- Dont forget, You can also use the selenium webdriver commands directly.")
		print("-------------------------")
		self.start_button = Button(text= "Run Preset", command = self.run_tester, bg = "green", font=("Arial Black", 10))
		self.start_button.pack(anchor=N, pady=5, padx=5)
		self.TextArea = Text(self.root, relief=GROOVE)
		self.TextArea.pack(expand=True, fill=BOTH)
		self.TextArea.focus()
		self.TextArea.config(tabs=('0.5c', '1c', '1.5c', '2c'))
		self.TextArea.config(wrap=NONE)
		self.scrollx = Scrollbar(self.TextArea, orient=VERTICAL, command=self.TextArea.yview)
		self.scrollx.pack(side=RIGHT, fill=Y)
		self.TextArea.config(yscrollcommand=self.scrollx.set)
		self.scrollx.config(cursor='arrow')

	def run_tester(self):
		exec(self.TextArea.get(1.0, END))
	
	def xpath_and_click(self, code, fail_message= "Xpath not found"):
		while True:
			try:
				x = self.wait.until(ExpectedConditions.presence_of_element_located((By.XPATH, code)))
				x.click()
				break
			except:
				print(fail_message + ": " + code + "\nretrying...")
				time.sleep(1)

	def css_and_click(self, code, fail_message= "Css not found"):
		while True:
			try:
				x = self.wait.until(ExpectedConditions.presence_of_element_located((By.CSS_SELECTOR, code)))
				x.click()
				break
			except:
				print(fail_message + ": " + code + "\nretrying...")
				time.sleep(1)

	def xpath_and_key(self, code, key, fail_message= "Xpath not found"):
		while True:
			try:
				x = self.wait.until(ExpectedConditions.presence_of_element_located((By.XPATH, code)))
				x.send_keys(key)
				break
			except:
				print(fail_message + ": " + code + "\nretrying...")
				time.sleep(1)

	def css_and_key(self, code, key, fail_message= "Css not found"):
		while True:
			try:
				x = self.wait.until(ExpectedConditions.presence_of_element_located((By.CSS_SELECTOR, code)))
				x.send_keys(key)
				break
			except:
				print(fail_message + ": " + code + "\nretrying...")
				time.sleep(1)

	def go_to(self, address, fail_message= "Address not found"):
		while True:
			try:
				self.driver.get(address)
				break
			except:
				print(fail_message + ": " + address + "\nretrying...")
				time.sleep(1)

	def wait_for_xpath(self, code, fail_message= "Element not found"):
		while True:
			try:
				self.wait.until(ExpectedConditions.presence_of_element_located((By.XPATH, code)))
				break
			except:
				print(fail_message + ": " + code + "\nretrying...")
				time.sleep(1)

if __name__ == "__main__":
	ac = Autochrome()
	print("----------------------------------------")
	print("-------Welcome to AutoChrome 6.0-------")
	print("----------------------------------------")
	print("This program is free to use, but if you would like to support me, \nplease consider donating to my paypal: paypal.me/cloudmaking")
	print("If you would like to request a paid commission, please contact me on twitter @cloudmaking")
	print("----------------------------------------")
	print("---Press Ctrl+C to exit at any point---")
	print("----------------------------------------")
	while True:
		print("Initializing Step 1/2: \nPlease select your chrome profile folder or an EMPTY folder to create a new profile")
		print("Warning: The chrome profile consists of a lot of files, so DO NOT select a folder with other files in it")
		choice = input("Type 1 to Continue or 2 to skip this step: ")
		if choice == "1":
			try:
				ac.open_chrome_profile()
				break
			except:
				print("Failed to open chrome profile, please try again")
		elif choice == "2":
			break
		else:
			print("Invalid input, please try again")
	time.sleep(1)
	while True:
		print("\nInitializing Step 2/2:")
		try:
			ac.connect_to_browser()
			break
		except Exception as e:
			print("Failed to connect to browser")
			choice = input("Choose 1 to retry, 2 to show the error, anything else to exit:")
			if choice == "1": continue
			elif choice == "2": print(e)
			else: exit()
	time.sleep(1)
	print("\n------------------------------------------------")
	print("-------------Initialization Complete--------------")
	print("Make sure to put 'ac.' before any selenium commands")
	print("--------------------------------------------------")
	while True:
		print("\nChoose 1 to run a preset script")
		print("Choose 2 to open the command tester GUI (for advanced users)")
		print("Choose 3 to re-open the Chrome profile")
		print("\nType 'exit' to Exit")
		choice = input("Enter your choice: ")
		if choice == "1":
			ac.run_preset_script()
			continue
		elif choice == "2":
			ac.open_command_tester()
			continue
		elif choice == "3":
			ac.open_chrome_profile()
			continue
		elif choice == "exit":
			print("Exiting... Goodbye!")
			break
		else:
			print("Invalid choice, try again")
