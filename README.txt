The Key Store Python program is a file based key-value data store program with User Interface for the user to operate. It supports Create, View, Delete functionalities. 

Functionalities provided:
1. Provides User Interface for all the functionalities
2. New key value pair can be added. key cannot be more than 32 chars
3. Time to live defaults to 1 day (86400 seconds) on creation. It is an optional field in the UI.
4. Any Key existing, can be viewed and deleted
5. Delete marks the Key to be Inactive i.e. KeyExpired to "Y". On Creation, the value is "N"
6. All operations (Create, View, Delete) are visible in the intuitive UI.
7. On Browse feature in the UI, the program marks all the elapsed records (Time to live expired)
8. Optionally, separate program "job.py" is given which can be run independently that marks all the elapsed records to be inactive.

The only pre-requisite for the program is - Program expects a default JSON data file named "keyStoreFile-1.json" with empty JSON structure to start with.
Note: It stores  and manages the data in the directory where python program is running (default).However, user can change the file by using the Browse functionality given. 

Python version: 3.0 and above
Utilizes TkInter UI modules

