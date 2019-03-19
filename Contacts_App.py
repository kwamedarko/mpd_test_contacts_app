import datetime
import mysql.connector
from mysql.connector import Error
from mysql.connector import errorcode
connection_config_dict = {
        'user': 'root',
        'password': 'Passw0rd!',
        'host': 'localhost',
        'port':'33066',
        'database': 'mpg'
    }

print("")
print("Welcome To Kad Kontacts")
print("")
print("Type 'help' to get more info")
print("")

def contacts_help():
    print('''
This APP Creates, Edits, Deletes, Searches and Shows All Contacts in MySQL Database

Type \"Create\" to Into the Terminal to create or add a contact

Type \"Edit\" to Into the Terminal to edit or modify a selected contact

Type \"Delete\" to Into the Terminal to delete or remove a selected contact

Type \"Showall\" to Into the Terminal to show all available contact(s)

Type \"Search\" to Into the Terminal to search for available contact(s)

Type \"Quit\" to Into the Terminal to exit or quit application
'''
)


#Data validaion function to validate NAME
def validate_name(c_name):
    data_valid = False
    try:
        val = str(c_name)
        if val != "":
            data_valid = True
            return data_valid
        else:
            return data_valid   
    except ValueError:
        return data_valid

#Data validaion function to validate AGE/Int
def validate_int(c_age):
    data_valid = False
    try:
        val = int(c_age)
        if(val > 0):
            data_valid = True
            return data_valid
        else:
            return data_valid   
    except ValueError:
            return data_valid

#Data validaion function to validate Date of Birth
def validate_dob(c_dob):
    date_format = '%Y-%m-%d'
    data_valid = False
    try:
        date_obj = datetime.datetime.strptime(c_dob, date_format)
        data_valid = True
        return data_valid 
    except ValueError:
        return data_valid 

#Database Error handling function
def handle_error(err):
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Something is wrong with your user name or password")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("Database does not exist")
    else:
        print(err)

#This function when called will add a new record to the database
def createcontact():
    while True:
        print("")
        quit_param = input("Type \"quit\" to quit the Create Prompt or Leave Blank and \n\nPress the 'Enter' key to continue Creating new contacts: ").strip()
        if quit_param.lower() == "quit":
            print("")
            break        
        print("")
        
        while True:           
            contact_name = input("Enter Name: ").upper().strip()
            name_IsValid = validate_name(contact_name)
            if name_IsValid == True:
                break
            else:
                print("")
                print("Sorry, please provide a valid name, name must be strings")
                continue
        print("")

        
        while True:
            contact_age = input("Enter Age: ").strip()
            age_IsValid = validate_int(contact_age)
            if age_IsValid == True:
                break
            else:
                print("")
                print("Sorry, please provide a valid age, age must be a positive number")
                continue
        print("")

        
        while True:
            contact_birth_date = input("Enter Birth Date: ").strip()
            dob_IsValid = validate_dob(contact_birth_date)
            if dob_IsValid == True:
                break
            else:
                print("")
                print("Sorry, please provide a valid date of birth, date of birth format 'YYYY-MM-DD'")
                continue
        print("")
        print(f"Your Details Are Name:{contact_name}, Age:{contact_age}, Birth Date:{contact_birth_date} ")
        print("")
        confirm_entry = input("Are You Sure, You Want To Create the Above Contact? \n\nPlease Type 'Y' and Press 'Enter' key to Create/confirm or Leave Blank and Press Enter to Cancel: ")
        print("")
        if confirm_entry.lower() == "y":        
            try:
                #Connection to the mysql database and inserting record(contact) 
                conn = mysql.connector.connect(**connection_config_dict)
                mycursor = conn.cursor()
                sql = "INSERT INTO contacts (contact_name, contact_age,contact_dob) VALUES (%s,%s,%s)"
                val = (contact_name,contact_age,contact_birth_date)
                mycursor.execute(sql, val)
                conn.commit()
                row_id = mycursor.lastrowid
                print("1 record inserted, ID:", row_id)
                mycursor.execute("SELECT * FROM contacts WHERE contact_id = "+ str(row_id) +"")
                new_rec = mycursor.fetchone()
                print("")
                print(new_rec)
                mycursor.close()
                conn.close()
            except mysql.connector.Error as err:
                handle_error(err)
            
        else:
            print("Contact creation cancelled by user")
    print("")   

