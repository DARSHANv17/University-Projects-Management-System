import streamlit as st
import mysql.connector
import io
import tempfile
import base64
from PyPDF2 import PdfReader

def get_domain_id(domain_name):
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="project_db"
    )

    cursor = connection.cursor()
    cursor.execute("SELECT id FROM domains WHERE name=%s", (domain_name,))
    domain_id = cursor.fetchone()[0]
    connection.close()

    return domain_id

def get_projects(user_id):
    # Connect to your MySQL database
    conn = mysql.connector.connect(
        host="localhost",  # Update with your host
        user="root",       # Update with your username
        password="root",   # Update with your password
        database="project_db"
    )

    # Create a cursor
    cursor = conn.cursor()

    # Count the number of projects for each domain of the user
    cursor.execute(f"SELECT domains.name AS domainName, COUNT(projects.id) AS projectCount \
                    FROM projects \
                    LEFT JOIN domains ON projects.domainID = domains.id \
                    WHERE projects.studentID = {user_id} \
                    GROUP BY domains.name")

    domain_projects_count = cursor.fetchall()

    # Fetch project data
    cursor.execute(f"SELECT title, description, file, domainName, status FROM ( \
                    SELECT projects.title, projects.description, projects.file, domains.name AS domainName, projects.status, projects.studentID \
                    FROM projects \
                    LEFT JOIN domains ON projects.domainID = domains.id \
                    LEFT JOIN users ON projects.studentID = users.id) AS subquery \
                    WHERE subquery.studentID = {user_id}")


    projects_data = cursor.fetchall()

    # Close cursor and connection
    cursor.close()
    conn.close()

    return domain_projects_count, projects_data

# Function to display PDF file
def view_pdf(file_data):
    st.subheader("Project File:")

    # Convert bytes to base64 string
    pdf_base64 = base64.b64encode(file_data).decode('utf-8')

    # Use iframe to embed PDF viewer
    pdf_display = f'<iframe src="data:application/pdf;base64,{pdf_base64}" width="700" height="500"></iframe>'
    st.markdown(pdf_display, unsafe_allow_html=True)


def display_projects(user_id, user_type):
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="project_db"
    )

    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM projects WHERE studentID=%s", (user_id,) if user_type == "Student" else "SELECT * FROM projects WHERE facultyID=%s", (user_id,))
    projects = cursor.fetchall()

    if projects:
        st.subheader("My Projects")
        for project in projects:
            st.write(f"Title: {project['title']}")
            st.write(f"Description: {project['description']}")
            st.write(f"Domain: {project['domain']}")
            st.write(f"Status: {project['status']}")
            # Display other project information as needed

            st.write("---")
    else:
        st.info("No projects found.")

    connection.close()

def add_project(user_id):
    st.subheader("Add New Project")

    title = st.text_input("Title")
    description = st.text_area("Description")
    domain_options = ['DBMS', 'AI/ML', 'AR/VR', 'CYBER SECURITY', 'ROBOTICS', 'IOT', 'Other']
    selected_domain = st.selectbox("Domain", domain_options)
    domain_id = get_domain_id(selected_domain)
    file = st.file_uploader("Upload Project File", type=['pdf', 'docx', 'txt'])  # Accepts multiple file types

    if st.button("Submit Project"):
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            database="project_db"
        )

        cursor = connection.cursor()
        cursor.execute(
            "INSERT INTO projects (title, description, domainID, file, studentID, status) VALUES (%s, %s, %s, %s, %s, %s)",
            (title, description, domain_id, file.read() if file else None, user_id, "pending")
        )
        connection.commit()
        connection.close()

        st.success("Project submitted successfully!")

# Function to delete all rejected projects for the logged-in user
def delete_rejected_projects(user_id):
    # Connect to your MySQL database
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="project_db"
    )

    cursor = connection.cursor()

    # Get all rejected projects for the user
    cursor.execute("SELECT id FROM projects WHERE studentID=%s AND status='rejected'", (user_id,))
    rejected_project_ids = [project_id[0] for project_id in cursor.fetchall()]  # Extracting IDs from tuples

    # Delete each rejected project
    for project_id in rejected_project_ids:
        cursor.execute("DELETE FROM comments WHERE projectID=%s", (project_id,))
        cursor.execute("DELETE FROM projects WHERE id=%s", (project_id,))

    # Commit the changes to the database
    connection.commit()

    # Close cursor and connection
    cursor.close()
    connection.close()

def main():
    st.title("My Projects")
    st.write("---")

    user_id = st.session_state.get("user_id")
    user_type = st.session_state.get("user_type")

    if user_id:
        if user_type == "Faculty":
            st.warning("Faculty members cannot view student projects.")
        else:
            domain_projects_count, projects_data = get_projects(user_id)

            if domain_projects_count:
                st.subheader("Number of Projects for Each Domain:")
                for domain_count in domain_projects_count:
                    st.write(f"{domain_count[0]}: {domain_count[1]} projects")
                # Button to delete all rejected projects
            if st.button("Delete All Rejected Projects"):
                user_id = st.session_state.get("user_id")
                if user_id:
                    delete_rejected_projects(user_id)
                    st.success("All rejected projects deleted successfully.")
                else:
                    st.warning("Please log in to delete rejected projects.")
            st.write("---")
            # st.subheader("My Projects")                

            if projects_data:
                    #st.subheader("My Projects")
                
                    # Display each approved project
                    for project in projects_data:
                            st.write(f"**Project Title:** {project[0]}")
                            col1, col2 = st.columns([1, 1])

                            with col1:
                                st.write(f"**Domain:** {project[3]}")

                            with col2:
                                st.write(f"**Status:** {project[4]}")
                            
                            
                            st.write(f"**Description:** {project[1]}")
                            

                            # Display the project file when clicked
                            #st.write(f"**Project File:**")
                            view_pdf(project[2])  # Assuming project[3] contains the file data
                            st.write("---")

            else:
                    st.info("No projects found.")
                
            st.write("---")
            add_project(user_id)
                

    else:
        st.warning("Please log in to view your projects.")

if __name__ == "__main__":
    main()
