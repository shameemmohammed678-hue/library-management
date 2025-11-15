import pymysql
import pymysql.cursors
class Librarymandb:


    def __init__(self):
        try:
            self.con = pymysql.connect(
            host="localhost",
            user="root",
            password="Root2004$",
            database="librarydb",
            port=3306,
            connect_timeout=5
            )
            self.cursor = self.con.cursor(pymysql.cursors.DictCursor)
        except Exception as e:
            print("Failed to connect",str(e))


    def book_exists(self,bookid):
        query = """SELECT * FROM books WHERE book_id = %s"""
        self.cursor.execute(query,(bookid,))
        return self.cursor.fetchone() is not None





    def add_books(self,uname,Id,title,author,publisher,genre,pub_year,available_quantity):

        if self.book_exists(Id):
            return "THIS BOOK ID IS ALREADY AVAILABLE"

        try:
            self.cursor.execute("""SELECT role FROM users WHERE username = %s""",(uname,))
            user = self.cursor.fetchone()
            if not user:
                return "USER NOT FOUND"
            elif user['role'] != 'admin':
                return "ACCESS DENIED: ONLY ADMIN CAN ADD BOOKS"



            query = """INSERT INTO books(book_id,title,author,publisher,genre,pubyear,available_quantity)
                   VALUES(%s,%s,%s,%s,%s,%s,%s)          
                """
            self.cursor.execute(query,(Id,title,author,publisher,genre,pub_year,available_quantity))
            self.con.commit()
            return "BOOK ADDED SUCCESSFULLY"
        except Exception as e:
            self.con.rollback()
            return f"FAILED TO ADD BOOKS {str(e)}"

    def View_books(self):
            try:
                self.cursor.execute("SELECT * FROM books")
                result = self.cursor.fetchall()
                if not result:
                    return "NO BOOKS FOUND"
                else:
                    return result
            except Exception as e:
                return f"SOMETHING WRONG {str(e)}"
    
    
    def user_exists(self,uname):
        uname = uname.lower()
        self.cursor.execute("SELECT * FROM users WHERE username = %s",(uname,))
        return self.cursor.fetchone() is not None
        
    
    def create_username(self,uname,phone,email):

        if self.user_exists(uname):
            return "USER ALREADY EXISTS"

        try:
            uname = uname.lower()
            query = """INSERT INTO users(username,phone,email)VALUES(%s,%s,%s)"""
            self.cursor.execute(query,(uname,phone,email))
            self.con.commit()
            return "USER NAME CREATED SUCCESSFULLY"
        except Exception :
            self.con.rollback()
            return f"SOMETHING WRONG {str(e)}"
        
    def borrow_book(self,uname,bookid,qty):
        try:
            uname = uname.lower()
            self.cursor.execute("""SELECT user_id FROM users WHERE username = %s""",(uname,))
            user = self.cursor.fetchone()
            if user is  None:
                return "USER NOT FOUND"
            
            user_id = user['user_id']
            self.cursor.execute("""SELECT * FROM borrowers WHERE user_id = %s AND book_id = %s AND
                                return_date IS NULL""",(user_id,bookid))
            existing = self.cursor.fetchone()
            if existing:
                return "BOOK ALREADY BORROWED"
            


            self.cursor.execute("""SELECT available_quantity FROM books WHERE book_id = %s """,(bookid,))
            book = self.cursor.fetchone()
            if book is None:
                return "No BOOKS FOUND"
            
            if book['available_quantity']<qty:
                return "NO ENOUGH COPIES"
            
            self.cursor.execute("""UPDATE books SET available_quantity = available_quantity-%s 
                                WHERE book_id = %s""",(qty,bookid))
            
    
            self.cursor.execute("""INSERT INTO borrowers(user_id,book_id,quantity) VALUES (%s,%s,%s)""",(user_id,bookid,qty))
            self.con.commit()
            return "BORROWED SUCCESSFULLY"
        except Exception as e :
            self.con.rollback()
            return f"SOMETHING WRONG {str(e)}"
            
        
    def return_book(self,uname,bookid):
        try:
            uname = uname.lower()
            self.cursor.execute("""SELECT user_id FROM users WHERE username =%s""",(uname,))
            user = self.cursor.fetchone()
            if user is None:
                return "USER NOT FOUND"

            user_id = user['user_id']
            self.cursor.execute("""SELECT borrower_id,quantity FROM borrowers 
                                WHERE book_id = %s AND user_id = %s AND return_date IS NULL""",(bookid,user_id))
            
            record = self.cursor.fetchone()

            if record is None:
                return "BOOK RECORD NOT FOUND"
            
            borrower_id  = record['borrower_id']
            qty = record['quantity']


            self.cursor.execute("""UPDATE borrowers SET return_date = CURRENT_TIMESTAMP 
                                WHERE borrower_id = %s 
                                """,(borrower_id,))
            self.cursor.execute("""UPDATE books SET available_quantity = available_quantity+%s 
                                WHERE book_id = %s""",(qty,bookid))


            self.con.commit()
            return "BOOK RETURNED SUCCESSFULLY"
        except Exception as e:
                self.con.rollback()
                return f"FAILED TO RETURN BOOK {str(e)}"

    def borrowers_details(self,uname):
        try:
            self.cursor.execute("""SELECT role FROM users WHERE username = %s""",(uname,))
            user = self.cursor.fetchone()
            if not user:
                return "NO USER FOUND"
            elif user['role'] != 'admin':
                return "ACCESS DENIED: ONLY ADMIN CAN VIEW BORROWER DETAILS"
            

            query = """SELECT b.borrower_id,
                        u.username,
                        bk.title,
                        b.borrow_date,
                        b.return_date FROM borrowers b
                        INNER JOIN users u ON u.user_id = b.user_id
                        INNER JOIN books bk ON bk.book_id = b.book_id"""
            
            self.cursor.execute(query)
            result =  self.cursor.fetchall()
            if not result:
                return "NO BORROWERS FOUND"
            else:
                return result

        except Exception as e:
            self.con.rollback()
            return f"FAILED TO FETCH_DATA {str(e)}"
        
    def View_users(self,uname):
        try:
            
            self.cursor.execute("""SELECT role FROM users WHERE username = %s""",(uname,))
            user = self.cursor.fetchone()
            if not user:
                return "USER NOT FOUND"
            elif user['role'] != 'admin':
                return "ACCESS DENIED: ONLY ADMIN CAN VIEW USER DETAILS"
            
            self.cursor.execute("""SELECT * FROM users""")
            result = self.cursor.fetchall()
            if not result:
                return "NO USERS FOUND"
            else:
                return result
        except Exception as e:
            return f"FAILED TO FTCH DATA {str(e)}"

            
    def search_book(self,bookid):
        try:
            query = """SELECT * FROM books 
            WHERE book_id = %s"""
            self.cursor.execute(query,(bookid,))
            result = self.cursor.fetchone()
            if result is not None:
                return result
            else:
                return "NO BOOK FOUND"
        except Exception as e:
            return f"FAILED_TO_FETCH_DATA {str(e)}"
        
    def remove_book(self,uname,book_id):
        try:
            self.cursor.execute("""SELECT role FROM users WHERE username = %s""",(uname,))
            user = self.cursor.fetchone()
            if not user:
                return "USER NOT FOUND"
            elif user['role'] != 'admin':
                return "ACCESS DENIED: ONLY ADMIN CAN REMOVE BOOKS"

            query = """SELECT * FROM books WHERE book_id = %s"""
            self.cursor.execute(query,(book_id,))
            book = self.cursor.fetchone()
            if book is None:
                return "BOOK NOT FOUND"
            else:
                self.cursor.execute("""UPDATE books SET available_quantity = 0 WHERE book_id = %s""",(book_id,))
                self.con.commit()
                return "BOOK REMOVED SUCCESSFULLY"
        except Exception as e:
            self.con.rollback()
            return f"SOMETHING WRONG {str(e)}"
        
    def get_user_role(self,uname):
        try:  
            uname = uname.lower()
            query = """SELECT role FROM users WHERE username = %s"""
            self.cursor.execute(query,(uname,))
            user = self.cursor.fetchone()
            if not user:
                return "USER NOT FOUND"
            if user['role'] == 'admin':
                return "ADMIN"
            else:
                return "USER"
        except Exception as e:
            return f"Something wrong {str(e)}"

    def Close_Connection(self):
        self.cursor.close()
        self.con.close()
        