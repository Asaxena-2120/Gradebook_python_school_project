from sqlalchemy import create_engine
from sqlalchemy import and_ 
from sqlalchemy.orm import sessionmaker
from models import Student, Grade, Course
from tabulate import tabulate

import ipdb

class CLI:
    all_users = set()
    

    def display_menu(self):
        print()
        print("------------------------------------")
        print("1. Add Course")
        print("2. Add Student")
        print("3. Add Grade")
        print("4. View information for a particular student: ")
        print("5. View all courses")
        print("6. View all students")
        print("0. Exit")
        print("------------------------------------")
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
            while True:
                name = (input("Enter the name of the full name (e.g; John Doe) student: "))
                student_id = (input("Enter the student ID: "))
                if student_id.isdigit():
                    choice = self.view_student(name, int(student_id))
                else:   
                    print("Student ID should be an interger.")
                    print()
                    continue
                
                if choice == 0:
                    break

        elif choice == '5':
            # View all courses
            print()
            for course in self.courses:
                print(course.name)
            
        elif choice == '6':
            # View all students
            for student in self.students:
                print(f'{student.id}. {student.name}')
                    
        elif choice == '0':
            print("Exiting the CLI.")
            return False
        else:
            print("Invalid choice. Try again.")
        return True
    
    def menu_for_teachers(self):
        while True:
            self.display_menu()
            choice = input("Enter your choice (0-6): ")
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

    def display_menu_for_student(self,student):
        print()
        print(f'1. Show all the courses for {student.name} is enrolled in ')
        print(f'2. Show all the grades for {student.name} ')
        print(f'3. Show all the statistics for {student.name} ')
        print(f'4. Update score for {student.name} ')
        print(f"5. What to check other student's record? ")
        print(f'0. Return to main menu\n')

    def view_student(self,name,id):
        
        # Instructor can have five incorrect attempts
        
        # check if name and id matches for student, if yes return True else False
        student = session.query(Student).filter(and_(Student.id==id,Student.name==name.title())).first()
        
        if student==None:
            print("You have entered wrong name or id, please try again!!")
            print()
            return

        # handle error if student info is wrong
        print()
        print(f'What information do you want to see for \033[1m{student.name}\033[0m today?"')
        while True:
            self.display_menu_for_student(student)
            choice = int(input("Enter your choice: ")) 
            if choice ==1:
                # display all courses names for the student
                print([grade.course.name for grade in session.query(Grade).filter(Grade.student==student).all()])
            elif choice == 2:
                # Display all the grades for the student
                ([print(f'{grade.course.name}: {grade.score}') for grade in session.query(Grade).filter(Grade.student==student).all()])
            elif choice == 3:
                # Show all the statistics for the student
                pass
            elif choice == 4:
                # Update score for the student
                print()
                course_name= input("Enter the course name for which grade has to be updated: ")
                course_id = session.query(Course).filter(Course.name==course_name).first().id
                updated_score = input("New score: ")
                # get initial grade
                grade = session.query(Grade).filter(Grade.course_id==course_id, Grade.student==student).first()

                # Are you sure you want to update?
                grade.score = updated_score
                confirm = input("Are you sure you want to update? (Y/N)")
                if confirm.lower()=='y':
                    session.commit()
                    print(f"Score has been updated for {course_name} to {updated_score} ")
                else:
                    print("Returning to main menu!")
                    print()
                    return 0
                
            if choice ==5 or choice == 0:
                return choice
                
                

    def add_student(self,name):
        student = Student(name=name.title())
        session.add(student)
        session.commit()
        print(f"Student '{name}' added.")
        
    def add_course(self,name):
        # Check if course is already there in Courses table, if Yes do not add a new course
        course = session.query(Course).filter(Course.name==name)
        if not course:
            course = Course(name=name)
            session.add(course)
            session.commit()
            print(f"Course '{name}' added.")  
        else:
            print("ATTENTION: The course already exists in the database. ")
        return

    def add_grade(course_id, student_id, score):
        # check if student exists
        # check if course exists
        # check if grade is valid integer (0-100)
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