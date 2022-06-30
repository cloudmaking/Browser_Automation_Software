Visit my website for the instructions with hyperlinks to downlaod and tutorials and more...
https://www.aliraza.cloud/chrome-automation

**Requirements:**

- Python3 and pip

- Chrome browser v.96+

- Download the Chromedriver and put in the chromedrivers folder 

(follow instructions + link in folder)

For MacOS you might have to manually install the latest version of the chromedriver and place it in the "chromedrivers" folder (additionally you might have to add the chromedriver to your firewall exceptions) read notes below form a MacOS user for more details follow all the instructions below

**Instructions:**

1. Download and or Update Python and The Chrome browser (if you don’t have it already)

2. Download and extract the project in your desired location (keep all files and folders that come with the repo in this folder)

3. Drink some Water fi you havnt today.

4. Run the following command "pip install selenium" for windows and "pip3 install selenium" for MacOS (in terminal, powershell or console)

5. Download the latest version of Chromedriver, delete everything in the chromedriver folder provided and put the New Chromedriver in that folder, please do not rename anything and again make your you are using the latest version of the chrome browser.

6. Run the script (Auto_Chrome.py) by double clicking it (for MAC right click and run in python launcher)

7. Open a pre-set file inside the script (make sure to pick the right pre-set for you or make your own)

8. Press the "Open Browser" button (If a browser window opens that means everything is working so far)

9. Run the script

**Pre-set Builder Commands: **

(Remember, all normal python code and syntax works)

Video tutorial on how to make your own pre-sets: Click ME! 

Find CSS and XPATH codes through the inspect window on chrome. All base selenium code also works fine (this just makes it so you don't need to setup anything)

- go_to(address, fail_message[optional])

- css_and_key(code, key, fail_message[optional])

- xpath_and_key(code, key, fail_message[optional])

- css_and_click(code, fail_message[optional])

- xpath_and_click(code, fail_message[optional])

- linktext_click(code, key, fail_message[optional])

- wait_for_xpath(code, fail_message[optional])



Must watch video for understanding selenium and making your own automation scripts: https://www.youtube.com/watch?v=tRNwTXeJ75U

Important Notes please read before starting:

Do not move anything in or out of the main script folder.

(here is a link to a handy script which does that for you: https://github.com/FireMarshmallow/Easy-file-renamer)

As far as know this only works with windows and MAC OS

Message from a MacOS user:

You might need to remove the quarantine attribute from the chromedriver, I did this by issuing the following command in the Terminal: xattr -r -d com.apple.quarantine ~/Downloads/Auto_Chrome_2-main/chromedrivers/chromedriver

You might also need to add the chromedriver to the mac Firewall exception list like so:

System Preferences > Security & Privacy > (Unlock the padlock if necessary) Firewall options > click on the + icon and locate the chromedriver

--------------------------------

If you have any questions or want to get in contact you can find me on Instagram and twitter by searching @cloudmaking (feel free to DM).

If you want to support this project or me, please check out my NFTs and maybe buy some, I accept most bids. https://opensea.io/collection/cryptoverse1 or Donate below: https://paypal.me/CloudMaking?locale.x=en_GB
