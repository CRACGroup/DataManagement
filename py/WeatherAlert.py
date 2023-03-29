###################
# NEW WEATHER ALERT SYSTEM
###################

import smtplib
import ssl
import time
import datetime as dt

################### FUNCTIONS
def send_emails(emails,message):
    """ This functions runs SMTPlib to send from
    uccweatheralert@outlook.com """
    port = 587  # For starttls
    smtp_server = "smtp.office365.com"
    sender_email = "...@outlook.com"
    password = "..."

    context = ssl.create_default_context()
    with smtplib.SMTP(smtp_server, port) as server:
        #server.ehlo()  # Can be omitted
        server.starttls(context=context)
        #server.ehlo()  # Can be omitted
        server.login(sender_email, password)
        for receiver_email in emails:
            try:
                server.sendmail(sender_email, receiver_email, message)
            except Exception as e:
                print('Error sending email ',receiver_email,
                      ' with following exception:')
                print(e)
                pass

def get_temps(loggerdatafile):
    """ This function gets temperatures from the logger, columns 5 and 7
    for air and ground, respectively.
    Converted to floats"""
    with open(loggerdatafile, "r") as f1:
        last_line = f1.readlines()[-1]
        last_line = last_line.strip('\n')
        last_line = last_line.split(',')
        T_g = float(last_line[6])
        T_a = float(last_line[4])
    return T_g,T_a
################### END OF FUNCTIONS

################### PARAMETERS
## Temperature
Tcold = 0.1  # Cold Threshold
Twarm = 2.0  # Warm Threshold

## Logger
loggerdatafile = r'C:\Campbellsci\LoggerNet\CR1000_Table3.dat' # Path and name of the minute data as raw string

## Emails
sendto = ["...", 
          "...",
          "...",
          "...",
          "...",
          "...",
          "..."]

sendtotest = ["..."] ### FOR TESTING

## Cold and Warm email messages
messagecold = """\
Subject: "Weather Alert: Ground temperature below 0C

UCC Weather Alert

A ground temperature of less than 0 C has been detected by the UCC weather station located in the UCC North Mall Campus.
A subsequent email will be sent once the ground temperature has risen above 2 C.

Please note: This is an automatically generated email, please do not reply to this message. 
For queries or more information please contact Andy Ruth at a.ruth@ucc.ie or Mixtli Campos at mcampos@ucc.ie

Location: 51deg 53' 58.1"N 8deg 29' 09.1"W"""

messagewarm = """\
Subject: Weather Alert UPDATE: Ground temperature above 2C

UCC Weather Alert - UPDATE

The UCC weather station, located in the UCC North Mall Campus, has detected that the ground temperature is currently at or above 2 C.

Please note: This is an automatically generated email, please do not reply to this message.
For queries or more information please contact Andy Ruth at a.ruth@ucc.ie or Mixtli Campos at mcampos@ucc.ie

Location: 51deg 53' 58.1"N 8deg 29' 09.1"W"""

## SYSTEM TEST EMAIL MESSAGES
messagecoldtest = """\
Subject: "SYSTEM TEST Weather Alert: Ground temperature below 0C

UCC Weather Alert - SYSTEM TEST

This is a test of the cold alert for the UCC Weather Mast 
Please note: This is an automatically generated email, please do not reply to this message. 
For queries or more information please contact Andy Ruth at a.ruth@ucc.ie or Mixtli Campos at mcampos@ucc.ie

Location: 51deg 53' 58.1"N 8deg 29' 09.1"W"""

messagewarmtest = """\
Subject: Weather Alert UPDATE: Ground temperature above 2C

UCC Weather Alert - UPDATE - SYSTEM TEST

This is a test of the warm alert for the UCC Weather Mast
Please note: This is an automatically generated email, please do not reply to this message.
For queries or more information please contact Andy Ruth at a.ruth@ucc.ie or Mixtli Campos at mcampos@ucc.ie

Location: 51deg 53' 58.1"N 8deg 29' 09.1"W"""
################### END OF PARAMETERS

################### ALGORITHM
### Two nested whiles, one is forever, the other while it's cold
while True:
    try:
        T_ground,T_air = get_temps(loggerdatafile)
        now = dt.datetime.now()
        print(now.strftime('%Y-%m-%d %H:%M:%S'))
        T_g_str = "Current ground temperature is %.2f C" %T_ground
        T_a_str = "Current air temperature is %.2f C" %T_air
        print(T_g_str,'\n'+T_a_str)

        ## for testing purposes only
        # sendmessagecoldtest = messagecoldtest+'\n'+T_g_str+'\n'+T_a_str
        # send_emails(sendtotest, sendmessagecoldtest)
        ## end of testing purposes block 
        
        if T_ground < Tcold :
            sendmessagecold = messagecold+"\n"+T_g_str+"\n"+T_a_str
            send_emails(sendto,sendmessagecold)
            y = True
            while y:
                time.sleep(600)
                try:
                    now = dt.datetime.now()
                    print(now.strftime('%Y-%m-%d %H:%M:%S'))
                    T_ground,T_air = get_temps(loggerdatafile)
                    T_g_str = "Current ground temperature is %.2f C" %T_ground
                    T_a_str = "Current air temperature is %.2f C" %T_air
                    print(T_g_str,'\n'+T_a_str)
                    
                    ## for testing purposes only
                    # sendmessagewarmtest = messagewarmtest+'\n'+T_g_str+'\n'+T_a_str
                    # send_emails(sendtotest, sendmessagecoldtest)
                    ## end of testing purposes block 
 
                    if T_ground > Twarm :
                        sendmessagewarm = messagewarm+"\n"+T_g_str+"\n"+T_a_str
                        send_emails(sendto,sendmessagewarm)
                        y = False
                except:
                    print("Cannot open file, retrying ... ")
                    time.sleep(5)
        time.sleep(600)
    except:
        print("Cannot open file, retrying ... ")
        time.sleep(5)
################### END ALGORITHM
