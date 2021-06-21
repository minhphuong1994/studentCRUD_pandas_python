import pandas
from termcolor import colored
from pathlib import Path
import re
import datetime
import sys

string_check= re.compile('[@_!#$%^&*()<>?/\|}{~:]')   # String of special charcters 

def main():
    keepGoing = "yes"
    while (keepGoing == "yes"):
        print(colored("********* Welcome to student Menu *********", 'yellow'))
        print(colored("Enter: 1 for entering student record", 'blue'))
        print(colored("       2 for reading all student record", 'blue'))
        print(colored("       3 for sorting student record", 'blue'))
        print(colored("       4 for searching student record", 'blue'))
        print(colored("       5 for modifying student record", 'blue'))
        choice = int(input("Enter your choice ----> "))
        option(choice)
        keepGoing = input(colored("Do you want to do other option? (yes for continue):", 'magenta'))

#calling different functions according to user choice
def option(choice):
    if (choice == 1):
        writeData()
    elif (choice == 2):
        displayData()
    elif (choice == 3):
        sortData()
    elif (choice == 4):
        search()
    elif (choice == 5):
        modify()
    else:
        print(colored("******* Incorrect choice *********",'red'))

# function for writing data and validations checking
def writeData():
    studentID, studentFlag = isValidID()
    FirstName, firstNameFlag = isValidFirstName()
    LastName, lastNameFlag = isValidLastName()
    Major, majorFlag = isValidMajor()
    number, numberFlag = isValidContactNumber()
    GPA, gpaFlag = isValidGpa()
    DOB,DOBFlag = isValidDateOfBirth()  
    if( studentFlag and firstNameFlag and lastNameFlag and majorFlag and numberFlag and gpaFlag and DOBFlag ):
        writeIntoFile(studentID,FirstName,LastName,Major,number,GPA,DOB)

# checks whether an ID is valid or not
def isValidID():
    flag1 = False
    flag2 = False
    correctID = []

    while (flag1 == False or flag2 == False):
        ID = input(colored("Enter student ID ===> ",'blue'))
        if Path('student.txt').is_file():  # Checking unique if file exist
            ID, flag2 = isUniqueID(ID)
        if all(ID.isalnum() and not (ID.isspace()) and flag2 ==True and string_check.search(ID) == None for ID in ID):
            flag1 = True
        else:
            print(colored("------ ID must be alphanumeric, contains no space and special character ---------",'red'))

    correctID.append(ID);
    correctID.append(flag1)
    return correctID

# checks whether entered id is unique or not
def isUniqueID(ID):
    checkID = ID
    flag = False
    uniqueID = []

    df = read_data()
    while(flag == False):
        subDF = df[(df['StudentID'] == checkID )] #Looking for Student ID in df and assign to subDF
        if subDF.empty:
            flag = True
            uniqueID.append(checkID)
            uniqueID.append(flag)
        else:
            print(colored("---------- Record already exist ---------------",'red'))
            print(colored("Enter an unique ID",'red'))
            checkID = input(colored('Enter student ID ===> ','blue'))
    return uniqueID
 
# validation on First Name       
def isValidFirstName():
    flag = False
    correctFirstName = []
    while (flag == False):
        firstName = input(colored("Enter first name ===> ",'blue'))
        if all(firstName.isalpha() or firstName.isspace() for firstName in firstName):
            flag = True
            correctFirstName.append(firstName)
            correctFirstName.append(flag)
        else:
            print(colored(" ------------- First Name must be alphabets only ---------",'red'))
    return correctFirstName
    
# validation on Last Name
def isValidLastName():
    flag = False
    correctLastName = []
    while (flag == False):
        lastName = input(colored("Enter last name ===> ",'blue'))
        if all(lastName.isalpha() or lastName.isspace() for lastName in lastName):
            flag = True
            correctLastName.append(lastName)
            correctLastName.append(flag)
        else:
            print (colored("------------ Last Name must be alphabets only ------------",'red'))
    return correctLastName

# validation on major
def isValidMajor():
    flag = False
    correctMajor = []
    while (flag == False):
        major = input(colored("Enter major ===>",'blue'))
        if all(major.isalnum() or (major.isspace()) for major in major):
            flag = True 
            correctMajor.append(major)
            correctMajor.append(flag)
        else:
            print (colored("------- Major can be alpha numeric -------------",'red'))
    return correctMajor

