###IMPORTANT####    Only works with MetaMask and Ethereum/Polygon collections on the Opensea  
# Download this extension before starting (https://chrome.google.com/webstore/detail/im-not-robot-captcha-clic/ceipnlhmjohemhfpbjdgeigkababhmjc?hl=en)
# 
# ###IMPORTANT###

#make sure to set your variables below for this script, examples provided
#####VARIABLE START####### (FILL BEFORE STARTING) ####
collection_link = "https://opensea.io/collection/instories"
start_num = 1
loop_price = 0.1
loop_title = "#"
loop_file_format = "png"
loop_external_link = "https://linktr.ee/Cloudmaking"
loop_description = ""
#this will only work with a hashlibs generated json _metadata.json file, 
#please put the metadata file in the folder and rename it "metadata.json" 
add_properties = False
number_of_properties = 5
#pick "polygon" or "ethereum"
Collection_type = "polygon" 
supply = 1
change_duration = False
#list options available: 1 day, 3 days, 1 month, 3 months, 6 months (type exactly as it is)
list_duration = "1 day" 
#####VARIABLES END########

driver.set_window_size(360, 840)

if list_duration == "1 day":
	ik = 1
elif list_duration == "3 days":
	ik = 2
elif list_duration == "1 month":
	ik = 3
elif list_duration == "3 months":
	ik = 4
elif list_duration == "6 months":
	ik = 5
else:
	print("Please enter a valid duration, skipping listing")

if add_properties == True:
	import json

	if opsys == "Darwin":
		with open('metadata/metadata.json') as f:
			data = json.load(f)
	else:
		with open('metadata\\metadata.json') as f:
			data = json.load(f)
	print("metadata file found")

	go_to(collection_link+"/assets/create")
	print("Looking for correct properties xpath...")
	driver.execute_script("window.scrollTo(0, 1000);")
	css_and_click("button[aria-label='Add properties']")
	for x in range(1, 11):
		try:
			wait.until(ExpectedConditions.presence_of_element_located((By.XPATH, f"/html/body/div[{x}]/div/div/div/section/table/tbody/tr/td[1]/div/div/input")))
			prop_div = x
			print(f"\nFound correct properties div: {prop_div}")
			break
		except:
			print(f"div {x} not found")

while loop_amount != 0:
	go_to(collection_link+"/assets/create")
	wait_for_xpath('//*[@id="main"]/div/div/section/div[2]/header/h1')

	print("\nUploading: " + str(start_num) + "  -  " + str(loop_amount) + " to go...")
	if opsys == "Darwin":
		imagePath = os.path.abspath(file_folder + "/" + str(start_num) + "." + loop_file_format)
	else:
		imagePath = os.path.abspath(file_folder + "\\" + str(start_num) + "." + loop_file_format)
	xpath_and_key('//*[@id="media"]', imagePath)

	xpath_and_key('//*[@id="name"]', loop_title + str(start_num))
	xpath_and_key('//*[@id="external_link"]', loop_external_link)
	xpath_and_key('//*[@id="description"]', loop_description)
	driver.execute_script("window.scrollTo(0, 1000);")
	
	if add_properties == True:
		css_and_click("button[aria-label='Add properties']")
		print("adding properties for " + str(start_num))
		for i in range(1, number_of_properties + 1):
			current_trait = data[start_num - 1]["attributes"][i - 1]["trait_type"]
			current_value = data[start_num - 1]["attributes"][i - 1]["value"]
			xpath_and_key(f'/html/body/div[{prop_div}]/div/div/div/section/table/tbody/tr[{i}]/td[1]/div/div/input', current_trait)
			xpath_and_key(f'/html/body/div[{prop_div}]/div/div/div/section/table/tbody/tr[{i}]/td[2]/div/div/input', current_value)
			xpath_and_click(f"/html/body/div[{prop_div}]/div/div/div/section/button")
		xpath_and_click(f"/html/body/div[{prop_div}]/div/div/div/footer/button")
	else:
		print("skipping properties")

	driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
	if Collection_type == "polygon":
		supply_css = "input[id='supply']"
		x = wait.until(ExpectedConditions.presence_of_element_located((By.CSS_SELECTOR, supply_css)))
		x.send_keys(Keys.BACKSPACE)
		x.send_keys(str(supply))
	else:
		print("Collection type is ethereum, supply is not available")
	time.sleep(1)
	driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
	xpath_and_click('//*[@id="main"]/div/div/section/div[2]/form/div[9]/div[1]/span/button', "create button not found")
	
	css_and_click("i[aria-label='Close']", "No upload confirmation, please wait, waiting for upload to finish...")

	###LISTING####
	current_page=driver.current_url
	main_page = driver.current_window_handle

	time.sleep(2)
	linktext_click("Sell")

	if change_duration == True:
		xpath_and_key('//*[@id="duration"]', "lel")
		css_and_click("input[placeholder='Select a date range']")
		xpath_and_click(f"/html/body/div[1]/div/main/div/div/div[2]/div/div[1]/div/form/div[2]/div/div[2]/div/div/div/div/div[1]/div/div[3]/div/div/div/ul/li[{ik}]/button/div")
		css_and_click("input[placeholder='Amount']")
	else:
		print("continuing with default duration")

	css_and_key("input[placeholder='Amount']", str(loop_price))
	driver.execute_script("window.scrollTo(0, 500);")
	css_and_click("button[type='submit']")

	if Collection_type == "polygon":
		time.sleep(2)
		xpath_and_click("/html/body/div[4]/div/div/div/section/div/div/section/div/div/div/div/div/div/div/button") 
		while True:
			try:
				print("Waiting for metamask popup, please wait...")
				time.sleep(5)
				for handle in driver.window_handles:
					if handle != main_page:
						login_page = handle
				driver.switch_to.window(login_page)
				break
			except Exception as wtf:
				print("metamask popup not found, retrying...")
		css_and_click("button[data-testid='request-signature__sign']")
		time.sleep(2)
		driver.switch_to.window(main_page)
		css_and_click("i[aria-label='Close']")
	elif Collection_type == "ethereum":
		while True:
			try:
				print("Waiting for metamask popup, please wait...")
				time.sleep(5)
				for handle in driver.window_handles:
					if handle != main_page:
						login_page = handle
				driver.switch_to.window(login_page)
				break
			except Exception as wtf:
				print("metamask popup not found, retrying...")
		xpath_and_click("//*[@id='app-content']/div/div[2]/div/div[3]/div[1]/img")
		xpath_and_click("//*[@id='app-content']/div/div[2]/div/div[4]/button[2]")
		time.sleep(2)
		driver.switch_to.window(main_page)
		time.sleep(1)
	else:
		print("Please pick either 'polygon' or 'ethereum' / no caps, make sure the spelling is correct")
		break
		
	start_num = start_num + 1
	loop_amount = loop_amount - 1

