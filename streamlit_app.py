import streamlit as st
import sqlite3
import pandas as pd
st.set_page_config(page_title="Student Records")
st.title("Student Records Website")
# Open or create the database file
conn = sqlite3.connect("students.db")
# Create a table if it does not exist
conn.execute("""
CREATE TABLE IF NOT EXISTS students (
id INTEGER PRIMARY KEY AUTOINCREMENT,
name TEXT NOT NULL,
course TEXT NOT NULL
)
""")
conn.commit()
# Website form
with st.form("student_form"):
name = st.text_input("Student name")
course = st.selectbox(
"Course",
["Python", "Artificial Intelligence", "Web Development"]
)
submitted = st.form_submit_button("Save student")
if submitted:
if name.strip():
conn.execute(
"INSERT INTO students (name, course) VALUES (?, ?)",
(name.strip(), course)
)
conn.commit()
st.success("Student saved!")
st.rerun()
else:
st.warning("Please enter a name.")
# Read and display records
students = pd.read_sql_query(
"SELECT * FROM students ORDER BY id DESC", conn
)
st.subheader("Saved students")
st.dataframe(students, hide_index=True, use_container_width=True)
conn.close()