#This function when called will retrieve a record to be edited 
#User will have to provide a Unique record ID or (contact_id)
def editcontact():
    while True:
        print("")
        quit_param = input("Type \"quit\" to quit the Edit Prompt or Leave Blank and \n\nPress 'Enter' key to continue to Edit other contacts: ").strip()
        if quit_param.lower() == "quit":
            print("")
            break       
        print("")
        #Get a user input of the contact ID of the  contact they want to edit
        contact_id = input("Enter Contact Id To Edit: ").strip()
        if validate_int(contact_id) == True:         
            try:
                conn = mysql.connector.connect(**connection_config_dict)
                mycursor = conn.cursor()
                sql_select = "SELECT * FROM contacts WHERE contact_id = '"+ contact_id +"'"
                c_id = (contact_id)
                mycursor.execute(sql_select,c_id)
                record = mycursor.fetchone()
                print("")
                #check if contact exist
                if mycursor.rowcount == 1:  
                    print(record)
                    print("")         
                    
                    sql_update_query = "UPDATE contacts SET contact_name = %s,contact_age = %s, contact_dob = %s WHERE contact_id = "+ contact_id +""
                    update_val =[]
                    unchange_value = 'Leave Blank To Accept Existing Value'
                    input_text = [f"Enter New Name({unchange_value}): ",f"Enter New Age({unchange_value}): ",f"Enter New Birth Date({unchange_value}): "]
                    input_error_msg = ["Sorry, please provide a valid name, name must be strings","Sorry, please provide a valid age, age must be a positive number","Sorry, please provide a valid date of birth, date of birth format 'YYYY-MM-DD'"]

                    #name edit input  and validation                        
                    while True: 
                        update_val.append("")
                        print("Existing Value: "+ str(record[1]))
                        update_val[0] = input(input_text[0]).strip().upper()
                        if update_val[0] != "":       
                            name_IsValid = validate_name(update_val[0])
                            if name_IsValid == True:
                                break
                            else:
                                print("")
                                print(input_error_msg[0])
                        else:
                            update_val[0] = record[1]
                            break
                            
                    print("")
                    
                    #age edit input and validation
                    while True:
                        update_val.append("")
                        print("Existing Value: "+ str(record[2]))
                        update_val[1] = input(input_text[1]).strip()
                        if update_val[1] != "": 
                            age_IsValid = validate_int(update_val[1])
                            if age_IsValid == True:
                                break
                            else:
                                print("")
                                print(input_error_msg[1])
                        else:
                            update_val[1] = record[2]
                            break
                            
                    print("")

                    #dob edit input  and validation
                    while True:
                        update_val.append("")
                        print("Existing Value: "+ str(record[3]))
                        update_val[2] = input(input_text[2]).strip()
                        if update_val[2] != "":
                            dob_IsValid = validate_dob(update_val[2])
                            if dob_IsValid == True:
                                break
                            else:
                                print("")
                                print(input_error_msg[2])
                        else:
                            update_val[2] = record[3]
                            break    

                    print("Before updating record ")
                    print("")
                    print(update_val)
                    print("")
                    #execute and commit update
                    mycursor.execute(sql_update_query,update_val)
                    conn.commit()
                    print("Record Updated successfully ")
                    print("")
                    print("After updating record ")
                    mycursor.execute(sql_select)
                    record = mycursor.fetchone()
                    print(record)
                    
                else:
                    print("No Record Found")
            
                mycursor.close()
                conn.close()
            except mysql.connector.Error as err:
                 handle_error(err)
        else:
            print("")
            print("Please Input a number or an integer")
            print("")   

