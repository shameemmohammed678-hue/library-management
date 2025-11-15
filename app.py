import streamlit as st
from librarydb import Librarymandb
import pandas as pd


lib = Librarymandb()

st.title("Library Management System")



admin_menus = ["View Books","Search Book","Add Book","Remove Book","Borrow Book","Return Book","Borrower Details","Create Username","View Users"]
user_menus = ["View Books","Search Book","Borrow Book","Return Book","Create Username"]
choice = None
if "role" not in st.session_state:
    st.session_state.role = None

if st.session_state.role is None:
    username = st.text_input("Enter your username")
    if st.button("Login"):
        result = lib.get_user_role(username)
        if result in ["USER","ADMIN"]:
            st.session_state.role = result
        else:
            st.error("USER NOT FOUND")
            st.session_state.role = None

if st.session_state.role == "ADMIN":
    choice = st.sidebar.selectbox("Menus",admin_menus)
elif st.session_state.role == "USER":
    choice = st.sidebar.selectbox("Menus",user_menus)
else:
    st.warning("PLEASE LOGIN TO CONTINUE")

if st.session_state.role:
    if st.sidebar.button("Log Out"):
        st.session_state.role = None
        st.success("LOG OUT SUCCESSFULLY")








if choice == "View Books":
    st.subheader("Book Details : ")
    if st.button("View Book List"):
        result = lib.View_books()
        if isinstance(result,str):
            st.info(result)
        else:
            df = pd.DataFrame(result)
            df.rename(columns={
                "book_id": "Book ID",
                "title": "Title",
                "author": "Author",
                "publisher": "Publisher",
                "genre": "Genre",
                "pubyear": "Publication Year",
                "available_quantity": "Available Quantity"
            }, inplace=True)
            st.dataframe(df, use_container_width=True)

elif choice == "Search Book":
    book_id = st.number_input("Enter Book ID: ",step = 1)
    if st.button("Check"):
        result = lib.search_book(book_id)
        if isinstance(result,str):
            st.warning(result)
        else:
            df = pd.DataFrame([result])  
            df.rename(columns={
                "book_id": "Book ID",
                "title": "Title",
                "author": "Author",
                "publisher": "Publisher",
                "genre": "Genre",
                "pubyear": "Publication Year",
                "available_quantity": "Available Quantity"
            }, inplace=True)
            st.dataframe(df, use_container_width=True)
        
elif choice == "Add Book":
    st.subheader("Enter Book Details")
    Id = st.number_input("Enter Book ID",step = 1)
    title = st.text_input("Enter the title")
    author = st.text_input("Enter Name of Author")
    publisher = st.text_input("Enter Publisher")
    genre = st.text_input("Enter Genre ")
    pubyear = st.text_input("Enter Publication year ")
    quantity = st.number_input("Enter Quantity",step = 1)
    uname = st.text_input("Enter your username ")
    if st.button("Add Book"):
        result = lib.add_books(uname,Id,title,author,publisher,genre,pubyear,quantity)
        if "SUCCESSFULLY" in result:
            st.success(result)
        else:
            st.error(result)

elif choice == "View Users":
    uname = st.text_input("Enter username")
    if st.button("Users list"):
        result = lib.View_users(uname)
        if isinstance(result,str):
            st.warning(result)
        elif isinstance(result, list):
            df = pd.DataFrame(result)
            df.rename(columns={
            "user_id": "User ID",
            "username": "Username",
            "phone": "Phone Number",
            "email": "Email Address"
                }, inplace=True)
            st.dataframe(df,use_container_width=True)

        else:
            st.error("No Data Found")


elif choice == "Create Username":
        st.subheader('Create username ')
        uname = st.text_input("Enter Username ")
        phone = st.text_input("Enter Mobile Number")
        email = st.text_input("Enter email")
        if st.button("Create"):
            result = lib.create_username(uname,phone,email)
            if "SUCCESSFULLY" in result:
                st.success(result)
            else:
                st.warning(result)


elif choice == "Borrower Details":
    st.subheader('Borrower Details')
    uname = st.text_input("Enter username")
    if st.button("View Borrower Details"):
        result = lib.borrowers_details(uname)
        if isinstance(result,str):
            st.warning(result)
        elif isinstance(result,list):
            df = pd.DataFrame(result)
            df.rename(columns={
                "borrower_id": "Borrower ID",
                "username": "Username",
                "title": "Book Title",
                "borrow_date": "Borrowed On",
                "return_date": "Returned On"
            }, inplace=True)
            st.dataframe(df, use_container_width=True)
        else:
            st.error("No Borrower Data Available ")

elif choice == "Borrow Book":
    st.subheader("Borrow Book")
    uname = st.text_input("Enter username ")
    bookid = st.number_input("Enter Book ID",step=1)
    qty = st.number_input("Enter Quantity",step=1)
    if st.button("Next"):
        result = lib.borrow_book(uname,bookid,qty)
        if "SUCCESSFULLY" in result:
            st.success(result)
        else:
            st.warning(result)

elif choice == "Return Book":
    st.subheader("Return Book")
    uname = st.text_input("Enter your Username")
    bookid = st.number_input("Enter Book ID",step =1)
    if st.button("Return"):
        result = lib.return_book(uname,bookid)
        if "SUCCESSFULLY" in result:
            st.success(result)
        else:
            st.warning(result)

elif choice == "Remove Book":
    st.subheader("Remove Book")
    bookid = st.number_input("Enter Book ID",step = 1)
    uname = st.text_input("Enter Your username ")
    confirm = st.checkbox("Are you confirm to remove this book permanently")
    if st.button("Remove"):
        if confirm:
            result = lib.remove_book(uname,bookid)
            if "SUCCESSFULLY" in result:
                st.success(result)
            else:
                st.warning(result)
        else:
            st.warning("Please confirm before removing ")

