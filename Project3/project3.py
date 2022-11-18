import sys
import mysql.connector

def DisplayModel():
    print("The format for models is: (modelNo, width, height, weight, depth, screenSize)")
    print("-----------------------------------------------------------------------------")
    mycursor.execute("SELECT * FROM Model;")
    for x in mycursor:
        print(x)

def Login():
    print("Login:")
    hostVar = input("Enter your host: ")
    userVar = input("Enter your username: ")
    passwdVar = input("Enter your password: ")
    dataVar = input("Enter the name of the database you want to use: ")
    global mydb
    mydb = mysql.connector.connect(
        host = hostVar,
        user = userVar,
        password = passwdVar,
        database = dataVar
    )
    
    if(mydb.is_connected()):
        print("Great, you are connected!")
        global mycursor
        mycursor = mydb.cursor()
    else:
        print("We believed you typed something wrong, try again.")
        login()

def Display():
    mycursor.execute("SELECT * FROM DigitalDisplay;")
    print("The format is: (serialNo, schedulerSystem, modelNo)")
    print("---------------------------------------------------")
    for x in mycursor:
      print(x)
    
def Search():
    search = input("Please enter the scheduler system you want to search with (either \"Random\", \"Smart\", or \"Virtue\" and without quotation marks): ")
    mycursor.execute("SELECT * FROM DigitalDisplay WHERE schedulerSystem = \"" + search + "\";")
    print("Systems with scheduler system \"" + search + "\":")
    for x in mycursor:
      print(x)
    
def Insert():
    serialNo = input("Please input a serial number: ")
    scheduler = input("Please input the type of scheduler system (\"Random\", \"Smart\", or \"Virtue\" without quotation marks): ")
    modelNo = input("Please input an existing model number to use: ")
    mycursor.execute("INSERT INTO DigitalDisplay values(\"" + serialNo + "\", \"" + scheduler + "\", \"" + modelNo + "\");")
    print("Digital Display has been successfully added!")
    Display()
    
def Delete():
    amount = 0
    modelNo = ""
    serialNo = input("Type in the serial number for your digital device would you like to be deleted: ")
    mycursor.execute("SELECT modelNo FROM DigitalDisplay WHERE serialNo = \"" + serialNo + "\";")
    for x in mycursor:
        modelNo = x
    print(modelNo[0])
    mycursor.execute("SELECT * FROM DigitalDisplay WHERE modelNo = \"" + modelNo[0] + "\";")
    for x in mycursor:
        temp = x
        amount = amount + 1
    mycursor.execute("DELETE FROM DigitalDisplay WHERE serialNo = \"" + serialNo + "\";")
    if(amount == 1):
        mycursor.execute("DELETE FROM Model WHERE modelNo = \"" + modelNo[0] + "\";")
    Display()
    DisplayModel()
    
def Update():
    serialNo = input("Input the serial number of the digital display that you would like to update: ")
    newSerialNo = input("Input the new serial number (or type it again if it is not changing): ")
    newSchedule = input("Input the new scheduler system (or type it again if it is not changing): ")
    newModelNo = input("Input the new mdoel number (or type it again if it is not changing): ")
    mycursor.execute("UPDATE DigitalDisplay SET serialNo = \"" + newSerialNo + "\", schedulerSystem = \"" + newSchedule + "\", modelNo = \"" + newModelNo + "\" WHERE serialNo = \"" + serialNo + "\";")
    Display()
    
def Logout():
    mydb.close()
    print("You have been logged out and are being sent back to the login screen.")
    Login()

if __name__ == '__main__':
    Login()
    option = ""
    while(1):
        option = input("\n\nWelcome to your database!\nIn order to display all your devices, type \"Display\".\nTo search digital displays given a scheduler system, type \"Search\".\nTo insert a new digital display, type \"Insert\".\nTo delete a digital display, type \"Delete\".\nTo update a digital display, type \"Update\".\nTo logout of your account, type \"Logout\".\n")
        
        if(option == "Display"):
            Display()
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
        else:
            print("I'm sorry, but that command is not available, please try again.")
