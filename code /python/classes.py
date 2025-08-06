import re
import uuid
import psycopg2
import qrcode
from datetime import *

from sqlalchemy import true

class loginValidation():
    def __init__(self):
        self.usernameReq = [3,16,"[a-z]"]
        self.passwordReq = [8,"[a-z]","[A-Z]","\d"]
        self.username = ""
        self.password = ""
        self.conn = psycopg2.connect(
            dbname='Library Management System', 
            user='sql test', 
            password='admin',
            port=5432)
        
    def usernameValidate(self, u):
        if len(u) >= self.usernameReq[0] and len(u) <= self.usernameReq[1] and re.search(self.usernameReq[2], u):
            return True 
        else: return False
            
    def passwordValidate(self, p):
        if len(p) >= self.passwordReq[0] and re.search(self.passwordReq[1],p) and re.search(self.passwordReq[2],p) and re.search(self.passwordReq[3],p):
            return True
        else: return False

    def check_login(self, data):
        self.username = data[0]
        self.password = data[1]
        
        cur = self.conn.cursor()
        
        script = "SELECT * FROM users WHERE email=%s AND password=%s"
        cur.execute(script, (self.username,self.password))
        
        rows = cur.fetchall()
        for row in rows:
            print(row)
            if row[2] == self.password and row[1] == self.username:
                return True
            else: return False
  
        
    
class utility():
    def __init__(self):
        pass
    
    def hashing(self, target):
        sum_of_char = 0
        for char in target:
            sum_of_char += ord(char)
        print(sum_of_char)    
        return sum_of_char    
    
    def generate_receipt(self, target):
        now = datetime.now()
        date_time = now.strftime("%Y-%m-%d %H:%M:%S")
        
        return f"""{"*" * 49} 
            {target[2]}
            {date_time} 
            {target[0]}
            {target[1]} \n{"*" * 49}"""
   
   
#* this was part of an attempt to set up a QR code system that would make it easier 
#* for users to signout books
#* I ran into a limitation of not being able to directly lauch the website through the QR code
#* without paying for a dedicated domain

"""    def generate_qrCode(self, data):
        img = qrcode.make(data[0])
        type(img)
        img.save(data[1])"""
        

        