#This function when called will remove/delete a record
#From the database based on Unique record ID or contact_id provided by 
#By the end user. 
def deletecontact():
     while True:
        print("")
        quit_param = input("Type \"quit\" to quit the Delete Prompt or Leave Blank and \n\nPress the 'Enter' key to continue to Delete other contacts: ").strip()
        if quit_param.lower() == "quit":
            print("")
            break       
        print("")
        #User input contact id
        contact_id = input("Enter Contact Id To Delete: ")
        if validate_int(contact_id) == True:
            print("")
            try:
                conn = mysql.connector.connect(**connection_config_dict)
                mycursor = conn.cursor()
                sql = "SELECT * FROM contacts WHERE contact_id = '"+ contact_id +"'"
                c_id = (contact_id)
                mycursor.execute(sql)
                myresult = mycursor.fetchone()
                #Check if contact exist
                if mycursor.rowcount == 1: 
                    print(myresult)
                    print("")
                    #Confirm Delete Operation
                    del_confirm = input("Are You Sure, You Want To Delete the Above contact? \n\nPlease Type 'Y' and Press the 'Enter' key to Confirm Delete or Leave Blank and Press Enter to Cancel :")
                    if del_confirm.lower() == "y":
                        del_sql = "DELETE FROM contacts WHERE contact_id = '"+ contact_id +"'"
                        mycursor.execute(del_sql)
                        conn.commit()
                        print("")
                        print(mycursor.rowcount, "record(s) deleted")
                    else:
                        print("")
                        print("User Has Cancelled the Delete Operation")
                else:
                    print("Contact does not Exist")

                mycursor.close()
                conn.close()
                print("")   
            except mysql.connector.Error as err:
                 handle_error(err)
        
        else:
            print("")
            print("Please Input a number or an integer")
            print("")

#This function when called will retrieve selected records
#From the database based on the search term(s) provided by 
# By the end user. 
def searchcontact():
    while True:
        print("")
        quit_param = input("Type \"quit\" to quit the Search Prompt or Leave Blank and \n\nPress the 'Enter' key to continue to Search for other contacts: ").strip()
        if quit_param.lower() == "quit":
            print("")
            break       
        print("")
        contact_id = input("Enter ContactInfo To Search: ")
        try:
            conn = mysql.connector.connect(**connection_config_dict)
            mycursor = conn.cursor()
            sql = "SELECT * FROM contacts WHERE contact_id LIKE %s OR contact_name LIKE %s OR contact_age LIKE %s OR contact_dob LIKE %s"
            c_id = (contact_id + "%",contact_id + "%",contact_id + "%",contact_id)
            mycursor.execute(sql,c_id)
            myresult = mycursor.fetchall()
            print("")
            #check for rows returned
            if mycursor.rowcount > 0:
                for x in myresult:
                    print(x)
            else:
                print("No Record(s) Found")
            mycursor.close()
            conn.close()
            print("")
        except mysql.connector.Error as err:
             handle_error(err)
    
#This function when called will retrieve all records
#Stored in the database
def showcontacts():
    print("")
    try:
        conn = mysql.connector.connect(**connection_config_dict)
        mycursor = conn.cursor()
        mycursor.execute("SELECT * FROM contacts")
        myresult = mycursor.fetchall()
        #check for rows returned
        if mycursor.rowcount > 0:
            for x in myresult:
                print(x)
        else:
            print("No Record(s) Found")

        mycursor.close()
        conn.close()
        print("")
    except mysql.connector.Error as err:
         handle_error(err)

#This function has a parameter that takes a key word
#Then a condition is check to decide which function should be called
#To perform next operation.
def to_do(my_key):           
    if my_key.lower() == "create":
        createcontact()
    
    elif my_key.lower() == "edit":
        editcontact()

    elif my_key.lower() == "delete":
        deletecontact()
    
    elif my_key.lower() == "search":
        searchcontact()
    
    elif my_key.lower() == "showall":
        showcontacts()
    
    elif my_key.lower() == "help":
        contacts_help()

    else:
        print("")
        print("Invalid Entry")
        print("")
        print("The Accepted Key Words are: Help,Create,Edit,Delete,Search,Showall,Quit")
        print("")

#Main program entry point
while True:
    my_key = input("What Do You Want To Do....?: ")
    if my_key.lower() == "quit":
        break
    else:
        to_do(my_key)