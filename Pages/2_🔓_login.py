import streamlit as st
import mysql.connector

def main():
    st.title("Login or Register")
    st.write("---")

    login_option = st.radio("Choose an option:", ("Login", "Register"))

    if login_option == "Login":
        st.subheader("Login")
        user_type = st.radio("Select user type:", ("Student", "Faculty"))
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        
        if st.button("Login"):
            if not username or not password:
                st.warning("Please fill in both fields.")
                return

            connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="root",
                database="project_db"
            )

            cursor = connection.cursor(dictionary=True)
            table_name = "users" if user_type == "Student" else "faculties"
            cursor.execute(f"SELECT * FROM {table_name} WHERE username=%s AND password=%s", (username, password))
            user = cursor.fetchone()
            connection.close()

            if user:
                user_id = user['id']
                st.session_state.user_id = user_id
                st.session_state.user_type = user_type
                st.success(f"Logged in as {username} (User ID: {user_id}, User Type: {user_type})")
                st.rerun()
            else:
                st.error("Invalid credentials. Please try again.")
    else:
        st.subheader("Register")
        name = st.text_input("Name")
        email = st.text_input("Email")
        user_type = st.radio("Select user type:", ("Student", "Faculty"))
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if st.button("Register"):
            try:
                if not name or not email or not username or not password:
                    st.warning("Please fill in all fields.")
                    return

                connection = mysql.connector.connect(
                    host="localhost",
                    user="root",
                    password="root",
                    database="project_db"
                )

                cursor = connection.cursor()
                table_name = "users" if user_type == "Student" else "faculties"
                cursor.execute(
                    f"INSERT INTO {table_name} (name, email, username, password) VALUES (%s, %s, %s, %s)",
                    (name, email, username, password)
                )
                connection.commit()
                connection.close()

                st.success(f"Registered successfully as {user_type}. You can now log in.")
            
                # ... (existing registration code)
            except mysql.connector.Error as err:
                if err.errno == 1644:
                    st.error("Invalid email format. Please provide a valid email.")
                else:
                    st.error(f"Database error: {err}")
            except Exception as e:
                st.error(f"An unexpected error occurred: {e}")
if __name__ == "__main__":
    main()
