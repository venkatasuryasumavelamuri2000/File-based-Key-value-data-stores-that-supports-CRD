# Python program to create a 
# GUI Key Store information 


import tkinter as tk 
from tkinter import messagebox
from tkinter import filedialog
import csv
import datetime
import time
import os
import json
import sys

'''
*******************************************************************
Script workflow:
GUI form presented to fill in Key Store details
1-Input fields are stored in a file. JSON format is used to store data.
File Name Convention:keyStoreDataFile_1.txt
2-Functions provided are Create, View and Delete
3-On 'Time to Live' expiration Key becomes Inactive & cannot be retreived
4.Once a file reaches 1 GB, another file gets created
*******************************************************************
'''

# creating a new tkinter window 
master = tk.Tk() 

# assigning a title 
master.title("Key Store Form") 

# specifying geomtery for window size 
master.geometry("800x700") 


# declaring objects for entering data 
txtImportFile = tk.Entry(master)
txtKey = tk.Entry(master) 
txtKeyValue = tk.Entry(master) 
txtTimeToLive = tk.Entry(master)
txtDisplay = tk.Entry(master) 

json_data = tk.Entry(master)

#Set default file to current directory with default file name
rootDir = os.getcwd()
txtImportFile.delete(0,tk.END)
txtImportFile.insert(tk.END,rootDir+"/keyStoreFile-1.json")


# Browse File to Import
def browseFile(): 
    print('browseFile START *************')
    rootDir = os.getcwd()

    fileName = filedialog.askopenfilename(initialdir = rootDir,title = 'Select a File',filetypes = (("all files","*.*"), ("csv files","*.csv")))
    if fileName != '':
        print("Input file selected: {}".format(fileName))
        txtImportFile.delete(0,tk.END)
        txtImportFile.insert(tk.END,fileName)
        file_size=os.path.getsize(fileName)
        print("Input file Size: {}".format(file_size))
    else:
        print("File is not selected: {}".format(fileName))

    #Call cleanup on file select
    try:
      key_cleanup(fileName)
      print('browseFile END *************')
    except:
      msg="Exception in key_cleanup"

# end of browseFile function 

# validateForm 
def validateForm(): 
    input_File = txtImportFile.get()
    input_Key = txtKey.get()
    input_KeyValue = txtKeyValue.get()
    input_TimeToLive = txtTimeToLive.get()

    # Check all fields required are filled in or not, proceed only when it is met
    if input_File == '' or input_Key == '' or input_KeyValue == '': 
      messagebox.showerror("Missing Fields", "Please enter all Fields")
      return
    b = input_Key.isalpha()
    if(not b):
        messagebox.showerror("Key Error", "Please enter only STRING")
        return
    if(input_TimeToLive!=''):
        b = input_TimeToLive.isdecimal()
        if(not b):
            messagebox.showerror("TimeToLive error", "Please enter only NUMBER")
            return
    k = len(input_Key)
    if(k>32):
        messagebox.showerror("KeyLen error", "Please enter only key less than 32Char")
        return
    k = sys.getsizeof(input_KeyValue)
    if(k>16000):
        messagebox.showerror("ValueSize error", "Please enter only value less than 16kb")
        return
    # Check file exists once again
    # Check Key length, TimeToLive is a digit

    if input_TimeToLive=='':
      input_TimeToLive = 24*60*60

    # call writeKey to write the key to the file
    writeKey(input_File,input_Key,input_KeyValue,input_TimeToLive)


# end of validateForm function 

# writeKey  
def writeKey(input_File,input_Key,input_KeyValue,input_TimeToLive): 
    print('writeKey START *************')

    print('File to Write='+input_File)
    
    found_Key = ''
    key_Record = ''

    try:

      found_Key,key_Record=searchKey(input_File,input_Key)

      if found_Key == "YES":
        txtDisplay.delete('1.0',tk.END)
        txtDisplay.insert(tk.END,"Key exists already as given below. Please provide new Key details."+"\n\n")
        txtDisplay.insert(tk.END,key_Record)
        found_Key = ''
        return

      dtNow = datetime.datetime.now().strftime("%m-%d-%y-%H%M")
      with open(input_File, "r") as read_file:

          json_data=json.load(read_file)
          print("************ JSON data AS IS************ ")
          print(json_data)

          temp=json_data['keys']
          rec_append = {"keyName":input_Key, 
                        "keyValue":input_KeyValue, 
                        "TimeToLive":input_TimeToLive, 
                        "keyCreatedTime":dtNow, 
                        "keyExpired":'N'
                       }
          temp.append(rec_append)

          print("************ Amended JSON data************ ")
          print(temp)

      with open(input_File, "w") as write_file:
          json.dump(json_data, write_file, indent=4)

      txtDisplay.delete('1.0',tk.END)
      txtDisplay.insert(tk.END,"Key Generated"+"\n\n")
      txtDisplay.insert(tk.END,rec_append)

    except:
        raise
        msg="Failed Writing Key to File"
        return False, msg

    print('writeKey END *************')

# end of writeKey function 

#searchKey
def searchKey(input_File,input_Key):
    print('searchKey START *************')
    found_Key=''
    key_Record=''
    try:
      with open(input_File, "r") as read_file:

          json_data=json.load(read_file)
          temp=json_data['keys']

          for key_record in temp:
            if input_Key == key_record['keyName']:
              found_Key="YES"
              key_Record=key_record
              #return found_Key, key_Record

          print('searchKey END RETURNS *************')
          return found_Key, key_Record         

    except:
        raise
        msg="Failed Reading File"
        print("searchKey EXCEPTION="+msg)
        return False, msg

