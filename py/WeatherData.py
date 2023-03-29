### Process the logger files into a nice csv with a header. Copy files to Google Drive

import shutil
import csv
import datetime as dt

### The list of the data files, the header file, and the list of output files

loggerdatafile = [r'C:\Campbellsci\LoggerNet\CR1000_Table1.dat',
                  r'C:\Campbellsci\LoggerNet\CR1000_Table2.dat',
                  r'C:\Campbellsci\LoggerNet\CR1000_Table3_tmp.dat']
headerfile = r'weatherheader.txt'
dataname = [r'\UCCWeatherMast_Hourly.dat',r'\UCCWeatherMast_Daily.dat',r'\UCCWeatherMast_']
localpath = r'.\Data'
drivepath = r'G:\My Drive\Data'

### Data collection and copy
### This algorithm simply merges the hearder and headerless data
### Grabs header, grabs data lines from data (removes header) into temp file, merges text and writes new file
### Copy files with shutil inside of loop

for ii,ele in enumerate(loggerdatafile):
    with open(headerfile, "r") as f1:
        headertxt = f1.read()

    with open(loggerdatafile[ii], "r") as f1:
        data = f1.readlines()[4:]
        parseddata = []
        for line in data:
            line = line.strip('\n') ### take out newline character
            line = line.split(',') ### split the columns
            line[0] = line[0].strip('\"') ### take out the quotes out of the date
            parseddata.append(line)

    with open('tempdata.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(parseddata)
    
    with open('tempdata.csv', "r") as f1:
        data = f1.read()
    
    #### The last table is the minute data, since this is sent daily to MET Eireann
    #### We create individual daily files that are timestamped, then we have to change
    #### the name 
    
    if ii==2:
        daytime = dt.datetime.strptime(parseddata[100][0],'%Y-%m-%d %H:%M:%S')
        day = daytime.strftime('%Y%m%d')
        dataname[ii] = dataname[ii] +day+ r'.dat'
    #### 
    
    text = headertxt+'\n'+data

    with open (localpath+dataname[ii], 'w') as fp:
        fp.write(text)
    
    # copy files
    shutil.copyfile(localpath+dataname[ii], drivepath+dataname[ii])
### End of data collection and copy
