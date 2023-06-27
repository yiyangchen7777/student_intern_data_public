import csv
import sqlite3
import sys

"""
    Usage : python import_csv_from_redcap.py <csvfile> <intake>
    Usage : python import_csv_from_redcap.py TestStudentInternshi_DATA_LABELS_2023-06-27_1517.csv "8 - Summer 23/24"
"""




def read_csv_file(file_path,intake):
    with open(file_path, 'r') as csv_file:
        reader = csv.reader(csv_file)
        header = next(reader) 

        conn = sqlite3.connect('../student_intern_data.db')

        for row in reader:
            full_name = row[9]
            pronouns = row[10]
            email_address = row[11]
            mobile_number = row[12]
            faculty_info = row[13]
            course_name = row[14]

            summary_interest_in_projects = ''
            if row[15] == 'Checked':
                summary_interest_in_projects += 'Data Analysis,'
            if row[16] == 'Checked':
                summary_interest_in_projects += 'Data Engineering,'
            if row[17] == 'Checked':
                summary_interest_in_projects += 'Software Engineering'
            summary_interest_in_projects = summary_interest_in_projects.rstrip(',')

            status = '01 Received application'
            data = (
                full_name, pronouns, email_address, mobile_number,
                faculty_info, course_name, summary_interest_in_projects, intake, status
            )
            print(data)
            insert_student_data(conn, data)


def insert_student_data(conn, data):
    cursor = conn.cursor()

    # Insert data into the students table
    cursor.execute('''
        INSERT INTO students (
            full_name, pronouns, email, mobile,
            course, course_major, summary_interest_in_projects,intake, status
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', data)
    conn.commit()

# Provide the path to your CSV file
csv_file_path = sys.argv[1]
intake = sys.argv[2]
read_csv_file(csv_file_path,intake)
