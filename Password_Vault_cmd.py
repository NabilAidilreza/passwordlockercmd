from tkinter import *
import sqlite3, hashlib
import os
import maskpass
with sqlite3.connect("password_vault.db") as db:
    cursor = db.cursor()
### Opens via prompt ###
cursor.execute('''
CREATE TABLE IF NOT EXISTS masterpassword(
id INTEGER PRIMARY KEY,
password TEXT NOT NULL);
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS vault(
id INTEGER PRIMARY KEY,
website TEXT NOT NULL,
username TEXT,
password TEXT NOT NULL);
''')

login_bool = False
masterPass = "@SIR"

def hashPassword(input):
    hashed = hashlib.md5(input)
    hashed = hashed.hexdigest()
    return hashed

def initializeSystem():
    print("\n")
    print("------------------------------------------------------------")
    print("       xxxxxxxxxXXX    LOGIN REQUIRED    XXXxxxxxxxxx       ")
    print("------------------------------------------------------------")
    print("")
    print("xxxxxxxxx -- UNAUTHORISED PERSONNEL NOT ALLOWED -- xxxxxxxxx")
    print("     xxxxxxxxx -- YOU HAVE BEEN WARNED -- xxxxxxxxx         ")
    print("")
    print("")
    print("xxxxxxx --- YOU ARE SIGNING IN AS ADMINISTRATOR --- xxxxxxxx")
    print("")
    print("      xxxxxxxxx -- INPUT YOUR PASSWORD -- xxxxxxxxx         ")
    print("")
    reply = maskpass.askpass(prompt="Enter password: ", mask="*")
    if reply != masterPass:
        print("")
        print("--------------------------------------------------------")
        print("     xxxxxxxxx -- INVALID PASSWORD -- xxxxxxxxx         ")
        print("--------------------------------------------------------")
        print("")
        print("--------------------------------------------------------")
        print("     xxxxxxxXXX  SHUTTING SCRIPT DOWN  XXXxxxxxxx       ")
        print("--------------------------------------------------------")
        raise SystemExit
    else:
        os.system('cls')
        menuScreen()


def menuScreen():
    print("\n")
    print("------------------------------------------------------------")
    print("        xxxxxxxxxXXX    CONFIDENTIAL    XXXxxxxxxxxx        ")
    print("------------------------------------------------------------")
    print("")
    print("")
    print("////////////////////////////////////////////////////////////")
    print("xxxxXXX        Welcome to the Password Vault        XXXxxxxx")
    print("")
    print("Actions:")
    print("1. View All")
    print("2. Search Entry")
    print("3. Insert Entry")
    print("4. Update Entry")
    print("5. Delete Entry")
    print("6. Exit")
    print("")
    print("////////////////////////////////////////////////////////////")
    print("")
    print("------------------------------------------------------------")
    print("        xxxxxxxxxXXX    CONFIDENTIAL    XXXxxxxxxxxx        ")
    print("------------------------------------------------------------")
    print("")
    reply = input("Action?: ")
    actionScreen(reply)

def actionScreen(reply):
    def fetchAll():
        fields = ("ID","Website","Username","Password")
        check = cursor.execute('''SELECT * FROM vault''')
        check = cursor.fetchall()
        print(fields)
        for c in check:
            print(c)
        menuScreen()
    def addEntry():
        web = input("Website Name: ")
        user = input("Username: ")
        pw = input("Password: ")

        insert_fields = '''INSERT INTO vault(website,username,password) VALUES(?,?,?)'''
        cursor.execute(insert_fields,(web,user,pw))
        db.commit()
        menuScreen()
        
    def removeEntry():
        txt = input("ID to delete: ")
        cursor.execute('''DELETE FROM vault WHERE id =?''',(txt,))
        db.commit()
        menuScreen()
        
    def updateEntry():
        TXT = input("ID to update: ")
        web = input("Website Name: ")
        user = input("New Username: ")
        pw = input("New Password: ")
        
        update_fields = '''UPDATE vault SET ,website = ?,username = ?, password = ? WHERE id =?'''
        cursor.execute(update_fields,(user,pw,web,TXT))
        db.commit()
        menuScreen()

    def searchEntry():
        web = input("Website Name: ")
        search_fields = '''SELECT username,password FROM vault WHERE website = ?'''
        cursor.execute(search_fields,(web,))
        temp = cursor.fetchall()
        if temp != []:
            temp = temp[0]
            reply = 'Website: ' + web + '\n' + 'Username:' + temp[0] + ' \nPassword: ' + temp[1]
            print("Result: " + reply)
        else:
            reply = 'No such website in vault'
            print("Result: " + reply)
        menuScreen()

    ### MAIN ###
            
    if reply == "1":
        fetchAll()
    elif reply == "2":
        searchEntry()
    elif reply == "3":
        addEntry()
    elif reply == "4":
        updateEntry()
    elif reply == "5":
        removeEntry()
    elif reply == "6":
        print("System Exit")
        raise SystemExit
    else:
        print("Invalid Input")
        
    ### ---- ###
        
check = cursor.execute('''SELECT * FROM vault''')
check = cursor.fetchall()
if check:
    initializeSystem()
else:
    print("No data")
