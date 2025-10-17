import json
class Libraryman:
    def __init__(self):
        self.Books = []
        self.username = []
        self.borrowedbooks= {}

    def savedata(self):
         data={
              "Books":self.Books,
              "username":self.username,
              "Borrowed_Books":self.borrowedbooks
    
         }
         with open("library_data.json",'w') as f:
              json.dump(data,f,indent= 4)
    
    def add_stocks(self,id,publisher,author,title,genre,pubyear,quantity):
        
        for book in self.Books:
             if book["ID"] == id:
                  print("There is already a book with a same ID ! ")
                  return
        newbook = {
            "ID": id,
            "Publisher":publisher,
            "Author":author,
            "Title":title,
            "Genre":genre,
            "published_year":pubyear,
            "Available_Quantity":quantity
        }
        self.Books.append(newbook)
        return newbook


    def Is_available(self):
            id = int(input("Enter the Book ID :"))
            for book in self.Books:
                if id == book["ID"]:
                    if book["Available_Quantity"] == 0:
                           print("This book is not in stock")
                    else:
                         print(f"ID:{book['ID']} ")
                         print(f"Book Name : {book['Title']}")
                         print(" Available Qauntity : ",book["Available_Quantity"])  
                         return

    
            print("No Book with this ID !")

    def create_username(self):
         
        name = input("Enter your user name : ")
        if name not in self.username:
             self.username.append(name)
             print("username is created ")
        else:
             print("username already existed")


    
    def Get_Book(self):
        username = input("Enter Your user Name : ")


        if username in self.username:
            id = int(input("Enter The Book ID : "))
            quantity = int(input("Enter Quantity : "))
            for book in self.Books:
                if id == book["ID"]:
                    if book["Available_Quantity"] >= quantity:
                         book["Available_Quantity"] -= quantity
                         if username not in self.borrowedbooks:
                              self.borrowedbooks[username] = []
                         book = {
                              "ID" : id,
                              "Title" : book["Title"],
                              "Quantity" :quantity
                         }
                         self.borrowedbooks[username].append(book)
                         print(f"Book Borrowed by {username} successfully")
                         return
                    else:
                         print("This book is not in stock")

                    

            print("No Book is found with this ID")

        else:
             print("Create username to get a Book ")

    def addbook(self):
         id = int(input("Enter The Book ID : "))
         publisher = input("Enter the Name of the publisher : ")
         author  = input("Enter the Name of  Author : ")
         title = input("Enter the Title of the Book : ")
         genre = input("Enter the Genre of the Book : ")
         pubyear  = input("Enter year of publication : ")
         quantity = int(input("Enter the Quantity : "))
         self.add_stocks(id,publisher,author,title,genre,pubyear,quantity)


    def Display(self):
        for book in self.Books:
            for key,value in book.items():
                   print(f"{key} : = {value}")
            print("-----------------------------")

        
    def Return_Book(self):
       uname = input("Enter your username: ")
       if uname in self.borrowedbooks and self.borrowedbooks[uname]:
          print("Books Borrowed by you:")
          for i, book in enumerate(self.borrowedbooks[uname], start=1):
            print(f"{i}. ID: {book['ID']} | Title: {book['Title']} | Quantity: {book['Quantity']}")

          try:
              choice = int(input("Enter the number of the book you want to return: ")) - 1
          except ValueError:
            print("Invalid input! Please enter a number.")
            return

          if 0 <= choice < len(self.borrowedbooks[uname]):
            book_info = self.borrowedbooks[uname][choice]
            id = book_info["ID"]
            quantity = book_info["Quantity"]

            for book in self.Books:
                if id == book["ID"]:
                    book["Available_Quantity"] += quantity
                    break

            
            self.borrowedbooks[uname].pop(choice)
            if not self.borrowedbooks[uname]:
                del self.borrowedbooks[uname]

            print("Book returned successfully!")
            self.savedata()  
          else:
            print("Invalid choice")
       else:
        print("No borrowed books found for this username")

                               
    def Borrowers_Details(self):
        if len(self.borrowedbooks) == 0:
             print("empty list ! ")
             return
         
        for user,books in self.borrowedbooks.items():
               print(f"  username : {user} ")
               for book in books: 
                   print(f"ID : {book['ID']} Title : {book['Title']} Quantity : {book['Quantity']}")
               print("--------------------")



    def Remove_book(self):
          id = int(input("Enter the Book ID : "))
          for book in self.Books:
              if book["ID"] == id:
                   confirm = input(f"Are You Sure Do You Want To remove {book['Title'] } ('yes/no') : ")
                   if confirm == "yes":
                         self.Books.remove(book)
                         self.savedata()
                         return
                   else:
                        print("Book Removal Cancel by the user ! ")
                        break
          print("NO Book Found With This ID")



    def loaddata(self):
     try:
           with open("library_data.json", 'r') as f:
              data = json.load(f)
              self.Books = data.get("Books", [])
              self.username = data.get("username", [])
              self.borrowedbooks = data.get("Borrowed_Books", {})
     except (FileNotFoundError, json.JSONDecodeError):
        self.Books = []
        self.username = []
        self.borrowedbooks = {}                   
def main():
     l =Libraryman()
     l.loaddata()
     if not l.Books:
         l.add_stocks(122,"Devi publishers ","william james","one love","Romantic","12-04-2003",10)
         l.add_stocks(234,"sofia publishers "," james","First day in Earth","Adventure","20-06-2005",10)
         l.add_stocks(456,"Abdul publishers","Daniel","one love","Romantic","02-12-2012",10)
         l.add_stocks(235,"hussain publishers","Benjamin","one love","Romantic","27-07-2014",10)


     while True:
        print()
        print("1.View Books Details " )
        print("2. check Availability  " )
        print("3.Add a Book ")
        print("4.Remove Book ")
        print("5.Borrow Book ")
        print("6.Return Book ")
        print("7.Borrowers Details" )
        print("8.Create User Name  ")
        print("9.Exit " ) 

        choice = int(input("Enter your choice : "))

        if choice == 1:
               print("Books Details : " )
               l.Display()

        elif choice == 2:
               l.Is_available()

        elif choice == 3:
                 print("Enter  the Details of the Book")
                 l.addbook()
        elif choice == 4:
             l.Remove_book()

        elif choice == 5:
             l.Get_Book()

        elif choice == 6:
             l.Return_Book()
             
             
        elif choice == 7:
             l.Borrowers_Details()

        elif choice == 8:
             l.create_username()

        elif choice == 9:
             print("System Exited ! Have a Good Day")
             l.savedata()
             break

        else:
             print("Enter a valid choice !")
             
if __name__ == "__main__":
     main()
