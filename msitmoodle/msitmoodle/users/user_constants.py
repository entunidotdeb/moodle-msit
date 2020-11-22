#Region Year Constants

FIRSTYR = 1
SECONDYR = 2
THIRDYR = 3
FOURTHYR = 4

YEAR = (
    (FIRSTYR, "First Year"),
    (SECONDYR, "Second Year"),
    (THIRDYR, "Third Year"),
    (FOURTHYR, "Fourth Year")
)

#Region ends

#Region Semester Constants

FIRSTSEM = 1
SECONDSEM = 2
THIRDSEM = 3
FOURSEM = 4
FIVESEM = 5
SIXSEM = 6
SEVENSEM = 7
EIGHTSEM = 8

SEMESTER = (
    (FIRSTSEM, "First Semester"),
    (SECONDSEM, "Second Semester"),
    (THIRDSEM, "Third Semester"),
    (FOURSEM, "Fourth Semester"),
    (FIVESEM, "Fifth Semester"),
    (SIXSEM, "Sixth Semester"),
    (SEVENSEM, "Seventh Semester"),
    (EIGHTSEM, "Eighth Semester"),
)

#Region ends

#Region Courses/Branches Constants

BTECHIT = 1
BTECHCSE = 2
BTECHECE = 3
BTECHEEE = 4
BTECHCSE2 = 5
BTECHIT2 = 6
BTECHECE2 = 7

COURSES = (
    (BTECHIT, "Bachelors of Technology (IT)"),
    (BTECHCSE, "Bachelors of Technology (CSE)"),
    (BTECHECE, "Bachelors of Technology (ECE)"),
    (BTECHEEE, "Bachelors of Technology (EEE)"),
    (BTECHCSE2, "Bachelors of Technology (CSE Second Shift)"),
    (BTECHIT2, "Bachelors of Technology (IT Second Shift)"),
    (BTECHECE2, "Bachelors of Technology (ECE Second Shift)"),
)

#Region End

#Region Subjects Constants

ET = 1 #Engineering and Technology
PE = 2
ME = 3
MT = 4
AT = 5
EE = 6
EL = 7
IT = 8
CS = 9
CE = 10
EC = 11
EN = 12
TE = 13
MA = 14
HS = 15
SS = 16
PH = 17
CH = 18

SUBJECTS = (
    (PE, "Power Engineering (PE)"),
    (ME, "Mechanical Engineering"),
    (MT, "Mechatronics"),
    (AT, "Mechanical and Automation Engineering"),
    (EE, "Electrical and Electronics Engineering"),
    (EL, "Electrical Engineering"),
    (IT, "Information Technology"),
    (CS, "Computer Science and Engineering"),
    (CE, "Civil Engineering"),
    (EC, "Electronics and Communications Engineering"),
    (EN, "Environmental Engineering"),
    (TE, "Tool Engineering"),
    (MA, "Mathematics"),
    (HS, "Humanities and Social Sciences"),
    (SS, "Social Services"),
    (PH, "Physics"),
    (CH, "Chemistry"),
)

TH = 1
PR = 2

SUB_TYPE = (
    (TH, "Theory"),
    (PR, "Practical"),
)

#End region

#Region Shifts

MOR = 1
EVE = 2

SHIFT = (
    (MOR, "Morning"),
    (EVE, "Evening")
)

#End Region

#Region Profile

TEACHER = 1
PROCTOR = 2
HOD = 3
STUDENT = 4
CR = 5

PROFILE_TYPE = (
    (TEACHER, "Teacher"),
    # (PROCTOR, "Proctor"),
    # (HOD, "HOD"),
    (STUDENT, "Student"),
    # (CR, "Class Representative") 
)
#End Region