class library():
    def __init__(self):
        self.title = ""
        self.author = ""
        self.ID = ""
        self.stock = False
        self.copies = 0
        self.conn = psycopg2.connect(
            dbname='Library Management System', 
            user='sql test', 
            password='admin',
            port=5432)
        
    def add_book(self, data):
        cur = self.conn.cursor()        
        print(data) 
        if len(data) == 3:

            self.title = data[0]
            self.author = data[1]
            self.copies = int(data[2])
            
            search_script = "SELECT * FROM books WHERE title = %s"
            cur.execute(search_script, (self.title,))
            
            rows = cur.fetchall()
            
            if rows:
                for row in rows:
                    self.stock = row[2]
                    self.copies += int(row[3])
                
                if self.stock == False:
                    self.stock = True
                    insert_script = "UPDATE books SET in_stock=%s, copies_in_stock=%s WHERE title=%s"
                    insert_values = (self.stock, self.copies)
                    cur.execute(insert_script,insert_values)
                
                return "Added to library"
            
            else:
                insert_script = 'INSERT INTO books (title, author, in_stock, copies_in_stock, book_id) VALUES (%s,%s,%s,%s,%s)'
                if self.copies > 0 and self.stock == False:
                    self.stock = True
                else: print("already have books in stock")
                self.ID = utility().hashing(self.title+self.author)
                insert_values = (self.title,self.author,self.stock,self.copies,self.ID)
                cur.execute(insert_script,insert_values)
                self.conn.commit()
                cur.close()
                self.conn.close()
                return "Added to library"
        else: return "Error, Not added to library"
      
    def search_library(self, data):
        cur = self.conn.cursor()
        
        title, author = data[0], data[1]
        
        if title is None and author is not None:
            search_script = 'SELECT title, author, in_stock FROM books WHERE author = %s'
            cur.execute(search_script, (author,))       
        elif author is None and title is not None:
                search_script = 'SELECT title, author, in_stock FROM books WHERE title ILIKE %s'
                cur.execute(search_script,(f"%{title}%",)) 
        elif title is not None and author is not None:
            search_script = 'SELECT title, author, in_stock FROM books WHERE title ILIKE %s AND author = %s'
            cur.execute(search_script, (f"%{title}%", author))
        else: 
            search_script = 'SELECT title, author, in_stock FROM books'
            cur.execute(search_script)
            
        rows = cur.fetchall()
        for row in rows:
            print(row)
        cur.close()
        self.conn.close()
        return rows    
        
    def remove_book(self, data):
        cur = self.conn.cursor()
        
        title = data[0]
        
        search_script = "SELECT * FROM books WHERE title = %s"
        cur.execute(search_script, (title,))
        
        rows = cur.fetchall()
        
        for row in rows:
            print(row)
            self.copies = int(row[3])
        
        if self.copies >= 0:
            self.stock = False
            return f"Error, no copies of {data} in stock"
        else: 
            self.copies -= 1
            if self.copies == 0:
                self.stock = False
            
            insert_script = "UPDATE books SET in_stock=%s, copies_in_stock=%s WHERE title=%s"
            insert_values = (self.stock,self.copies, title)
            cur.execute(insert_script,insert_values)
            
            search_script = "SELECT * FROM books WHERE title = %s"
            cur.execute(search_script, (title,))
            rows = cur.fetchall()
            for row in rows:
                print(row)
            
            self.conn.commit()
            cur.close()
            self.conn.close()
            return f"removed a copy of {data}"
               
    def check_removed(self, data):
        cur = self.conn.cursor()
        
        search_script = 'SELECT * FROM loans'
        cur.execute(search_script)    
        
        rows = cur.fetchall()
        for row in rows:
            print(row)
        cur.close()
        self.conn.close()
        return rows    
    
    def create_loan(self, data):
        now = datetime.now()
        
        
        self.title = data[0]
        self.author = data[1]
        name = data[2]
        time = data[3]
        
        print(time)
        
        if time.endswith("d"):
            due_date = now + timedelta(days=int(time[:-1]))
        elif time.endswith("w"):
            due_date = now + timedelta(weeks=int(time[:-1]))
            
        else: raise ValueError("Error", "ITS BWOKEN - Lando Norris")
            
        date_time = now.strftime("%Y-%m-%d")
        
        cur = self.conn.cursor()
        
        search_script = "SELECT uuid FROM users WHERE name=%s"
        cur.execute(search_script, (name,))
        
        rows = cur.fetchall()
        uuid = rows[0]
        
        search_script = "SELECT book_id FROM books WHERE title=%s"
        cur.execute(search_script, (self.title,))
        
        rows = cur.fetchall()
        self.ID = rows[0]
        
        
        print(str(date_time))
        print(str(due_date))
        
        insert_script = 'INSERT INTO loans (uuid, book_id, date_borrowed, due_date, returned, overdue) VALUES (%s,%s,%s,%s,%s,%s)'
        insert_values = (uuid, self.ID, str(date_time), str(due_date), False, False)
        
        cur.execute(insert_script, insert_values)
        self.conn.commit()
        cur.close()
        self.conn.close()
        
        return "created a new loan"


        
class signUpValidate():
    def __init__(self):
        self.name = ""
        self.email = ""
        self.uuid = ""
        self.conn = psycopg2.connect(
            dbname='Library Management System', 
            user='sql test', 
            password='admin',
            port=5432)      
        
    def add_user(self, data):
        
        print(data)
        
        self.name = str(data[0])
        self.email = str(data[1])
        
        password = str(data[2])
        
        cur = self.conn.cursor()
        
        uuid_check_script = "SELECT uuid FROM users"
        cur.execute(uuid_check_script)
        
        self.uuid = utility().hashing(self.name + self.email)
        
        rows = cur.fetchall()
        check = False
        while check == False:
            for row in rows:
                print(row)
                if row == self.uuid:
                    self.uuid += 1
                else:
                    check = True    
        
        if loginValidation().passwordValidate(password) == True:
            insert_script = "INSERT INTO users (name, email, password, uuid) VALUES (%s,%s,%s,%s)"
            insert_values = (self.name,self.email,password,self.uuid)
            
            cur.execute(insert_script, insert_values)
            self.conn.commit()
            cur.close()
            self.conn.close()
            return "New user added"
            
        else: return "Error, password is not valid"
            
      
        
class debug():
    def __init__(self):
        self.conn = psycopg2.connect(
            dbname='Library Management System', 
            user='sql test', 
            password='admin',
            port=5432)
        
    def reset_books(self):
        cur = self.conn.cursor()
        
        script = "DELETE FROM books"
        
        cur.execute(script)
        self.conn.commit()
        cur.close()
        self.conn.close() 
        
    def reset_loans(self):
        cur = self.conn.cursor()
        
        script = "DELETE FROM loans" 
        
        cur.execute(script)   
        self.conn.commit()
        cur.close()
        self.conn.close()                    
