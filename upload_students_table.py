import sqlite3
import random

# Connect to the SQLite database
conn = sqlite3.connect('student_intern_data.db')
cursor = conn.cursor()

# Step 1: Delete all existing rows from the Students table
cursor.execute('DELETE FROM Students')

# student table 
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Students (
        intern_id INTEGER PRIMARY KEY AUTOINCREMENT,
        full_name TEXT,
        pronouns TEXT,
        status TEXT,
        email TEXT,
        mobile TEXT,
        course TEXT,            
        course_major TEXT,
        link_to_application_doc TEXT,
        read_student_handbook TEXT,
        read_student_projects TEXT,
        cover_letter_projects TEXT,
        cover_letter_concept TEXT,
        cover_letter_technical TEXT,
        pronunciation TEXT,
        project TEXT,
        start_date DATE,
        end_date DATE,
        hours_per_week INTEGER,
        intake TEXT,    
        supervisor_email TEXT,
        wehi_email TEXT,
        summary_tech_skills TEXT,
        summary_experience TEXT,
        summary_interest_in_projects TEXT,
        pre_internship_summary_recommendation_external TEXT,
        pre_internship_summary_recommendation_internal TEXT,
        pre_internship_technical_rating TEXT,
        pre_internship_social_rating TEXT,
        pre_internship_learning_quickly TEXT,
        pre_internship_enthusiasm TEXT,
        pre_internship_experience TEXT,
        pre_internship_communication TEXT,
        pre_internship_adaptable TEXT,
        pre_internship_problem_solver TEXT,
        post_internship_comments TEXT,
        post_internship_adaptability TEXT,
        post_internship_learn_technical TEXT,
        post_internship_learn_conceptual TEXT,
        post_internship_collaborative TEXT,
        post_internship_ambiguity TEXT,
        post_internship_complexity TEXT,
        post_internship_summary_rating_internal TEXT,
        post_internship_summary_rating_external TEXT,
        github_username TEXT,
        extra_notes TEXT,
        remote_internship TEXT,
        code_of_conduct TEXT,
        facilitator_follower TEXT,
        listener_or_talker TEXT,
        thinker_brainstormer TEXT,
        why_applied TEXT,
        projects_recommended TEXT
    )
''')

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
default_intake = '10 - Semester 2 2024'

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
            cursor.execute('''
                INSERT INTO Students (
                    full_name, pronouns, status, email, mobile, course, course_major, intake, project
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (name, pronoun, status, email, mobile, course, course_major, intake, project))

# Commit changes and close the connection
conn.commit()
conn.close()

print("Data has been inserted or updated in the database.")
