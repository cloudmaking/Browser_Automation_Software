import subprocess
import os
import platform
import threading
import time
from tkinter import filedialog, Tk

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ExpectedConditions
import chromedriver_autoinstaller


class Autochrome:
	def __init__(self):
		self.browser_port = 8080
		self.operating_system = platform.system()
		self.main_directory = os.getcwd()
		self.stop_tester = threading.Event()

	def open_chrome_profile(self):
		while True:
			try:
				self.profile_location = filedialog.askdirectory(
				    initialdir=self.main_directory, title="Select Chrome Profile Folder")
				if self.profile_location == "":
					print("No profile selected")
					continue
				else:
					if self.operating_system == "Windows":
						cmd = ['start', 'chrome',
						    f'--remote-debugging-port={self.browser_port}', f'--user-data-dir={self.profile_location}']
						subprocess.Popen(cmd, shell=True)
					elif self.operating_system == "Darwin":
						cmd = f"open -a /Applications/Google\ Chrome.app --args \ --remote-debugging-port={self.browser_port} \ --user-data-dir={self.profile_location}"
						subprocess.Popen(cmd, shell=True)
					else:
						cmd = ['google-chrome',
						    f'--remote-debugging-port={self.browser_port}', f'--user-data-dir={self.profile_location}']
						subprocess.Popen(cmd, shell=True)
					print("Opening debug browser on port {port_num}".format(
					    port_num=self.browser_port))
					break
			except Exception as e:
				print("Error opening browser" + str(e))
				time.sleep(1)

	def connect_to_browser(self):
		chromedriver_autoinstaller.install()
		op = webdriver.ChromeOptions()
		op.add_experimental_option(
		    "debuggerAddress", f"localhost:{self.browser_port}")
		self.driver = webdriver.Chrome(options=op)
		self.wait = WebDriverWait(self.driver, 10)
		print(f"Connected to browser on port {self.browser_port}")

	def run_tester(self):
		try:
			root = Tk()
			root.withdraw()  # Hide the main window
			file_path = filedialog.askopenfilename(filetypes=[("Python files", "*.py")])
			root.destroy()  # Destroy the main window
			if file_path:
				with open(file_path, 'r') as file:
					code = file.read()
				t = threading.Thread(target=lambda: exec(code))
				t.start()
			else:
				print("No file selected")
		except Exception as e:
			print("Error in run_tester: ", e)

	def xpath_and_click(self, code, fail_message="Xpath not found"):
		while True:
			try:
				x = self.wait.until(
				    ExpectedConditions.presence_of_element_located((By.XPATH, code)))
				x.click()
				break
			except:
				print(fail_message + ": " + code + "\nretrying...")
				time.sleep(1)

	def css_and_click(self, code, fail_message="Css not found"):
		while True:
			try:
				x = self.wait.until(
				    ExpectedConditions.presence_of_element_located((By.CSS_SELECTOR, code)))
				x.click()
				break
			except:
				print(fail_message + ": " + code + "\nretrying...")
				time.sleep(1)

	def xpath_and_key(self, code, key, fail_message="Xpath not found"):
		while True:
			try:
				x = self.wait.until(
				    ExpectedConditions.presence_of_element_located((By.XPATH, code)))
				x.send_keys(key)
				break
			except:
				print(fail_message + ": " + code + "\nretrying...")
				time.sleep(1)

	def css_and_key(self, code, key, fail_message="Css not found"):
		while True:
			try:
				x = self.wait.until(
				    ExpectedConditions.presence_of_element_located((By.CSS_SELECTOR, code)))
				x.send_keys(key)
				break
			except:
				print(fail_message + ": " + code + "\nretrying...")
				time.sleep(1)

	def go_to(self, address, fail_message="Address not found"):
		while True:
			try:
				self.driver.get(address)
				break
			except:
				print(fail_message + ": " + address + "\nretrying...")
				time.sleep(1)

	def wait_for_xpath(self, code, fail_message="Element not found"):
		while True:
			try:
				self.wait.until(
				    ExpectedConditions.presence_of_element_located((By.XPATH, code)))
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
	
	print("\n------------------------------------------------")
	print("-------------Initialization Complete--------------")
	print("Make sure to put 'ac.' before any selenium commands")
	print("--------------------------------------------------")
	print('if ac.stop_tester.is_set(): \n	print("Stopping tester") \n	   break \nadd the above code to your script to stop the tester')
	print("please insure that its in the loop of your script \nif you do nto have a loop in your scritp, ignore this message")
	print("----------------------------------------")

	while True:
		print("\nChoose 1 to run a script")
		print("Choose 2 to stop a script with a loop while its running")
		print("Type 'exit' to Exit")
		choice = input("Enter your choice: ")
		if choice == "1":
			ac.stop_tester.clear()
			ac.run_tester()
			continue
		elif choice == "2":
			ac.stop_tester.set()
			continue
		elif choice == "exit":
			print("Exiting... Goodbye!")
			break
		else:
			print("Invalid choice, try again")
