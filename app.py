import streamlit as st
from libraryman import Libraryman
import pandas as pd


lib = Libraryman()
lib.loaddata()

st.title("Library Management System")
menus = ["View Book Details","Check Availability","Add Book","Remove Book","Borrow Book","Return Book","Borrower Details","Create username"]
choice = st.sidebar.selectbox("Menus",menus)

if choice == "View Book Details":
    st.subheader("Book Details : ")
    if lib.Books:
        st.dataframe(pd.DataFrame(lib.Books))
    else:
        st.info("No Books Available")

elif choice == "Check Availability":
    book_id = st.number_input("Enter Book ID: ",step = 1)
    if st.button("Check"):
        found = False
        for book in lib.Books:
            if book["ID"] == book_id:
                st.success(f" Book Name : {book['Title']}  Availalable Quantity : {book['Available_Quantity']} copies ")
                found = True
                break
        if not found:
            st.warning("No Book  available with this ID") 

elif choice == "Add Book":
    st.subheader("Enter Book Details")
    id = st.number_input("Enter Book ID",step = 1)
    publisher = st.text_input("Enter the Name of Publisher")
    author = st.text_input("Enter the Name of Author")
    title = st.text_input("Enter the Title ")
    genre = st.text_input("Enter the Genre ")
    pubyear = st.text_input("Enter Publication Year")
    quantity = st.number_input("Enter quantity",step = 1)
    if st.button("Add book"):
      lib.add_stocks(id,publisher,author,title,genre,pubyear,quantity)
      lib.savedata()
      st.success(f"Book {title} added to stocks successfully !")


elif choice == "Remove Book":
    id = st.number_input("Enter Book ID",step=1)
    found = False
    if st.button("Remove Book"):
        for book in lib.Books:
            if book["ID"] == id:
                lib.Books.remove(book)
                found = True
                lib.savedata()
                st.success("Book Removed successfully ")
                break    
        if not found:
            st.warning("No Book with this ID")


elif choice == "Create username":
    st.subheader('Create username ')
    uname = st.text_input('Enter username ')
    if st.button('create'):
        if uname in lib.username:
            st.warning('username already exists')
        else:
            lib.username.append(uname)
            st.success('User Name created successfully')
            lib.savedata()
        
elif choice == "Borrower Details":
    st.subheader('Borrower Details')
    if lib.borrowedbooks:
        for user,book in lib.borrowedbooks.items():
            st.write(f"{user}")
            st.dataframe(pd.DataFrame(book))

    else:
        st.info("No Borrowed Book currently")

elif choice == "Borrow Book":
    st.subheader("Borrow Book")
    uname = st.text_input("Enter username ")
    bookid = st.number_input("Enter Book ID",step=1)
    qty = st.number_input("Enter Quantity",step=1)
    found = False
    if st.button("Next"):
        if uname not in lib.username:
            st.warning("Create username : your username is not available ")
        else:
            for book in lib.Books:
                if book["ID"] == bookid and book["Available_Quantity"]>=qty:
                    book["Available_Quantity"]-=qty
                    if uname not in lib.borrowedbooks:
                        lib.borrowedbooks[uname] = []
                    b = {"ID":bookid,
                        "Title":book["Title"],
                        "Quantity":qty}
                    lib.borrowedbooks[uname].append(b)
                    found = True
                    lib.savedata()
                    st.success(f"Book{book['Title']} borrowed by {uname} successfully")
                    break
            if not found:
                    st.warning("This Book is currently not available")


elif choice == "Return Book":
    st.subheader("Return Book")
    uname = st.text_input("Enter your Username")
    found = False
    if uname in lib.borrowedbooks:
            borrowed = lib.borrowedbooks[uname]
            st.dataframe(pd.DataFrame(borrowed))
            book_id = st.number_input("Enter Book ID",step=1)
            if st.button("Return"):
                for book in borrowed:
                    if book["ID"] == book_id:
                        qty = book["Quantity"]
                        for b in lib.Books:
                            if b["ID"] == book_id:
                                b["Available_Quantity"]+=qty
                                break
                        borrowed.remove(book)
                        lib.borrowedbooks[uname] = borrowed
                        lib.savedata()
                        found = True
                        st.success("Book return successfully ")
                        break
                if not found:
                    st.warning("Book not found in the borrower list")

    else:
        st.info("No Books Borrowed by this username")