# end of searchKey function

# viewKey  
def viewKey(): 
    print('viewKey START *************')
    input_File = txtImportFile.get()
    input_Key = txtKey.get()
    if input_Key == '': 
           messagebox.showerror("Missing Field", "Please enter Key to view")
           return
    found_Key=''
    try:
      with open(input_File, "r") as read_file:

          json_data=json.load(read_file)
          temp=json_data['keys']
          print(temp)

          for key_record in temp:
            if input_Key == key_record['keyName']:
              found_Key="YES"
              print(key_record)
              txtDisplay.delete('1.0',tk.END)
              txtDisplay.insert(tk.END,key_record)


          if(found_Key == ''): 
              print(input_Key + " Key is not found. Please provide a valid Key")
              txtDisplay.delete('1.0',tk.END)
              txtDisplay.insert(tk.END,input_Key + " Key is not found. Please provide a valid Key.")

           
    except:
        raise
        msg="Failed Reading File"
        print(msg)
        return False, msg
    print('viewKey END *************')

# end of viewKey function 

# deleteKey  
def deleteKey(): 
    print('deleteKey START *************')
    input_File = txtImportFile.get()
    input_Key = txtKey.get()
    if input_Key == '': 
           messagebox.showerror("Missing Field", "Please enter Key to Delete")
           return

    found_Key = ''
    key_Record = ''

    try:

      found_Key,key_Record=searchKey(input_File,input_Key)
      if found_Key == '':
        txtDisplay.delete('1.0',tk.END)
        txtDisplay.insert(tk.END,input_Key + " Key is not found. Please provide a valid Key to Delete.")
        found_Key = ''
        return
      else:
        with open(input_File, "r") as read_file:
          json_data = json.load(read_file)  
        object_to_delete = next(
           (item for item in json_data['keys'] if item['keyName'] == input_Key and item['keyExpired'] == 'N'), None)
        if object_to_delete is not None:
           object_to_delete['keyExpired'] = 'Y'
        
        with open(input_File, 'w') as json_file:
          json.dump(json_data, json_file, indent=4)

        txtDisplay.delete('1.0',tk.END)
        txtDisplay.insert(tk.END,input_Key + " Key deleted successfully.")

      print('deleteKey END *************')
    except:
        raise
        msg="Failed Deleting Key"
        print(msg)
        return False, msg
# end of deleteKey function 

# key_cleanup 
def key_cleanup(file_path):
    print('key_cleanup START *************')
    print('file_path='+file_path)
    with open(file_path) as json_file:
        json_data = json.load(json_file)

    for obj in json_data['keys']:
        if obj['keyExpired'] == 'Y':
            continue
        expire_date = datetime.datetime.strptime(
            obj['keyCreatedTime'], '%m-%d-%y-%H%M') + datetime.timedelta(0, int(obj['TimeToLive']))

        if expire_date < datetime.datetime.now():
            obj['keyExpired'] = 'Y'

    with open(file_path, 'w') as json_file:
        json.dump(json_data, json_file, indent=4)

    json_file.close()
    print('key_cleanup END *************')

# end of key_cleanup function 

#Form Starts here

rowNumber=0
# label for Title
tk.Label(master, text="Key Store Form").grid(row=rowNumber+0, column=0) 

rowNumber=1
tk.Label(master, text="File").grid(row=rowNumber, column=0) 
txtImportFile.grid(row=rowNumber, column=1) 
btnBrowseFile=tk.Button(master, text="Browse a File", bg="grey", command=browseFile) 
btnBrowseFile.grid(row=rowNumber, column=2) 

rowNumber=2
# label to enter Partition, DNS Alias, Service Port 
tk.Label(master, text="Key").grid(row=rowNumber, column=0) 
txtKey.grid(row=rowNumber, column=1) 

tk.Label(master, text="Value").grid(row=rowNumber, column=2) 
txtKeyValue.grid(row=rowNumber, column=3) 

tk.Label(master, text="Time To Live (sec)").grid(row=rowNumber, column=4) 
txtTimeToLive.grid(row=rowNumber, column=5) 

rowNumber=5

btnCreateKey=tk.Button(master, text="Create Key", bg="grey", command=validateForm) 
btnCreateKey.grid(row=rowNumber, column=1) 

btnViewKey=tk.Button(master, text="View Key", bg="grey", command=viewKey) 
btnViewKey.grid(row=rowNumber, column=2)

btnDeleteKey=tk.Button(master, text="Delete Key", bg="grey", command=deleteKey) 
btnDeleteKey.grid(row=rowNumber, column=3)
	

rowNumber=10
#txtDisplay.grid(row=rowNumber+10, column=1, columnspan = 4,sticky = tk.W+tk.E) 
xScroll = tk.Scrollbar(master,orient = tk.HORIZONTAL)
xScroll.grid(row = rowNumber+4, column = 1, columnspan = 5,sticky = tk.W+tk.E)
yScroll =  tk.Scrollbar(master, orient = tk.VERTICAL)
yScroll.grid(row = rowNumber+3, column = 5,sticky = tk.N+tk.S+tk.W)
txtDisplay = tk.Text(master,height = 5,xscrollcommand =xScroll.set,yscrollcommand = yScroll.set)
txtDisplay.grid(row = rowNumber+3,column = 1,columnspan = 5,sticky = tk.W+tk.E)
xScroll.config(command = txtDisplay.xview)
yScroll.config(command = txtDisplay.yview)     


master.mainloop() 

#Form Ends here

