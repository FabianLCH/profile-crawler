# profile-crawler
A crawler script that searches for a display bug on the Forestry Profiles website. 

When the crawler detects a bug, it creates a log file that is stored locally and displays a windows toast message to the user. Then, it attempts to send an email containing the contents of the log file to all recipients in the `EMAILS` list.

## Setup
```sh
    git clone https://github.com/FabianLCH/profile-crawler
    cd profile-crawler
    pip install -r requirements.txt
    python crawler.py
```

### Add `globals.py`
Create a `globals.py` file with the following variables:

```sh
URL=
AFFECTED_IMG_SRC_BASE=
CRAWLER_EMAIL=
PASSWORD=
ADMIN_EMAILS=
```

|Variable|Type|Description|
|---|---|---|
|URL|String|The URL of the page that will be crawled|
|AFFECTED_IMG_SRC_BASE|String|The name of the image file that replaces the faculty member's image file when the bug occurs|
|CRAWLER_EMAIL|String|The email address that will be used to send crawl notifications|
|PASSWORD|String|The password for `CRAWLER_EMAIL`|
|ADMIN_EMAILS|List|A list containing emails that will receive crawler notifications|

## How to set up automatic execution with Windows Task Scheduler
In order to have the script run locally at automatic intervals, we will use the Windows Task Scheduler. To set up the Task Scheduler, follow the steps below:

1. Open the Task Scheduler and create a new folder under the _Task Scheduler Library_ folder by right clicking the folder and selecting _New Folder..._

2. Enter a name for the folder and click _OK_

3. Right click the new folder and select _Create Task..._

4. Give the task a name and select a security option from the list at the bottom. 
**NOTE:** Without administrative priviledges, the Task Scheduler will only be able to execute the script when the user is logged in. 

5. Go to the **Triggers** tab and click on _New..._ at the bottom

6. Choose a start date and time for the task and specify how often the task should run. Then, click _OK_. 

For example, to set up the task to run daily on one hour intervals choose the following settings: 
```
Settings
---
• Daily 

Advanced Settings
---
✓ Repeat task every: 1 hour
✓ Stop task if it runs longer than: 1 minute (set accordingly based on how much work the task should perform)
```
7. Go to the **Actions** tab and click on _New..._ at the bottom

8. If not selected, choose _Start a program_ from the **Action** dropdown

9. Under _Program/script_, enter the path to your `python.exe` file

10. On the _Add arguments_ field, enter the name of your Python script (e.g `script.py`)

11. On the _Start in_ field, enter the path to the folder containing your Python script and click _OK_ 

12. Go to the **Conditions** tab

13. Under _Power_, select the option _Wake the computer to run this task_.

14. Click _OK_ at the bottom to save the new task.
