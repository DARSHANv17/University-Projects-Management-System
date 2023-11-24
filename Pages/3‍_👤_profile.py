import streamlit as st
import mysql.connector

def main():
    st.title("User Profile")
    st.write("---")

    user_id = st.session_state.get("user_id")
    user_type = st.session_state.get("user_type")

    if user_id:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            database="project_db"
        )

        cursor = connection.cursor(dictionary=True)
        table_name = "users" if user_type == "Student" else "faculties"
        cursor.execute(f"SELECT * FROM {table_name} WHERE id=%s", (user_id,))
        user = cursor.fetchone()

        if user:
            #st.subheader("Profile Information")

            if "editing_profile" in st.session_state and st.session_state.editing_profile:
                # Display editable input fields
                name = st.text_input("Name", user['name'], key="profile_name")
                email = st.text_input("Email", user['email'], key="profile_email")
                username = st.text_input("Username", user['username'], key="profile_username")

                # Update Profile
                if st.button("Update Profile"):
                    cursor.execute(
                        f"UPDATE {table_name} SET name=%s, email=%s, username=%s WHERE id=%s",
                        (name, email, username, user_id)
                    )
                    connection.commit()
                    st.session_state.editing_profile = False
                    st.success("Profile updated successfully.")
            else:
                # Display read-only profile information
                # Assuming 'user' is a dictionary with keys 'name', 'email', and 'username'
                st.markdown(
                    f"""
                    <style>
                        table {{
                            width: 50%;
                            border-collapse: collapse;
                            margin-top: 10px;
                        }}
                        th, td {{
                            padding: 10px;
                            text-align: left;
                            border-bottom: 1px solid #ddd;
                        }}
                    </style>
                    <table>
                        <tr>
                            <th>Name</th>
                            <td>{user['name']}</td>
                        </tr>
                        <tr>
                            <th>Email</th>
                            <td>{user['email']}</td>
                        </tr>
                        <tr>
                            <th>Username</th>
                            <td>{user['username']}</td>
                        </tr>
                    </table>
                    """,
                    unsafe_allow_html=True
                )


                st.write("---")
                # Edit Profile
                if st.button("Edit Profile"):
                    st.session_state.editing_profile = True
            
            # Logout
            if st.button("Logout"):
                st.session_state.user_id = None
                st.session_state.user_type = None
                st.success("Logged out successfully.")

        connection.close()
    else:
        st.warning("Please log in to view your profile.")

if __name__ == "__main__":
    main()
