###IMPORTANT####    Only works with MetaMask and RARI collections on the Rarible (ethereum-single)  ###IMPORTANT###

#make sure to set your variables below for this script, examples provided

#####VARIABLE START####### (FILL BEFORE STARTING) ####
start_num = 1
listing_option='Fixed price' ### 'Timed auction' ### 'Fixed price' ###change 'Open for bids' as desired##
loop_price = 0.075
loop_title = "#"
loop_file_format = "png"
loop_description = ""
royalties = "10"
#####VARIABLES END########

driver.set_window_size(360, 740)

while loop_amount != 0:
	print("Uploading: " + str(start_num) + "  -  " + str(loop_amount) + " to go...")
	driver.switch_to.window(driver.window_handles[0])
	go_to("https://rarible.com/create/start/ethereum")
	css_and_click("button[id='create-single']")
	while True:
		try:
			print("Checking for draft discard button, please wait...")
			x = wait.until(ExpectedConditions.presence_of_element_located((By.CSS_SELECTOR, "button[data-marker='restore-modal/discardButton']")))
			x.click()
			break
		except Exception as wtf:
			#print(wtf)
			#print("----- retrying uploading -----")
			break

	if opsys == "Darwin":
		imagePath = os.path.abspath(file_folder + "/" + str(start_num) + "." + loop_file_format)
	else:
		imagePath = os.path.abspath(file_folder + "\\" + str(start_num) + "." + loop_file_format)

	css_and_key("input[name='primary-attachment']", imagePath)
	time.sleep(1)
	driver.execute_script("window.scrollTo(0, 300);")
	css_and_click("img[alt='{list_op}']".format(list_op = listing_option)) 
	time.sleep(1)

	if listing_option == "Fixed price":
		css_and_key("input[data-marker='root/appPage/create/form/price/input/priceInput']", loop_price)
	elif listing_option == "Timed auction":
		print("please contact @cloudmaking on twitter or instagram to request a custom preset for this listing option")
	elif listing_option == "Open for bids":
		pass
	else:
		print("please pick listing option")
		time.sleep(1)

	time.sleep(1)
	css_and_key("input[data-marker='root/appPage/create/form/nameInput']", loop_title+str(start_num))
	time.sleep(1)
	css_and_key("textarea[data-marker='root/appPage/create/form/descriptionInput']", loop_description)
	x = wait.until(ExpectedConditions.presence_of_element_located((By.CSS_SELECTOR, "input[data-marker='root/appPage/create/form/royaltiesInput']")))
	x.send_keys(Keys.BACKSPACE)
	x.send_keys(Keys.BACKSPACE)
	x.send_keys(royalties)  
	main_page = driver.current_window_handle
	css_and_click("button[data-marker='root/appPage/create/form/createButton']")
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
			print("Metamask popup not found, retrying...")
	css_and_click("div[data-testid='signature-request-scroll-button']")
	css_and_click("button[class='button btn--rounded btn-primary btn--large']", "waiting for first sign button, please wait...")
	time.sleep(1)
	driver.switch_to.window(main_page)

	if listing_option == "Fixed price":
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
				print("Metamask popup not found, retrying...")
		css_and_click("div[data-testid='signature-request-scroll-button']")
		css_and_click("button[class='button btn--rounded btn-primary btn--large']", "waiting for second sign window...")
		time.sleep(1)
	else:
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
				print("Metamask popup not found, retrying...")
		css_and_click("div[data-testid='signature-request-scroll-button']")
		xpath_and_click("//*[@id='app-content']/div/div[2]/div/div[3]/button[2]", "waiting for second sign window...")
		time.sleep(1)

	driver.switch_to.window(main_page)
	start_num = start_num + 1
	loop_amount = loop_amount - 1


