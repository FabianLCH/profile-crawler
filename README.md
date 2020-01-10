# profile-crawler
A crawler script that searches for a display bug on a specified URL. 

When the crawler detects a bug, it creates a log file that is stored locally and displays a windows toast message to the user. Then, it attempts to send an email containing the contents of the log file to all recipients in the `EMAILS` list. 
