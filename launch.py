from selenium import webdriver
import discord
from discord.ext import tasks
from datetime import datetime

client = discord.Client()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    testCheck.start()

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')

    if message.content.startswith('$check'):
        details = {
        "Licence": "", # Full UK Driving Licence
        "Booking_Ref": "", # Current Test Booking Reference
        "Test_Center": "", # Test Center Name / Postcode
        "before_date": ""
        }

        # Use Chrome for website
        driver = webdriver.Chrome("/usr/bin/chromedriver")

        # Open the test booking management website
        driver.get('https://driverpracticaltest.dvsa.gov.uk/login')

        # Login with current test details
        driver.find_element_by_id("driving-licence-number").send_keys(details["Licence"])

        driver.find_element_by_id("application-reference-number").send_keys(details["Booking_Ref"])

        driver.find_element_by_id("booking-login").click()

        # Get current test date
        date_time_str = driver.find_element_by_xpath("/html/body/div[2]/div[4]/section/section[1]/div/dl/dd[2]").get_attribute('innerHTML')
        print(date_time_str)
        details["before_date"] = datetime.strptime(date_time_str, '%A %d %B %Y')

        # Change test center option
        driver.find_element_by_id("test-centre-change").click()

        driver.find_element_by_id("test-centres-input").clear();
        driver.find_element_by_id("test-centres-input").send_keys(details["Test_Center"])

        driver.find_element_by_id("test-centres-submit").click()

        # Select first test center
        results_container = driver.find_element_by_class_name("test-centre-results")

        test_center = results_container.find_element_by_xpath(".//a")

        test_center.click()

        #Check if any tests avaliable
        if "There are no tests available" in driver.find_element_by_id("main").get_attribute('innerHTML'):
            driver.quit()
            await message.channel.send('No test available')
        else:
            await message.channel.send('Tests available, checking dates...')


            minDate = details["before_date"]

            available_calendar = driver.find_element_by_class_name("BookingCalendar-datesBody")
            available_days = available_calendar.find_elements_by_xpath(".//td")
            available_days_msg = ""

            for day in available_days:
                if not "--unavailable" in day.get_attribute("class"):
                    day_a = day.find_element_by_xpath(".//a")
                    if datetime.strptime(day_a.get_attribute("data-date"), "%Y-%m-%d") < minDate:
                        await message.channel.send('Available: ' + day_a.get_attribute('data-date'))
                        available_days_msg = available_days_msg + """
                        """+ day_a.get_attribute("data-date")

            if available_days_msg == "":
                driver.quit()
                await message.channel.send('No tests are available')
            else:
                messages = """Driving tests have become available at """ + details["Test_Center"] + """ on the following days before """ + details["before_date"].strftime('%d/%m/%Y') + """:
                """ + available_days_msg + """
                Click here to launch the DVSA booking website: https://driverpracticaltest.dvsa.gov.uk/manage
                """
                await message.channel.send(messages)
                driver.quit()


@tasks.loop(seconds = 1800)
async def testCheck():
    #Channel ID to send update every 30 minutes
    channel = client.get_channel()

    currentTime = datetime.now()
    currentTime = currentTime.strftime("%H:%M:%S")
    start = '10:00:00'
    end = '23:00:00'

    if currentTime > start and currentTime < end:


        details = {
        "Licence": "", # Full UK Driving Licence
        "Booking_Ref": "", # Current Test Booking Reference
        "Test_Center": "", # Test Center Name / Postcode
        "before_date": ""
        }

        # Use Chrome for website
        driver = webdriver.Chrome("/usr/bin/chromedriver")

        # Open the test booking management website
        driver.get('https://driverpracticaltest.dvsa.gov.uk/login')

        # Login with current test details
        driver.find_element_by_id("driving-licence-number").send_keys(details["Licence"])

        driver.find_element_by_id("application-reference-number").send_keys(details["Booking_Ref"])

        driver.find_element_by_id("booking-login").click()

        # Get current test date
        date_time_str = driver.find_element_by_xpath("/html/body/div[2]/div[4]/section/section[1]/div/dl/dd[2]").get_attribute('innerHTML')
        print(date_time_str)
        details["before_date"] = datetime.strptime(date_time_str, '%A %d %B %Y')

        # Change test center option
        driver.find_element_by_id("test-centre-change").click()

        driver.find_element_by_id("test-centres-input").clear();
        driver.find_element_by_id("test-centres-input").send_keys(details["Test_Center"])

        driver.find_element_by_id("test-centres-submit").click()

        # Select first test center
        results_container = driver.find_element_by_class_name("test-centre-results")

        test_center = results_container.find_element_by_xpath(".//a")

        test_center.click()

        #Check if any tests avaliable
        if "There are no tests available" in driver.find_element_by_id("main").get_attribute('innerHTML'):
            driver.quit()
            await channel.send('No test available')
        else:
            minDate = details["before_date"]
            available_calendar = driver.find_element_by_class_name("BookingCalendar-datesBody")
            available_days = available_calendar.find_elements_by_xpath(".//td")
            available_days_msg = ""

            for day in available_days:
                if not "--unavailable" in day.get_attribute("class"):
                    day_a = day.find_element_by_xpath(".//a")
                    if datetime.strptime(day_a.get_attribute("data-date"), "%Y-%m-%d") < minDate:
                        await channel.send('Available: ' + day_a.get_attribute('data-date'))
                        available_days_msg = available_days_msg + """
                        """+ day_a.get_attribute("data-date")

        if available_days_msg == "":
       		driver.quit()
        	await channel.send('No tests are available')
        else:
        	messages = """@everyone \n Driving tests have become available at """ + details["Test_Center"] + """ on the following days before """ + details["before_date"].strftime('%d/%m/%Y') + """:\n
""" + available_days_msg +""" \n
Click here to launch the DVSA booking website: https://driverpracticaltest.dvsa.gov.uk/manage
        """
        	await channel.send(messages)
       		driver.quit()
    else:
        await channel.send('Out of hours, only operational between 10:00-23:00')

#Discord bot token
client.run('')
