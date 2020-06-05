import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from win10toast import ToastNotifier
import traceback

import datetime
import re
import requests
from bs4 import BeautifulSoup

from globals import URL, AFFECTED_IMG_SRC_BASE, CRAWLER_EMAIL, PASSWORD, ADMIN_EMAILS

"""
Crawl Forestry website
"""
today = datetime.datetime.now()
output_file = "./crawl-logs/{0}-{1}-{2}_{3}-{4}_affected-profiles.txt".format(today.year, today.month, ("0" + str(today.day)) if today.day < 10 else today.day, today.hour, ("0" + str(today.minute)) if today.minute < 10 else today.minute)
error_file = "./error-logs/{0}-{1}-{2}_{3}-{4}_errors.txt".format(today.year, today.month, ("0" + str(today.day)) if today.day < 10 else today.day, today.hour, ("0" + str(today.minute)) if today.minute < 10 else today.minute)

# request the html from the page and parse it
req = requests.get(URL)
soup = BeautifulSoup(req.text, "lxml")

# create empty list with affected profiles
affectedProfiles = []

# get all divs with id that starts with "post"
content = soup.find(id="content")
profileList = content.find_all(id=re.compile("^post"))

for profile in profileList:
    try:
        profile_image = profile.find("img")
        if profile_image is not None and AFFECTED_IMG_SRC_BASE in profile_image['src']:
            
            # ignore the original profile
            last_name = profile.find(id="last")
            if last_name is not None and last_name.string == "Innes":
                continue

            affectedProfiles.append(profile)
    except Exception as e:
        error_traceback = traceback.format_exc()

        crawlErrorToast = ToastNotifier()
        crawlErrorToast.show_toast("Crawl Error", "Could not successfully crawl the profiles page.", duration=5)
        
        with open(error_file, "w") as errors:
            errors.write(error_traceback)

# check if there are any bugged profiles 
if len(affectedProfiles) != 0:
    toaster = ToastNotifier()
    toaster.show_toast("Profile Crawler", "The crawler found affected profiles!", duration=5)

    with open(output_file, "w") as affected_profiles_text:
        
        affected_profiles_text.write("The crawler has found the following profiles were affected: \n")

        for affProf in affectedProfiles:
            # get name strings
            given = affProf.find(id="first").string if affProf.find(id="first") else ""
            middle = affProf.find(id="middle").string if affProf.find(id="middle") else ""
            last = affProf.find(id="last").string if affProf.find(id="last") else "" 

            # add spaces to given name and middle initial conditionally
            given += " "
            middle = middle + " " if len(middle) != 0 else middle

            full_name = given + middle + last
            affected_profiles_text.write(full_name + "\n")
    
    try:
        """
        Set up SMTP server
        """
        s = smtplib.SMTP(host='smtp-mail.outlook.com', port=587)
        s.starttls()
        s.login(CRAWLER_EMAIL, PASSWORD)

        for email in ADMIN_EMAILS:
            msg = MIMEMultipart()

            with open(output_file) as aff_prof_txt:
                message = aff_prof_txt.read()
            
            msg['From'] = CRAWLER_EMAIL
            msg['To'] = email
            msg['Subject'] = "Forestry Profiles Crawl Alert"

            msg.attach(MIMEText(message, 'plain'))

            s.send_message(msg)

            del msg
    except Exception as e:
        errorToaster = ToastNotifier()
        errorToaster.show_toast("Profile Crawler Error", "The crawler was unable to send an email report. Please check the errors file for more details", duration=10)
        
        with open(error_file, "w") as errors:
            errors.write(repr(e))
else:
    for i in range(10):
        print("No affected profiles.")