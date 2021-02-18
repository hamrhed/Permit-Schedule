# #############################################################################
# SCRIPT - PYTHON
# NAME: Fay-Permit.py
# 
# AUTHOR:  	Don Garrison
# DATE:  	9/13/2020
# EMAIL: 	hamrhed@gmail.com
# 
# COMMENT:  Scrapes KY scheduling website, identifies available and schedulable timeslots, emails results (if available).
#
#
# TO ADD: <nothing at this time>
#
#  
# #############################################################################



import bs4 as bs
import requests
import datetime
import os
import smtplib

#Set Variables -- Alter dest to appropriate county web page
dest = "https://schedule.ky.gov/Booking.Web/Event/Book/308"
spotsAvailable = 0
numofdays = 0
numoftimeslots = 0
days=["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]

#Get Page Info
source = requests.get(dest)
soup = bs.BeautifulSoup(source.content, 'lxml')

#Count for List of List
for medias in (soup.find_all(class_="media")):
        for potentialdays in (medias.find_all(class_="media-left")):
                datetime_object = ((potentialdays.find("time", class_="icon")["datetime"]).split(" ")[0])
                downum = datetime.datetime.strptime(datetime_object, '%m/%d/%Y').weekday()
                dayofweek = (days[downum])
                numofdays += 1
                tempnumoftimeslots = 0
        for potentialtimes in (medias.find_all(class_="row")):
                for individualTimes in (potentialtimes.find_all(class_="instanceSelector")):
                        spotsAvailable = (individualTimes["data-capacity"])
                        tempnumoftimeslots += 1
                        if tempnumoftimeslots > numoftimeslots:
                                numoftimeslots = tempnumoftimeslots

#Create multidimentional List
ListOfTimeslots = [[0 for y in range(5)] for y in range(numoftimeslots * numofdays)]

DayCounter = 0
TimeslotCounter = 0

for medias in (soup.find_all(class_="media")):
        for potentialdays in (medias.find_all(class_="media-left")):
                datetime_object = ((potentialdays.find("time", class_="icon")["datetime"]).split(" ")[0])
                downum = datetime.datetime.strptime(datetime_object, '%m/%d/%Y').weekday()
                dayofweek = (days[downum])
        for potentialtimes in (medias.find_all(class_="row")):
                for individualTimes in (potentialtimes.find_all(class_="instanceSelector")):
                        spotsAvailable = (individualTimes["data-capacity"])
                        timeslotvalue = individualTimes.text
                        ListOfTimeslots[TimeslotCounter][0] = dayofweek
                        ListOfTimeslots[TimeslotCounter][1] = datetime_object #mm/dd/yyyy
                        ListOfTimeslots[TimeslotCounter][2] = timeslotvalue
                        ListOfTimeslots[TimeslotCounter][3] = spotsAvailable
                        ListOfTimeslots[TimeslotCounter][4] = "Good"
                        TimeslotCounter += 1
        DayCounter += 1

if os.path.exists("DrivingTest/Fay-Permit-temp.txt"):
        os.remove("DrivingTest/Fay-Permit-temp.txt")
f = open("DrivingTest/Fay-Permit-temp.txt","a")
f.write("\n\n")
f.write("Fayette County - Permit Registrations Available!!! \n")
f.write("\n")
f.write(dest + " \n")
f.write("\n")
f.write("Total number of days visible on the website: "+ str(numofdays))
f.write("\n\n")

f.write("DATE\t\tDAY\t\tTIMESLOT\tSEATS AVAIL\n")
f.write("-------------------------------------------------------------\n")

AreSpotsAvailable = "No"


for i in range(numoftimeslots * numofdays):
        if ((ListOfTimeslots[i][4] == "Good") and ((ListOfTimeslots[i][3] == "1") or (ListOfTimeslots[i][3] == "2"))):
                f.write(ListOfTimeslots[i][1] + "\t" + ListOfTimeslots[i][0] + "\t" + ListOfTimeslots[i][2] + "\t" + ListOfTimeslots[i][3] + "\n")
                AreSpotsAvailable = "Yes"



EmailEnabled = "Yes"

Recipients = ["_____ListOfRecipients___","_____SeparatedByCommas_____"]

if AreSpotsAvailable == "Yes" and EmailEnabled == "Yes":
        for dest in Recipients:
                f = open("DrivingTest/Fay-Permit-temp.txt","r")
                message = f.read()
                print ("Spots available")
                #email
                s = smtplib.SMTP('smtp.gmail.com', 587)
                s.starttls()
                s.login("_____SendingGmailAccount_____", "_____APIPASSWORD_____")
                s.sendmail("_____SendingGmailAccount_____", dest, message)
                s.quit()

print (str(datetime.datetime.now())+ "\tAvailable spots?: " + AreSpotsAvailable + "\tEmail Enabled?: " + EmailEnabled)

f.close()
g = open("DrivingTest/log.txt","a")
g.write("Fayette Co Permit - Run at: "+ str(datetime.datetime.now()) + "     - Any Spots Available?: " + AreSpotsAvailable + "\n")
g.close()
# print ("Total Number of Days visible on Website: "+ str(numofdays))
