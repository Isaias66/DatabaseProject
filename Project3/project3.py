"""
CS-482
Authors: Miguel Fernandez, Camika Leiva, Isaias Melendez
11-18-22

Version: Python 3.10.2

Purpose: To demonstrate a user friendly interface within a command line to allow a user to manipulate
         and make changes to a database. This program will prompt the user for their host name, username,
         password, and the database they wish to acccess. After a connection has been made they will be
         provided a help list page of the different functionalites that this API offers. 

"""
import sys
import mysql.connector

#Establish database connection to cs482502, this is hardcoded in the program
#We also check if the connection failed to ensure that the program works and
#Prompt users to enter information through a command line interface
def Login():

    #Display basic cmd information for user to type in information
    print("Login: (Note: Type RESET in order to return the start of the login")
    hostVar = input("Enter your host: ")
    if(hostVar == "RESET"):
        Login()
    userVar = input("Enter your username: ")
    if(userVar == "RESET"):
        Login()
    passwdVar = input("Enter your password: ")
    if(passwdVar == "RESET"):
        Login()
    dataVar = input("Enter the name of the database you want to use: ")
    if(dataVar == "RESET"):
        Login()

    #Check if the connection was successful
    global mydb
    mydb = mysql.connector.connect(
        host = hostVar,
        user = userVar,
        password = passwdVar,
        database = dataVar
    )        

    #DB connection was successful so we may create a cursor
    if(mydb.is_connected()):
        print("Great, you are connected!")
        global mycursor
        mycursor = mydb.cursor()
        
    #Else the credentials were incorrect and we redirect back to the login page
    else:
        print("We believed you typed something wrong, try again.")
        Login()


#@Param: None
#@Output: All Display Models with all their attributes listed
#         in a row format
def DisplayModel():

    sql = "SELECT * FROM Model;"

    mycursor.execute(sql)
    record = mycursor.fetchall()

    #Check if results exist for the given query
    if mycursor.rowcount == 0:
        print("No results found for given query\n")
    else:
        #Display information
        for row in record:
            print("ModelNo: ", row[0],)
            print("Width: ", row[1],)
            print("Height: ", row[2],)
            print("Weight: ", row[3],)
            print("Depth: ", row[4],)
            print("ScreenSize: ", row[5], "\n")


#@Param: None
#@Output: All Digital Displays with all their attributes listed
#         in a row format        
def Display():

    sql = "SELECT * FROM DigitalDisplay;"
    mycursor.execute(sql)
    record = mycursor.fetchall()

    #Check if results exist for the given query
    if mycursor.rowcount == 0:
        print("No results found for given query\n")
    else:
        #Display information
        for row in record:
            print("SerialNo: ", row[0],)
            print("SchedulerSys: ", row[1],)
            print("ModelNo: ", row[2], "\n")


#@Param: None
#@Output: All attribute information regarding
#         the specified scheduler system
def Search():

    param = input("Please enter the scheduler system you want to search with (either \"Random\", \"Smart\", or \"Virtue\" and without quotation marks): ")

    sql = "SELECT * FROM DigitalDisplay WHERE schedulerSystem = %s;"
    val = (param,)

    mycursor.execute(sql,val)
    record = mycursor.fetchall()

    #Check if results exist for given query
    if mycursor.rowcount == 0:
        print("No results found for given query\n")
    else:
        #Display information
        print("Systems with scheduler system \"" + param + "\":")
        for row in record:
            print("Serial No: ", row[0], )
            print("Model No: ", row[1])
            print("Technical Support Name: ", row[2], "\n")


#@Param: None
#@Output: All attribute information regarding
#         the specified DigitalDisplays after the insertion has occurred
def Insert():

    serialNo = input("Please input a serial number: ")
    scheduler = input("Please input the type of scheduler system (\"Random\", \"Smart\", or \"Virtue\" without quotation marks): ")
    modelNo = input("Please input an EXISITING model number to use: ")

    sql = ("INSERT INTO DigitalDisplay values(%s, %s, %s);")
    val = (serialNo, scheduler, modelNo)
    mycursor.execute(sql, val)    

    #We display the new changes made to the DB
    print("Digital Display has been successfully added!")
    Display()


#WIP  Integrity Error------------------------------------------------------------------------------------------------ 
def Delete():

    amount = 0
    modelNo = ""
    serialNo = input("Type in the serial number for your digital display would you like to be deleted: ")

    sql = "SELECT modelNo FROM DigitalDisplay WHERE serialNo = %s;"
    val = (serialNo,)

    mycursor.execute(sql,val)
    
    for row in mycursor:
        modelNo = row

    #print(modelNo[0])
    sql2 = "SELECT * FROM DigitalDisplay WHERE modelNo = %s;"
    val2 = (modelNo[0],)
    mycursor.execute(sql2,val2)

    for row in mycursor:
        amount = amount + 1
        
    sql4 = "DELETE FROM Locates WHERE serialNo = %s;"
    mycursor.execute(sql4, val)

    sql3 = "DELETE FROM DigitalDisplay WHERE serialNo = %s;"
    mycursor.execute(sql3,val)

    if(amount == 1):
        sql4 = "DELETE FROM Specializes WHERE modelNo = %s;"
        val4 = (modelNo[0],)
        mycursor.execute(sql4,val4)
        
        sql4 = "DELETE FROM Model WHERE modelNo = %s;"
        mycursor.execute(sql4,val4) 

    #Display results after deletion
    Display()
    DisplayModel()

#WIP (Integrity Error()----------------------------------------------------------------------------   
def Update():

    serialNo = input("Input the serial number of the digital display that you would like to update: ")
    newSerialNo = input("Input the new serial number (or type it again if it is not changing): ")
    newSchedule = input("Input the new scheduler system (or type it again if it is not changing): ")
    newModelNo = input("Input the new model number (or type it again if it is not changing): ")

    sql = "UPDATE DigitalDisplay SET serialNo = %s, schedulerSystem = %s, modelNo = %s WHERE serialNo = %s;"
    val = (newSerialNo, newSchedule, newModelNo, serialNo)
    mycursor.execute(sql,val)

    #Display changes to the DB
    Display()


#@Param: None
#@Output: The main login screen with prompts for credentials
def Logout():

    #Close the connection to the database
    if (mydb.is_connected()):
        mydb.close()
        print("MySQL connection is closed")
        
    print("You have been logged out and are being sent back to the login screen.")

    #Return back to login screen
    Login()


#Main function that handles and directs user to correct functions based on the input given on cmd
def main():

    Login()
    option = ""

    while(1):
        #Basic Help Information for User
        option = input("\n\nWelcome to your database!\nIn order to display all your devices, type \"Display\".\nIn order to display all your Display Models, type \"DisplayModel\".\nTo search digital displays given a scheduler system, type \"Search\".\nTo insert a new digital display, type \"Insert\".\nTo delete a digital display, type \"Delete\".\nTo update a digital display, type \"Update\".\nTo logout of your account, type \"Logout\".\n")

        #All different functions to handle the user input
        if(option == "Display"):
            Display()
        elif(option == "DisplayModel"):
            DisplayModel()
        elif(option == "Search"):
            Search()
        elif(option == "Insert"):
            Insert()
        elif(option == "Delete"):
            Delete()
        elif(option == "Update"):
            Update()
        elif(option == "Logout"):
            Logout()

        #If user input is not recognized then we prompt them to try again
        else:
            print("I'm sorry, but that command is not available, please try again.")
            
if __name__ == '__main__':
    main()
