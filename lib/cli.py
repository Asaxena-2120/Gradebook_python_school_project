from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Student, Grade, Course
from tabulate import tabulate

import ipdb

class CLI:
    all_users = set()
    

    def display_menu(self):
        print()
        print("1. Add Course")
        print("2. Add Student")
        print("3. Add Grade")
        print("4. View information for a student enter the student's information: ")
        print("0. Exit")
        print()
    
    def __init__(self):
        self.students = session.query(Student).all() #returns list
        self.courses = session.query(Course).all()
        self.grades = session.query(Grade).all()
        self.user_name = ""
        self.roll_number = ""
        self.user_validate = {
            "teacher_code" : "INSTRUCTOR",
            "student_code" : "STUDENT"
        }
        self.everything = {} # Only used by Instructors
        self.course_info = {}
        self.start()

    def process_choice_for_teachers(self,choice):
        if choice == '1':
            name = input("Enter the name of the course: ")
            self.add_course(name)
            
        elif choice == '2':
            name = input("Enter the full name of the student: ")
            self.add_student(name)
        elif choice == '3':
            course_id = int(input("Enter the course ID: "))
            student_id = int(input("Enter the student ID: "))
            score = int(input("Enter the score: "))
            self.add_grade(course_id, student_id, score)
        elif choice == '4':
            name = (input("Enter the name of the student: "))
            student_id = int(input("Enter the student ID: "))
            self.view_student(name, student_id)
        elif choice == '0':
            print("Exiting the CLI.")
            return False
        else:
            print("Invalid choice. Try again.")
        return True
    
    def menu_for_teachers(self):
        while True:
            self.display_menu()
            choice = input("Enter your choice (0-3): ")
            if not self.process_choice_for_teachers(choice):
                break

    
    
    def start(self):
        print("!!!!!!WELCOME TO GRADEBOOK!!!!!!")
        print()

        #Check if the user is an instructor or student
        self.user_name = input("Please enter your name: ")
        password = (input("Please enter your password: ")).upper()
        print()

        if password in self.user_validate.values():

            if password == self.user_validate["teacher_code"]:
                print(f'Hello Instructor {self.user_name}')
                self.menu_for_teachers()

            if password == self.user_validate["student_code"]:
                print(f'Hello Student {self.user_name}')
        else:
            print("Incorrect username or password!!! Please try again!")
            print("Exiting the CLI.")
            print()
            quit()


    def view_student(self,name,id):
        # check if name and id matches for student, if yes return True else False
            

    def add_student(self,name):
        student = Student(name=name)
        session.add(student)
        session.commit()
        print(f"Student '{name}' added.")
        
    def add_course(self,name):
        course = Course(name=name)
        session.add(course)
        session.commit()
        print(f"Course '{name}' added.")  

    def add_grade(course_id, student_id, score):
        grade = Grade(course_id=course_id, student_id=student_id, score=score)
        session.add(grade)
        session.commit()
        print(f"Grade added for Course ID: {course_id}, Student ID: {student_id}, Score: {score}.")


    

    
if __name__=='__main__':
    engine = create_engine('sqlite:///gradebook.db')
    Session = sessionmaker(bind=engine)
    session = Session()
    CLI()
    

#GOALS:
# Search and Filter: Implement search and filter functionality to
# retrieve specific records based on criteria such as student name,
# course name, grade range, etc.

#Make a dictionary stating that if you are a student than you can only see your grades
# If you are a teacher you can see all grades

# Make a class method that validates code

# Make a set that has info about teacher, student and admin, and admin does not require any code returning user

#all(0 can give user history, who all login in)