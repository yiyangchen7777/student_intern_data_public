'''
The update_students_table.py renew the student information based on the original database student_intern_data.db

Changes:
1. New columns are added, see details in upgrade_database_2024_semester_2.sql created by @Yovela Budiman

2. Create fake students and all revelent information

3. We assign each student with their 'intake' information

4. For our new columns 'remote_internship', 'facilitator_follower', 'listener_or_talker', 'thinker_brainstormer', 'projects_recommended',
   we assign corresponding data 
   
Author: [Yiyang Chen]
Date: [Sep, 2024]
'''
import sqlite3
import random

# Connect to the SQLite database
conn = sqlite3.connect('student_intern_data.db')
cursor = conn.cursor()




# List of projects excluding 'Unassigned'
project_data = [
    'Genomics Metadata Multiplexing',
    'BioNix',
    'Imaging',
    'Clinical Dashboards',
    'Clinical PDFs',
    'Immunology Web',
    'Haemosphere',
    'Research Data Workflows',
    'Quantum Computing',
    'Data Commons',
    'Flux'
]

# Status counts based on the stages of application (where project should be 'unassigned')
early_stage_statuses = {
    '01 Received application': 8,
    '02 Emailed acknowledgement': 8,
    '03 Quick review': 8,
    '04 Initial phone call': 8,
    '05 Added to Round 2 list': 8,
    '06 Interviewed by non-RCP supervisor': 8,
    '07 Offered contact': 8,
    '08 Accepted contract': 7,
    '09 Signed contract': 7
}

# Status counts for other stages where project should not be 'unassigned'
status_counts = {
    '10 Sent to be added to Workday': 7,
    '11 Added to WEHI-wide Teams Group': 7,
    '12 WEHI email created': 7,
    '13 Internship started': 36,
    '14 Finished': 100,
    '15 Ineligible': 12,
    '15 Chose another internship': 5,
    '15 Did not complete': 2,
    '15 Did not reply': 2,
    '15 Was not chosen': 33,
    '15 Withdrew': 12,
    '15 Applied after close': 5
}

# List of intakes
finished_intakes = [
    '1 - Semester 2 2021',
    '2 - Summer 2021/2022',
    '3 - Semester 1 2022',
    '4 - Semester 2 2022',
    '5 - Summer 2022/2023',
    '6 - Semester 1 2023',
    '7 - Semester 2 2023',
    '8 - Summer 2023/2024',
    '9 - Semester 1 2024'
]

# Current intake
default_intake = '10 - Semester 2 2024'

# Values for the additional columns
remote_internship_options = ['yes', 'no']
facilitator_follower_options = ['facilitator', 'follower']
listener_or_talker_options = ['listener', 'talker']
thinker_brainstormer_options = ['thinker', 'brainstormer']

# Handle names and basic details
first_names = ['John', 'Jane', 'Alice', 'Bob', 'Charlie', 'Dana', 'Evan', 'Fiona', 'Grace', 'Hank', 'Ivy', 'Jack', 'Karen', 'Leo', 'Mia', 'Nina', 'Oscar', 'Paul', 'Quincy', 'Rachel']
last_names = ['Doe', 'Smith', 'Johnson', 'White', 'Brown', 'Lee', 'Scott', 'Hill', 'Moore', 'King', 'Clark', 'Miller', 'Davis', 'Martinez', 'Anderson', 'Taylor', 'Thomas', 'Jackson', 'Harris', 'Baker']
fake_names = [f"{first} {last}" for first in first_names for last in last_names]
used_names = set()  # To track used names and avoid duplicates

fake_domain = 'example.com'
pronouns = ['he/him', 'she/her', 'they/them']
courses = ['Engineering and IT', 'Science', 'Engineering']

# Insert or update students in the Students table based on the counts
def assign_project_and_intake(status):
    """Assign project and intake based on status."""
    if status in ['15 Ineligible', '15 Chose another internship', '15 Did not complete', '15 Did not reply', '15 Was not chosen', '15 Withdrew', '15 Applied after close']:
        # If status is any of these, project and intake should be empty
        return None, None
    elif status == '14 Finished':
        # If status is 'Finished', choose from finished_intakes and assign a project
        return random.choice(finished_intakes), random.choice(project_data)
    elif status in early_stage_statuses:
        # If status is early stage, intake is default and project is 'Unassigned'
        return default_intake, 'Unassigned'
    else:
        # For other statuses, assign the default intake and choose a project
        return default_intake, random.choice(project_data)

for status, count in {**early_stage_statuses, **status_counts}.items():
    for _ in range(count):
        # Generate a unique name
        while True:
            name = random.choice(fake_names)
            if name not in used_names:
                used_names.add(name)
                break
        
        pronoun = random.choice(pronouns)
        # Create email based on the student's name, using lowercase first name and last initial
        first_name, last_name = name.split()
        email = f"{first_name.lower()}{last_name[0].lower()}@{fake_domain}"

        mobile = ''.join([str(random.randint(0, 9)) for _ in range(10)])
        course = random.choice(courses)
        
        # Dynamically assign course_major based on course
        if course == 'Engineering and IT':
            course_major = random.choice(['AI', 'Cybersecurity', 'Biomedical Engineering', 'Software Engineering'])
        elif course == 'Science':
            course_major = random.choice(['Biology', 'Data Science', 'Computer Science', 'Chemistry', 'Physics'])
        elif course == 'Engineering':
            course_major = random.choice(['Course Major 1', 'Course Major 2', 'Course Major 3', 'Course Major 4', 'Course Major 5'])
        
        # Check if the student already exists
        cursor.execute('''
            SELECT COUNT(*) FROM Students WHERE email = ?
        ''', (email,))
        result = cursor.fetchone()

        if result[0] == 0:
            # If student doesn't exist, insert the student with all randomly generated data
            intake, project = assign_project_and_intake(status)
            # Randomly assign values for the additional columns
            remote_internship = random.choice(remote_internship_options)
            facilitator_follower = random.choice(facilitator_follower_options)
            listener_or_talker = random.choice(listener_or_talker_options)
            thinker_brainstormer = random.choice(thinker_brainstormer_options)
            projects_recommended = random.choice(project_data)
            cursor.execute('''
                INSERT INTO Students (
                    full_name, pronouns, status, email, mobile, course, course_major, intake, project,
                    remote_internship, facilitator_follower, listener_or_talker, thinker_brainstormer, projects_recommended
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (name, pronoun, status, email, mobile, course, course_major, intake, project, remote_internship, facilitator_follower, listener_or_talker, thinker_brainstormer, projects_recommended))

# Update status == '15 Withdrew' to assign random intake from finished_intakes
cursor.execute('''
    UPDATE Students 
    SET intake = ? 
    WHERE status = '15 Withdrew'
''', (random.choice(finished_intakes),))

# For status == '07 Offered contact', '08 Accepted contract', '09 Signed contract', assign random projects
cursor.execute('''
    UPDATE Students 
    SET project = ? 
    WHERE status IN ('07 Offered contact', '08 Accepted contract', '09 Signed contract')
''', (random.choice(project_data),))

# For status == '12 WEHI email created', set intake to '11 - Summer 2024/2025'
cursor.execute('''
    UPDATE Students 
    SET intake = '11 - Summer 2024/2025' 
    WHERE status = '12 WEHI email created'
''')


# Commit changes and close the connection
conn.commit()
conn.close()

print("Data has been inserted or updated in the database.")