# validation on contact number    
def isValidContactNumber():
    flag = False
    correctNumber = []
    constraint= "\w{3}-\w{3}-\w{4}" # setting string of phone format
    while (flag == False):
        phoneNumber = input(colored("Enter phone number in format '516-111-2222' ===> ",'blue'))
        if re.search(constraint, phoneNumber):
            flag = True
            correctNumber.append(phoneNumber)
            correctNumber.append(flag)
        else:
            print(colored("---------- Enter phone number in 516-111-2222 format only -------------",'red'))
    return correctNumber

# validation on gpa
def isValidGpa():
    flag = False
    correctGPA = []
    while (flag == False):
         gpa = input(colored("Enter GPA===> ",'blue'))  
         try:
             if "." in gpa or gpa.isdigit():
                 gpaValue = float(gpa)
                 flag = True
                 correctGPA.append(gpaValue)
                 correctGPA.append(flag)
             else: 
                 print (colored("----------------- GPA must be integer or float ------------",'red'))
         except:
             print(colored("---------- GPA must be integer or float ------------",'red'))
    return correctGPA

#validation on date of birth             
def isValidDateOfBirth():
    flag = False
    correctDateOfBirth = []
    while (flag == False):
        dateOfBirth = input(colored("Enter date of birth in format 'dd/mm/yy' : ",'blue'))
        try:
            day,month,year = dateOfBirth.split('/')
            isValidDate = True
            try :
                datetime.datetime(int(year),int(month),int(day))
            except ValueError :
                isValidDate = False
                print (colored("-------------- Enter date of birth in correct format ----------",'red'))
            if isValidDate== True:
                flag = True
                correctDateOfBirth.append(dateOfBirth)
                correctDateOfBirth.append(flag)
        except:
            print (colored("-------------- Enter date of birth in correct format ----------",'red'))
    return correctDateOfBirth

# writes student record into file        
def writeIntoFile(ID,firstName,lastName,major,phone,gpaValue,dateOfBirth):
    studentFile = open("student.txt", "a+");
    studentRecord = ID + ":" + firstName + ":" + lastName + ":" + major + ":" + phone + ":" + str(gpaValue) + ":" + dateOfBirth
    print(colored("******* Record Successfully Entered **********\n Record is ===> ",'green'))
    print(colored(studentRecord,'green'))
    studentFile.write(studentRecord + "\n")
    studentFile.close();

# function in order to display file data
def displayData():
    print(read_data().to_string(index=False)) #Hide row index in display

# read data from file and returns to displayData()
def read_data():
    try:
        df = pandas.read_csv('student.txt', delimiter=":",
                               names=('StudentID', 'FirstName', 'LastName', 'Major', 'Phone', 'GPA', 'DateOfBirth'))
    except FileNotFoundError:
        print(colored("---------------- File not found ---------------",'red'))
        sys.exit(1)
    else:
        df['StudentID'] = df['StudentID'].astype(str)
        df['FirstName'] = df['FirstName'].astype(str)
        df['LastName'] = df['LastName'].astype(str)
        df['Major'] = df['Major'].astype(str)
        df['Phone'] = df['Phone'].astype(str)
        df['GPA'] = df['GPA'].astype(float)
        df['DateOfBirth'] = df['DateOfBirth'].astype(str)
        return df

# sort student records and display
def sortData():
    check = False
    list_fields = []
    while check == False:
        count = 1
        print(colored("StudentID(1) - FirstName(2) - LastName(3) - Major(4) - Phone(5) - GPA(6) - DateOfBirth(7)",'blue'))
        print(colored("Example: enter-->2 3 4 for sorting by FirstName, LastName and Major",'blue'))
        list_fields = input("Please choose fields you want to sort: ").split(' ')
        for x in list_fields:
            if not x.isdigit() or int(x) < 1 or int(x) > 7:
                print(colored("-------- WRONG INPUT! Please enter again as the instruction shown ------",'red'))
                check = False
                break
            else:
                check = True

    count = 0
    for x in list_fields:
        if x == '1':
            list_fields[count] = 'StudentID'
        elif x == '2':
            list_fields[count] = 'FirstName'
        elif x == '3':
            list_fields[count] = 'LastName'
        elif x == '4':
            list_fields[count] = 'Major'
        elif x == '5':
            list_fields[count] = 'Phone'
        elif x == '6':
            list_fields[count] = 'GPA'
        elif x == '7':
            list_fields[count] = 'DateOfBirth'
        count += 1

    # Read data from text file to pandas DataFrame
    df = read_data()
    # Sort by fields stored in sortby variable and in Ascending order
    if df.empty:
        print("File is empty!!")
    else:
        df.sort_values(by=list_fields, axis=0, inplace=True)
    print(df.to_string(index=False))

