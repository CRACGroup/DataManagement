#####################################################################
### This is the CRAC server script to grab data from workstations
### Created and maintained by Mixtli Campos
### github.com/mixtli-c
###
### IMPORTANT:
### Function GetData not 100% tested, check comments within code
###
###
#####################################################################



import numpy as np
import pandas as pd 
import datetime as dt
import os
import glob
import h5py
import paramiko


def ConcileTree(dots,localpath,remfolders):
    """
    This function compares local and remote
    trees at a specific level and makes
    local folders accordingly
    """
    # Comparing instrument folders and making new folders if
    # ... necessary
    locfolders = []
    for folder in (entry for entry in
            os.scandir(path=localpath) if entry.is_dir()):
        locfolders.append(folder.name)
    print(dots,"...Found local: ", locfolders)
    setlocal = set(locfolders)
    setremote = set(remfolders)
    setdiff = setremote.difference(setlocal)

    if not setdiff:
        print(dots,"No new folders.")
    else:
        print(dots,"New folders found: ", setdiff)
    
    for dirname in setdiff:
        os.mkdir(os.path.join(localpath,dirname))
        print(dots,"...Created new folder: ",
                dirname)


def GetData(workstation):
    """
    This function gets instrument info and data
    Connects via paramiko using input list
    Grabs a file with instrument names
    Then compares instrument structure
    Then grabs files
    """
    # Connects to SSH via paramiko
    print("Connecting to workstation: ", workstation[1])
    client = paramiko.SSHClient()
    client.load_system_host_keys()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy)
    client.connect(workstation[0],username = workstation[1])
    
    # Transfers from RootData/Instruments with SFTP
    print("...Getting instruments file.")
    instrumentdir = os.path.join(workstation[2],'Instruments')
    instrumentfile = os.path.join(workstation[2],'Instruments',
            'inst_names.txt')
    localinst = os.path.join('/home/anton/CRAC/Data/',workstation[1],
            'Instruments')
    sftp = client.open_sftp()
    sftp.get(instrumentfile,os.path.join(localinst,'inst_names.txt'))
    
    # Get instrument names and type of collection from file 
    print("...Parsing information from instruments file.")
    instnames = []
    with open(os.path.join(localinst,'inst_names.txt'), 'r') as names:
        for name in names:
            n = name.strip('\n')
            instnames.append(n)
    print("......Found remote instruments: ", instnames)

    # Reconcile the tree at the workstation level (instrument folders)
    ConcileTree('......',localinst,instnames)

    # Get all the new Data
    print("...Getting data...")
    ## Maybe at some point this can be done with regex
    for inst in instnames:

        print("......Looking at instrument: ", inst)
        
        # local and remote instrument folder path
        locinstdir = os.path.join(localinst,inst)
        reminstdir = os.path.join(instrumentdir,inst)
        
        # get instrument folder root files
        if workstation[3] == 'W':
            cmmd = 'dir ' + workstation[2] + 'Instruments\\' + \
                    inst + ' /b /a:-d'

        ######################################################            
        if workstation[3] == 'L': ##### NEED TO CHECK THIS ONE
            cmmd = 'find ' + reminstdir + \
                ' -maxdepth 1 -type f -printf %f'
        ######################################################
        
        stdin, stdout, stderr = client.exec_command(cmmd)
        remoterootfiles = []
        for line in stdout:
            remoterootfiles.append(line.rstrip())
        print(".........",len(remoterootfiles)," instrument root files found.")
        
        for rootfile in remoterootfiles:
            print(".........Now trying to copy: ",rootfile)
            try:
                sftp.get(os.path.join(reminstdir,rootfile),
                    os.path.join(locinstdir,rootfile))
            except:
                print('............There was an error trying to copy ',
                    rootfile)
    
        # get folder names from remote
        if workstation[3] == 'W':
            cmmd = 'dir ' + workstation[2] + 'Instruments\\' + \
                    inst + ' /b /a:d'

        ######################################################            
        if workstation[3] == 'L': ##### NEED TO CHECK THIS ONE
            cmmd = 'find ' + reminstdir + \
                ' -maxdepth 1 -type d -printf %f'
        ######################################################
        
        stdin, stdout, stderr = client.exec_command(cmmd)
        remotefolders = []
        for line in stdout:
            remotefolders.append(line.rstrip())
        print(".........Finding remote folders: ",remotefolders)
        
        # Reconcile the three at the instrument level (data folders)
        ConcileTree('.........',locinstdir,remotefolders)

        # recursively sftp from every folder
        for foldername in remotefolders:

            print('.........Now working on folder: ',foldername)
        
            # local and remote data folder path
            locdatafolder = os.path.join(locinstdir,foldername)
            remdatafolder = os.path.join(reminstdir,foldername)
            
            # list files in remote folder
            remfiles = sftp.listdir(path=remdatafolder)
            print('.........',len(remfiles)," remote files found.")

            # list files in local folder
            locfiles = [] 
            for element in (entry for entry in 
                    os.scandir(path=locdatafolder) if entry.is_file()):
                locfiles.append(element.name)
            print('.........',len(locfiles)," local files found.")
            setlocalfiles = set(locfiles)
            setremotefiles = set(remfiles)
            setdifffiles = setremotefiles.difference(setlocalfiles)

            if not setdifffiles:
                print('.........',"No new files.")
            else:
                print('.........',len(setdifffiles)," new files found.")
            
            #copy them all
            for datafile in setdifffiles:
                print("............Now trying to copy: ",datafile)
                try:
                    sftp.get(os.path.join(remdatafolder,datafile),
                            os.path.join(locdatafolder,datafile))
                except:
                    print('...............There was an error trying to copy ',
                            datafile)
    
    print("Closing connection to workstation: ", workstation[1])
    # Close SFTP and SSH
    sftp.close()
    client.close()
    
def FileName_Builder(rules):
    """
    This function grabs some rules and constructs filenames
    """
    return namelist

def Hierarchy_Reader():
    """
    """

def Attribute_Reader():
    """
    """

def Flag_Reader():
    """
    """
    
def Metadata_Decoder():
    """
    This function opens the metadata file and decodes the information
    to locate and structure variables
    """
    #How do we know where the metadata files are located ?

### Name of the file with ID and path to root data folder
print("Loading locations file.")
locationsfile = '/home/anton/CRAC/Data/locations.txt'
workstation_info = []

### Need the login information and location at data computers
with open(locationsfile, 'r') as locations:
    for line in locations:
        l = line.strip('\n')
        workstation_info.append(l.split())
print("Locations file loaded.")
print("Getting files from workstations.")
for workstation in workstation_info:
    try:
        GetData(workstation)
    except Exception as e:
        print('Unable to connect to', workstation[1], 
                'due to the following error:')
        print(e)
        pass

print("Writing to log file.")
timestamp = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
output_log = "Script ran on: " + timestamp + '\n'
with open("/home/anton/CRAC/Data/collection.log","a") as file:
    file.write(output_log)
        
