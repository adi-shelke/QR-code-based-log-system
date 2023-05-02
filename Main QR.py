
# try:
from importlib.resources import path
import time
from time import time
from unicodedata import name
import cv2
from django.db import connection
import numpy as num
from pygame import Cursor
from pyzbar.pyzbar import decode
import qrcode
import mysql.connector
import datetime
from multiprocessing import Process
import os

# FOR VOICE ACKNOWLEDGEMENT
import pyttsx3

# FOR GUI (TKINTER)
from re import T
import tkinter as tk

# FOR MAKING A WINDOW
                                        # CONNECTION TO DATABASE 


conn = mysql.connector.connect(user='root', password='', host='127.0.0.1',database='attendance')
# print(conn)




                                    # BUILDING THE SPEAKING ABILITY

                                    # INITIALIZING SPEAK FUNCTION 

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice',voices[0].id)
engine.setProperty('rate',150)

                                    # DEFINING SPEAK FUNCTION
def speak(audio):
    engine.say(audio)
    engine.runAndWait()

global img


                                        # CHECKING THE DATE AND TIME


cam = cv2.VideoCapture(0,cv2.CAP_DSHOW)


# Checking if the folder exists or not 



                                
                                            # GENAERATING QR CODES
def generate():
    userInfo= input("Enter Name Surname and Roll Number seperated by spaces ")
    img = qrcode.make(userInfo)
    userInfo=str(userInfo)
    userInfo = userInfo.split()
    qrName= userInfo[0]+" "+userInfo[1]
    img_name=str(qrName)+"" ".jpg"
    img.save(f'qrCodes/{img_name}')

    return
    

                            # OPENING CAMERA AND DETECTING QR AND MAKING ENTRY
def scan():
    try:
        while True:
            now = datetime.datetime.now()
            date = now.strftime("%y-%m-%d")
            date = "20"+date
            time= now.strftime("%H:%M:%S")
            HoursminNow=now.strftime("%H:%M:%S")
            dateNow=date
            # print(dateNow)

            ret, img = cam.read()
            cv2.imshow('result',img)
            key = cv2.waitKey(1) %0x100
            if key==27 or key ==10:
                cv2.destroyAllWindows()
                break


            for qr in decode(img):
                info = qr.data.decode('utf-8')
                info= info.split()
                name=info[0]+" "+info[1]
                rollNumber=info[2]
                lastDate= f'select date from attendance_entry WHERE roll="{rollNumber}" ORDER BY date DESC LIMIT 1'
                cursor=conn.cursor()
                cursor.execute(lastDate)
                lastDate=cursor.fetchone()
                if not lastDate:
                    entry_string=f'insert into attendance_entry (roll,name,date,time,status) values ("{rollNumber}","{name}","{date}","{time}","enter")'
                    cursor.execute(entry_string)
                    conn.commit()
                    print(name)
                    speak(name)
                else:
                    lastDate=lastDate[0]
                    lastDate=str(lastDate)
                    dateNow=str(dateNow)
                    if lastDate!=dateNow:
                        # print(" In No equal date")
                        entry_string=f'insert into attendance_entry (roll,name,date,time,status) values ("{rollNumber}","{name}","{date}","{time}","enter")'
                        cursor.execute(entry_string)
                        conn.commit()
                        print(name)
                        speak(name)



                    else:
                        # print("In equal date")
                        query = 'select * from attendance_entry where roll=''"'+rollNumber+'"'' and date= "'+date+'"'
                        # print(str)
                        cursor2=conn.cursor()
                        cursor2.execute(query)
                        records = cursor2.fetchall()
                        if cursor2.rowcount%2==0:
                            # print("In even records")
                            # lastScan = f'select date_format(time,"%H:%i") from attendance_entry WHERE name="{info}" ORDER BY time DESC LIMIT 1'
                            lastScan = f'select time from attendance_entry WHERE roll="{rollNumber}" and date="{date}" ORDER BY time DESC LIMIT 1'
                            # print(lastScan)
                            cursor2.execute(lastScan)
                            records=cursor2.fetchone()
                            if not records:
                                # print(info)
                                # print("In no records")
                                entry_string=f'insert into attendance_entry (roll,name,date,time,status) values ("{rollNumber}","{name}","{date}","{time}","enter")'
                                cursor2.execute(entry_string)
                                conn.commit()
                                print(name)
                                speak(name)
                            else:
                                # print("Have recordds")
                                lastTime=records[0]
                                n=2
                                lastTime=lastTime+datetime.timedelta(minutes=n)
                                lastTime=str(lastTime)
                                # print("lasttime",lastTime)
                                # print("timenow",HoursminNow)
                                # print(info)
                                if HoursminNow>lastTime:
                                    # print("in even no equal time")
                                    # print(info)
                                    entry_string=f'insert into attendance_entry (roll,name,date,time,status) values ("{rollNumber}","{name}","{date}","{time}","enter")'
                                    cursor2.execute(entry_string)
                                    conn.commit()
                                    print(name)
                                    speak(name)
                        else:
                            # print("In odd")
                            # print(info)
                            # lastScan = f'select date_format(time,"%H:%i") from attendance_entry WHERE name="{info}" ORDER BY time DESC LIMIT 1'
                            # lastDate = f'select date from attendance_entry WHERE name="{info}" ORDER BY time DESC LIMIT 1'
                            lastScan = f'select time from attendance_entry WHERE roll="{rollNumber}" and date="{date}"ORDER BY time DESC LIMIT 1'
                            cursor2.execute(lastScan)
                            records=cursor2.fetchone()
                            lastTime=records[0]
                            n=2
                            lastTime=lastTime+datetime.timedelta(minutes=n)
                            lastTime=str(lastTime)
                            # print("lasttime",lastTime)
                            # print("timenow",HoursminNow)
                            # print(lastTime)
                            if HoursminNow>lastTime:
                                # print(info)
                                # print("In odd no equal time")
                                entry_string=f'insert into attendance_entry (roll,name,date,time,status) values ("{rollNumber}","{name}","{date}","{time}","exit")'
                                cursor2.execute(entry_string)
                                conn.commit()
                                print(name)
                                speak(name)


                points = num.array([qr.polygon],num.int32)
                points = points.reshape((-1,1,2))
                cv2.polylines(img,[points],True,(255,255,0),3)
                
    except:
        print("Error Occured While scanning QR")
        scan()

                                    # CHECHKING THE ENTRIES


                                    #CHECKING ONE DAY ENTRY
