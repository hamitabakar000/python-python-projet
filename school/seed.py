import os
import django
import random
import datetime

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'school.settings')
django.setup()

from home_auth.models import CustomUser
from teacher.models import Teacher
from department.models import Department
from subject.models import Subject
from student.models import Student, Parent
from holiday.models import Holiday
from exam.models import Exam, ExamResult
from timetable.models import Timetable

def seed_data():
    print("Clearing old data...")
    CustomUser.objects.exclude(is_superuser=True).delete() # keep superusers created via createsuperuser
    Teacher.objects.all().delete()
    Student.objects.all().delete()
    Parent.objects.all().delete()
    Department.objects.all().delete()
    Subject.objects.all().delete()
    Holiday.objects.all().delete()
    Exam.objects.all().delete()
    ExamResult.objects.all().delete()
    Timetable.objects.all().delete()
    
    # Re-delete the specific emails just in case
    CustomUser.objects.filter(email__in=['admin@preskool.com', 'teacher@preskool.com', 'student@preskool.com']).delete()

    print("Creating System Users...")
    try:
        admin = CustomUser.objects.create_superuser(
            username='admin', email='admin@preskool.com', password='adminpassword',
            first_name='Admin', last_name='User', is_admin=True
        )
    except Exception:
        pass # Admin might already exist

    CustomUser.objects.create_user(
        username='teacher@preskool.com', email='teacher@preskool.com', password='teacherpassword',
        first_name='John', last_name='Doe', is_teacher=True
    )
    CustomUser.objects.create_user(
        username='student@preskool.com', email='student@preskool.com', password='studentpassword',
        first_name='Alice', last_name='Smith', is_student=True
    )

    departments_data = ["Mathematics", "Computer Science", "Physics", "Chemistry", "Languages", "History"]
    departments = []
    print("Creating Departments...")
    for dept_name in departments_data:
        dept = Department.objects.create(name=dept_name, description=f"{dept_name} Department")
        departments.append(dept)

    print("Creating Teachers...")
    first_names = ["James", "Mary", "John", "Patricia", "Robert", "Jennifer", "Michael", "Linda", "William", "Elizabeth", "David", "Barbara", "Richard", "Susan", "Joseph", "Jessica", "Thomas", "Sarah", "Charles", "Karen"]
    last_names = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis", "Rodriguez", "Martinez", "Hernandez", "Lopez", "Gonzalez", "Wilson", "Anderson"]
    
    teachers = []
    for i in range(1, 13):
        fn = random.choice(first_names)
        ln = random.choice(last_names)
        email = f"{fn.lower()}.{ln.lower()}{i}@preskool.com"
        
        user = CustomUser.objects.create_user(
            username=email, email=email, password='password123',
            first_name=fn, last_name=ln, is_teacher=True
        )
        
        dept = random.choice(departments)
        teacher = Teacher.objects.create(
            teacher_id=f"T{1000+i}",
            first_name=fn, last_name=ln,
            gender=random.choice(['Male', 'Female']),
            date_of_birth=datetime.date(random.randint(1970, 1995), random.randint(1, 12), random.randint(1, 28)),
            mobile_number=f"06{random.randint(10000000, 99999999)}",
            email=email,
            joining_date=datetime.date(random.randint(2015, 2023), random.randint(1, 12), random.randint(1, 28)),
            qualification=random.choice(["Ph.D.", "M.Sc.", "M.A.", "B.Sc."]),
            department=dept
        )
        teachers.append(teacher)

    print("Setting Department Heads...")
    for dept in departments:
        dept_teachers = [t for t in teachers if t.department == dept]
        if dept_teachers:
            dept.head = dept_teachers[0]
            dept.save()

    print("Creating Subjects...")
    subjects_data = {
        "Mathematics": ["Algebra", "Calculus", "Geometry", "Statistics"],
        "Computer Science": ["Programming 101", "Data Structures", "Web Development", "Databases"],
        "Physics": ["Mechanics", "Thermodynamics", "Quantum Physics"],
        "Chemistry": ["Organic Chemistry", "Inorganic Chemistry"],
        "Languages": ["English", "French", "Spanish"],
        "History": ["World History", "Modern History"]
    }
    
    subjects = []
    subject_counter = 100
    for dept_name, sub_list in subjects_data.items():
        dept = next((d for d in departments if d.name == dept_name), departments[0])
        dept_teachers = [t for t in teachers if t.department == dept]
        for sub_name in sub_list:
            subject_counter += 1
            teacher = random.choice(dept_teachers) if dept_teachers else random.choice(teachers)
            sub = Subject.objects.create(
                name=sub_name, code=f"SUB{subject_counter}", department=dept, teacher=teacher
            )
            subjects.append(sub)

    print("Creating Students...")
    classes = ["L1 GINFO", "L2 GINFO", "L3 GINFO", "M1 GINFO", "M2 GINFO"]
    students = []
    
    for i in range(1, 41):
        s_fn = random.choice(first_names)
        s_ln = random.choice(last_names)
        email = f"{s_fn.lower()}.{s_ln.lower()}{i}@student.preskool.com"
        
        CustomUser.objects.create_user(
            username=email, email=email, password='password123',
            first_name=s_fn, last_name=s_ln, is_student=True
        )
        
        parent = Parent.objects.create(
            father_name=f"Mr. {random.choice(first_names)} {s_ln}",
            father_mobile=f"06{random.randint(10000000, 99999999)}",
            mother_name=f"Mrs. {random.choice(first_names)} {s_ln}",
            mother_mobile=f"06{random.randint(10000000, 99999999)}",
            present_address=f"{random.randint(1, 100)} Main St, Cityville",
            permanent_address=f"{random.randint(1, 100)} Main St, Cityville"
        )
        
        student = Student.objects.create(
            student_id=f"S{2000+i}",
            first_name=s_fn, last_name=s_ln,
            gender=random.choice(['Male', 'Female']),
            date_of_birth=datetime.date(random.randint(2000, 2005), random.randint(1, 12), random.randint(1, 28)),
            student_class=random.choice(classes),
            joining_date=datetime.date(random.randint(2020, 2024), 9, 1),
            mobile_number=f"07{random.randint(10000000, 99999999)}",
            admission_number=f"A{10000+i}",
            section=random.choice(["A", "B", "C"]),
            parent=parent
        )
        students.append(student)

    print("Creating Holidays...")
    Holiday.objects.create(name="Summer Vacation", start_date=datetime.date(2025, 7, 1), end_date=datetime.date(2025, 8, 31), holiday_type="School")
    Holiday.objects.create(name="Winter Break", start_date=datetime.date(2025, 12, 20), end_date=datetime.date(2026, 1, 5), holiday_type="School")
    Holiday.objects.create(name="National Day", start_date=datetime.date(2025, 5, 1), end_date=datetime.date(2025, 5, 1), holiday_type="National")
    Holiday.objects.create(name="Spring Break", start_date=datetime.date(2026, 3, 15), end_date=datetime.date(2026, 3, 22), holiday_type="School")

    print("Creating Exams and Results...")
    for class_name in classes:
        for _ in range(2):
            exam_sub = random.choice(subjects)
            exam = Exam.objects.create(
                name=f"{exam_sub.name} Final",
                subject=exam_sub,
                class_name=class_name,
                exam_date=datetime.date(2025, random.randint(5, 6), random.randint(1, 28)),
                start_time=datetime.time(9, 0),
                end_time=datetime.time(11, 0),
                total_marks=100
            )
            class_students = [s for s in students if s.student_class == class_name]
            for student in class_students:
                marks = random.randint(40, 100)
                ExamResult.objects.create(
                    exam=exam, student=student, marks_obtained=marks, remarks="Pass" if marks >= 50 else "Fail"
                )

    print("Creating Timetable...")
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
    for class_name in classes:
        for day in days:
            Timetable.objects.create(
                class_name=class_name, day=day, start_time=datetime.time(8, 0), end_time=datetime.time(10, 0),
                subject=random.choice(subjects), teacher=random.choice(teachers), room=f"Room {random.randint(101, 305)}"
            )
            Timetable.objects.create(
                class_name=class_name, day=day, start_time=datetime.time(10, 15), end_time=datetime.time(12, 15),
                subject=random.choice(subjects), teacher=random.choice(teachers), room=f"Room {random.randint(101, 305)}"
            )

    print("Populated database with dynamic fake data!")

if __name__ == '__main__':
    seed_data()
