import streamlit as st
import mysql.connector
import base64

def view_pdf(file_data):
    st.subheader("Project File:")

    # Convert bytes to base64 string
    pdf_base64 = base64.b64encode(file_data).decode('utf-8')

    # Use iframe to embed PDF viewer
    pdf_display = f'<iframe src="data:application/pdf;base64,{pdf_base64}" width="700" height="500"></iframe>'
    st.markdown(pdf_display, unsafe_allow_html=True)

# Function to fetch pending projects from the database
def get_pending_projects():
    # Connect to your MySQL database
    conn = mysql.connector.connect(
        host="localhost",  # Update with your host
        user="root",       # Update with your username
        password="root",   # Update with your password
        database="project_db"
    )

    # Create a cursor
    cursor = conn.cursor()

    # Execute a query to fetch pending projects
    cursor.execute("SELECT title, description, file, domains.name AS domainName, users.username AS userName , projects.id FROM projects \
                   LEFT JOIN domains ON projects.domainID = domains.id \
                   LEFT JOIN users ON projects.studentID = users.id \
                   WHERE projects.status = 'pending'")

    # Fetch project data
    pending_projects = cursor.fetchall()

    # Close cursor and connection
    cursor.close()
    conn.close()

    return pending_projects

# Function to update the status of a project (approve or reject)
def update_project_status(project_id, new_status):
    # Connect to your MySQL database
    conn = mysql.connector.connect(
        host="localhost",  # Update with your host
        user="root",       # Update with your username
        password="root",   # Update with your password
        database="project_db"
    )

    # Create a cursor
    cursor = conn.cursor()

    # Execute a query to update the project status
    cursor.execute("UPDATE projects SET status = %s WHERE id = %s", (new_status, project_id))

    # Commit the changes to the database
    conn.commit()

    # Close cursor and connection
    cursor.close()
    conn.close()

# Main function
def main():

    st.title('Check Pending Projects')
    st.write("---")
    user_id = st.session_state.get("user_id")
    user_type = st.session_state.get("user_type")

    if user_id:
        if user_type == "Student":
            st.warning("You don't have access to this page")
        else:
            # Call the function to get pending projects
            pending_projects = get_pending_projects()

            # Display each pending project
            for project in pending_projects:
                st.subheader(f"**Project Title:** {project[0]}")
                col1, col2 = st.columns([1, 1])

                with col1:
                    st.write(f"**Student name:** {project[4]}")

                with col2:
                    st.write(f"**Domain:** {project[3]}")

                st.write(f"**Description:** {project[1]}")

                # Display the project file when clicked
                view_pdf(project[2])  # Assuming project[3] contains the file data

                st.write("---")

                # Buttons for approving and rejecting the project
                col3, col4 = st.columns([1, 1])
                with col3:
                    # Provide a unique key for the "Approve Project" button
                    if st.button(f'Approve Project {project[5]}'):
                        update_project_status(project[5], 'approved')
                        st.success(f"Project ID {project[5]} has been approved.")

                with col4:
                    # Provide a unique key for the "Reject Project" button
                    if st.button(f'Reject Project {project[5]}'):
                        update_project_status(project[5], 'rejected')
                        st.error(f"Project ID {project[5]} has been rejected.")

                # Add a line break for separation
                st.write("---")
                st.write("---")
    else:
        st.warning("Please log in to check.")


if __name__ == '__main__':
    main()
