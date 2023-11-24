import streamlit as st
import mysql.connector
from PyPDF2 import PdfReader
import io
import tempfile
import base64

# streamlit run 1_🏛️_Projects.py
# Function to fetch projects from the database
def get_projects():
    # Connect to your MySQL database
    conn = mysql.connector.connect(
        host="localhost",  # Update with your host
        user="root",       # Update with your username
        password="root",   # Update with your password
        database="project_db"
    )

    # Create a cursor
    cursor = conn.cursor()

    # Execute a query to fetch projects
    cursor.execute("SELECT projects.id, projects.title, projects.description, projects.file, domains.name AS domainName, users.username AS userName FROM projects \
                   LEFT JOIN domains ON projects.domainID = domains.id \
                   LEFT JOIN users ON projects.studentID = users.id \
                   WHERE projects.status = 'approved'")

    # Fetch project data
    projects_data = cursor.fetchall()

    # Close cursor and connection
    cursor.close()
    conn.close()

    return projects_data

# Function to fetch comments from the database
def get_comments(project_id):
    # Connect to your MySQL database
    conn = mysql.connector.connect(
        host="localhost",  # Update with your host
        user="root",       # Update with your username
        password="root",   # Update with your password
        database="project_db"
    )

    # Create a cursor
    cursor = conn.cursor()

    # Execute a query to fetch comments for a specific project
    cursor.execute("SELECT users.username, comments.text FROM comments \
                   LEFT JOIN users ON comments.studentID = users.id \
                   WHERE comments.projectID = %s", (project_id,))

    # Fetch comment data
    comments_data = cursor.fetchall()

    # Close cursor and connection
    cursor.close()
    conn.close()

    return comments_data

# Function to add a comment to the database
def add_comment(project_id, student_id, comment_text):
    # Check if the user is logged in
    user_id = st.session_state.get("user_id")

    if user_id is None:
        st.warning("Please log in to add a comment.")
        return
    user_type=st.session_state.user_type

    if user_type == "Faculty":
            st.warning("Faculty members cannot comment.")
    else:
            # Connect to your MySQL database
            conn = mysql.connector.connect(
                host="localhost",  # Update with your host
                user="root",       # Update with your username
                password="root",   # Update with your password
                database="project_db"
            )

            # Create a cursor
            cursor = conn.cursor()

            # Execute a query to insert the comment into the database
            cursor.execute("INSERT INTO comments (text, projectID, studentID) VALUES (%s, %s, %s)",
                        (comment_text, project_id, student_id))

            # Commit the changes to the database
            conn.commit()

            # Close cursor and connection
            cursor.close()
            conn.close()

# Function to display PDF file
def view_pdf(file_data):
    st.subheader("Project File:")

    # Convert bytes to base64 string
    pdf_base64 = base64.b64encode(file_data).decode('utf-8')

    # Use iframe to embed PDF viewer
    pdf_display = f'<iframe src="data:application/pdf;base64,{pdf_base64}" width="700" height="500"></iframe>'
    st.markdown(pdf_display, unsafe_allow_html=True)


# Main function
def main():
    st.title('University Projects')
    st.write("---")

    # Call the function to get project data from the database
    projects_data = get_projects()

    # Display each approved project
    for project in projects_data:
# Display project information in a more structured layout
        st.subheader(f"{project[1]}")

# Create columns for project details
        col1, col2 = st.columns([1, 1])

        with col1:
            st.write(f"**Created by:** {project[5]}")

        with col2:
            st.write(f"**Domain:** {project[4]}")

        
        st.write(f"**Description:** {project[2]}")






        # Display the project file when clicked
        #st.write(f"**Project File:**")
        view_pdf(project[3])  # Assuming project[3] contains the file data

        with st.expander("Comments",expanded=False):
        # Comment section
            #st.subheader(f'Comments for Project ID: {project[0]}')

            # Display existing comments for this project
            comments_data = get_comments(project[0])  # project[0] contains the project ID
            for comment in comments_data:
                st.write(f"{comment[0]} : {comment[1]} ")
                st.write("------")
                #st.write(f"**Comment:** ")

            comment_text = st.text_input(f'Add comments:', key=f'comment_{project[0]}')
            if st.button(f'Submit Comment', key=f'comment_button_{project[0]}'):
                # Get the user's ID from session (you need to implement this)
                user_id = st.session_state.get("user_id")  # Replace with the actual user's ID

                # Store the comment in the database
                add_comment(project[0], user_id, comment_text)
        
            # Add a line break for separation
        st.write("---")
        st.write("---")
        

if __name__ == '__main__':
    main()