def checkOneDayEntry():
    print("")
    print("")
    print("Enter Roll Number  ", end="")
    userRoll = input()
    print("Enter The Intended Date In YYYY-MM-DD  ",end="")
    date = input()
    print("")
    print("")

    query=f'Select * from attendance_entry where roll="{userRoll}" and date="{date}"'
    cursor=conn.cursor()
    cursor.execute(query)
    records=cursor.fetchall()
    print("")
    print("")
    print(" Time        Status")
    print("")
    for row in records:
        print(row[3],end="      ")
        print(row[4])

        


    print("")
    print("")
                                # CHECKING ALL ENTRIES OF A PERSON 

def checkAllEntries():
    print("")
    print("")

    print("Enter Roll Number  ", end="")
    userRoll=input()
    print("")
    print("")

    
    query=f'Select * from attendance_entry where roll="{userRoll}"'
    cursor=conn.cursor()
    cursor.execute(query)
    records=cursor.fetchall()
    print("")
    print("")
    print("     Name                      Date                  Time                Status")
    print("")
    for row in records:
        print(row[1],end="              ")
        print(row[2],end="          ")
        print("   ",row[3],end="          ")
        print("    ",row[4])

    print("")
    print("")
        



    



def checkStatus():
    while True:
        print("")
        print("")
        print("1. Check Specific Day Entries Of a Person")
        print("2. Show All Enties Of a Specific Person")
        print("3. Return To Main Menu")
        print("")

        user_choice=int(input("Choose Your Option  ")) 

        if user_choice==1:
            checkOneDayEntry()
        elif user_choice==2:
            checkAllEntries()
        elif user_choice==3:
            break


                                    # DEFINING MAIN FUNCTION 




def main():
    folderPath="qrCodes"
    isExist = os.path.exists(folderPath)
    # print(isExist)
    if not isExist:
        os.mkdir(folderPath)
    while True:
        print("")
        print("")
        print("1. Generate QR Code")
        print("2. Take Entries")
        print("3. Check Status")
        print("4. Exit")
        print("")
        
        user_choice = int(input("Enter your choice  "))

        if user_choice==1:
            generate()
        if user_choice==2:
            scan()
        if user_choice==3:
            checkStatus()
        if user_choice==4:
            break

if __name__=="__main__":
    main() 
# except:
#     print("Something Wrong")