# search a particular record from file
def search():
    list_search = []
    # Read data from text file to pandas DataFrame
    df = read_data()

    print(colored('******** PROVIDE YOUR SEARCH CONDITIONS ********','blue'))
    list_search.append(input("Input student ID (enter to skip): "))
    list_search.append(input("Input last name(enter to skip): "))
    list_search.append(input("Input major(enter to skip): "))
    if list_search[0] != '':
        subDF = df[(df['StudentID'] == list_search[0])] #Looking for Student ID in df and assign to subDF
    else:
        subDF = df

    if list_search[1] != '':
        subDF = subDF[subDF['LastName'] == list_search[1]]

    if list_search[2] != '':
        subDF = subDF[subDF['Major'] == list_search[2]]

    if subDF.empty:
        print(colored("No data matched!", 'cyan'))
    else:
        print(subDF.to_string(index=False))

# modifying instructions
def modify():
    # Read data from text file to pandas DataFrame
    df = read_data()
    check =0
    while check == 0:
        print(colored('******** PROVIDE STUDENT ID YOU WANT TO MODIFY ********', 'blue'))
        search = input("===> ")
        subDF = df[(df['StudentID'] == search)]

        if subDF.empty:
            print(colored('------------- No student is found -----------', 'red'))
        else:
            print(colored('The student you are going to modify is: ', 'blue'))
            print(subDF.to_string(index=False))
            check = 1

    choice = '0'
    if len(subDF.index) == 1:
        while choice not in {'1', '2'}: #Force user to input just 1 or 2
            print(colored('Choose one of these two options: Update(1) - Delete(2)', 'blue'))
            print(colored('Example: enter -->1 to change student info', 'blue'))
            choice = input('-->')
            if choice == '1':
                update(subDF)
            elif choice == '2':
                delete(subDF)
            else:
                print(colored('--------------- Wrong input --------------', 'red'))
    else:
        print(colored('----------- Can not modify multiple students a time -------------', 'red'))

# doing updations in file
def update(subDF):
    with open('student.txt', 'r') as file: #read all file for later use
        lines = file.readlines()
    print(colored('You can change any info except StudentID', 'blue'))
    changes = []
    changes.append(input("Change first name(enter to skip): "))
    changes.append(input("Change last name(enter to skip): "))
    changes.append(input("Change major (enter to skip): "))
    changes.append(input("Change phone(enter to skip): "))
    changes.append(input("Change GPA(enter to skip): "))
    changes.append(input("Change date of birth(enter to skip): "))

    studentRecord = str(subDF.iloc[0,0]) + ":" #Get studentID from dataframe and assign to studentRecord
    count =2
    n = len(changes)
    for i in changes:
        if i != '':
            studentRecord += i + ":"
        else:
            studentRecord += str(subDF.iloc[0,count-1]) + ":"

        if count == n+1: #Remove the last ":" in studentRecord string
            studentRecord = studentRecord[:-1]
            studentRecord += "\n"
        count += 1

    time = 0
    check = int(list(subDF.index)[0])
    with open('student.txt','w') as file: #Write the changed info back to the file
        for i in lines:
            if time != check:
                file.write(i)
            else:
                file.write(studentRecord)
            time += 1

    print(colored('Info changed sucessfully!', 'green'))


# delete a particular record from file
def delete(subDF):
    with open('student.txt', 'r') as file: #read all file for later use
        lines = file.readlines()

    time = 0
    check = int(list(subDF.index)[0])

    with open('student.txt','w') as file: #Write the info back to the same file
        for i in lines:
            if time != check:
                file.write(i)
            time += 1
    print(colored('Deleted the student info', 'green'))


main()