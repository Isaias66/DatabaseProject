"""
CS-482
Authors: Miguel Fernandez, Camika Leiva, Isaias Melendez
10-7-22

Version: Python 3.10.2

Purpose: This program will receive user input through the function main() parameters and display the
         correlated information depending on the values entered. This information will come from the
         database schema that was given in Project 1.

Pre-Conditions: 


Post-Conditions:


"""
import mysql.connector
import sys

#Establish database connection to cs482502
mydb = mysql.connector.connect(
    host = "localhost",
    user = "dbuser",
    passwd= "lwilldowell",
    database="cs482502"
    )

#@Param: A string variable containing a street name
#@Output: All sites that are on the given street, each
#        statement is printed on per line and contains all
#        attributes for the specified site
def queryOne(arg):
    mycursor = mydb.cursor()
    param = arg
    
    sql = "SELECT * FROM Site WHERE address like '%" + param + "%'"
    val = (param,)

    mycursor.execute(sql)
    record = mycursor.fetchall()

    for row in record:
        print("Site Code: ", row[0],)
        print("Type: ", row[1])
        print("Address: ", row[2])
        print("Phone No. : ", row[3], "\n")

    if (mydb.is_connected()):
        mydb.close()
        mycursor.close()
        print("MySQL connection is closed")


#@Param: A string variable containing a scheduler system
#@Output: 
def queryTwo(arg):
    mycursor = mydb.cursor()
    param = arg
    
    sql = "SELECT d.serialNo, d.modelNo, t.name FROM DigitalDisplay as d, Specializes as s, TechnicalSupport as t WHERE s.empId = t.empId and s.modelNo = d.modelNo and d.schedulerSystem = %s"
    val = (param,)

    mycursor.execute(sql,val)
    record = mycursor.fetchall()

    for row in record:
        print("Serial No: ", row[0], )
        print("Model No: ", row[1])
        print("Technical Support Name: ", row[2], "\n")

    if (mydb.is_connected()):
        mydb.close()
        mycursor.close()
        print("MySQL connection is closed")


#@Param: None
#@Output: 
def queryThree():
    mycursor = mydb.cursor()

    sql = "SELECT DISTINCT * FROM Salesman ORDER BY name asc;"  

    mycursor.execute(sql)

    #### WIP
    print("Name   cnt")
    print("-------------")

    record = mycursor.fetchall()
    
    for row in record:        
        print(row[1])

#@Param: 
#@Output:
def queryFour(arg):
    mycursor = mydb.cursor()
    param = arg
    
    sql = "SELECT * FROM Client WHERE phone = %s"
    val = (param,)

    mycursor.execute(sql,val)
    record = mycursor.fetchall()

    for row in record:
        print("clientID ", row[0], )
        print("Name: ", row[1])
        print("Phone: ", row[2])
        print("Address: ", row[3], "\n")

    if (mydb.is_connected()):
        mydb.close()
        mycursor.close()
        print("MySQL connection is closed")


#@Param: None
#@Output: 
def queryFive():
    mycursor = mydb.cursor()
    
    sql = "SELECT b.empId, b.name, a.hours FROM AdmWorkHours as a, Administrator as b WHERE a.empId = b.empId ORDER BY a.hours asc;"

    mycursor.execute(sql)
    record = mycursor.fetchall()

    # NOTE: I am unsure if this is the correct info for the total hours, this may need to be reviewed
    for row in record:
        print("EmpId: ", row[0], )
        print("Name: ", row[1])
        print("Hours: ", row[2], "\n")

    if (mydb.is_connected()):
        mydb.close()
        mycursor.close()
        print("MySQL connection is closed")   

#@Param: A model Number, string 
#@Output: The names of the technical supports who work on the specified model.
def querySix(arg):
    mycursor = mydb.cursor()
    param = arg
    
    sql = "SELECT t.name FROM TechnicalSupport as t, Specializes as s WHERE t.empId = s.empId and s.modelNo = %s;"
    val = (param,)

    mycursor.execute(sql,val)
    record = mycursor.fetchall()

    for row in record:
        print("Name of Tech. Support: ", row[0], "\n")

    if (mydb.is_connected()):
        mydb.close()
        mycursor.close()
        print("MySQL connection is closed")

#@Param: None
#@Output: 
def querySeven():
    mycursor = mydb.cursor()

    ##NOTE: WIP this is not the correct SQL statement
    sql = "SELECT s.name, avg(p.commissionRate) FROM Salesman as s, Purchases as p WHERE s.empId = p.empId ORDER BY p.commissionRate desc;"

    mycursor.execute(sql)
    record = mycursor.fetchall()

    # NOTE: The output is only one salesman which is not correct, WIP
    for row in record:
        print("Name: ", row[0], )
        print("Avg.CommisionRate: ", row[1], "\n")

    if (mydb.is_connected()):
        mydb.close()
        mycursor.close()
        print("MySQL connection is closed")   


#@Param: None
#@Output: 
def queryEight():
    mycursor = mydb.cursor()

    ##NOTE: WIP this is not the correct SQL statement
    sql = ""

    mycursor.execute(sql)
    record = mycursor.fetchall()

    # NOTE:WIP
    for row in record:
        print("")

    if (mydb.is_connected()):
        mydb.close()
        mycursor.close()
        print("MySQL connection is closed")   

def main():

    #This will ignore 'proj.py' and recognize the arugments given after
    #the python script 
    args = sys.argv[1:]

    #Question Num: 1
    if len(args) == 2 and args[0] == '1':
        queryOne(args[1])
        
    #Question Num: 2
    elif len(args) == 2 and args[0] == '2':
        queryTwo(args[1])
        
    #Question Num: 3
    elif len(args) == 1 and args[0] == '3':
        queryThree()
        
    #Question Num: 4
    elif len(args) == 2 and args[0] == '4':
        queryFour(args[1])

    #Question Num: 5
    elif len(args) == 1 and args[0] == '5':
        queryFive()

    #Question Num: 6
    elif len(args) == 2 and args[0] == '6':
        querySix(args[1])

    #Question Num: 7
    elif len(args) == 1 and args[0] == '7':
        querySeven()

    #Question Num: 8
    elif len(args) == 1 and args[0] == '8':
        queryEight()

    #No arguments were recieved
    elif len(args) == 0:
        print("No arguments were received")

    #Incorrect spelling or not a valid argument
    else:
        print("Not a valid command line argument")
    

if __name__ == "__main__":
    main()
