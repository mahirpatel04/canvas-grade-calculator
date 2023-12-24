import sys
from canvasapi import Canvas


def CalculateGradeOnPoints(course):
    assignments = course.get_assignments()
    totalPoints = 0
    pointsAchieved = 0
    for assignment in assignments:
        if ((assignment.omit_from_final_grade == False) and (assignment.hide_in_gradebook == False)):
            totalPoints += assignment.points_possible
            
            if (assignment.graded_submissions_exist == True):
                pointsAchieved += assignment.get_submission(account).score
        

    print("TOTAL POINTS ACHIEVABLE: " + str(totalPoints))
    print("TOTAL POINTS ACHIEVED: " + str(pointsAchieved))
    print("YOUR CURRENT PERCENTAGE FOR THIS CLASS IS: " + str(round(((pointsAchieved / totalPoints) * 100), 3)) + "%")
    
def CalculateWeightedGrade(course):
    totalPercentage = 0
    groups = course.get_assignment_groups()
    totals = {}
    for group in groups:
        totals[group.id] = [0, 0, group.group_weight]

        
    assignments = course.get_assignments()
    for assignment in assignments:
        currGroup = course.get_assignment_group((assignment.assignment_group_id))
        
        if ((assignment.omit_from_final_grade == False) and (assignment.hide_in_gradebook == False)):
            if (assignment.graded_submissions_exist == True):
                totals[currGroup.id][0] += assignment.get_submission(account).score
                totals[currGroup.id][1] += assignment.points_possible
                

    for group in totals:
        if (totals[group][1] != 0):
            totalPercentage += totals[group][0] / totals[group][1] * totals[group][2]
    
    print("YOUR CURRENT PERCENTAGE FOR THIS CLASS IS: " + str(round(totalPercentage, 3)) + "%")
    
# Canvas API URL
API_URL = "https://elearn.ucr.edu"
# Canvas API key
API_KEY = "14493~ZvWG92XTxD7gfTh1v5b0mDpgPr2Rp0WkXEU1X0pQG0xrmh6HHAOjaDT06aVc9j1E"

# Initialize a new Canvas object
canvas = Canvas(API_URL, API_KEY)

account = canvas.get_current_user()
print(account.name)

# Validating Courses
    
courses = account.get_courses()
validCourses = []

for course in courses:
    try:
        course.name
        validCourses.append(course)
    except:
        AttributeError
        
        
        
# Ask User which class they want to calculate the grades for
   
print("WHICH CLASS DO YOU WANT TO CALCULATE YOUR GRADES FOR?")
for i in range(len(validCourses)):
    print("[" + str(i+1)  + "] " + validCourses[i].course_code)

classNum = int(input("Enter class number here: ")) - 1
course = validCourses[classNum]
# Calculate and Output GROUPS:


is_weighted = input("Do you want to calculate WEIGHTED GRADE (1) or grade based on ONLY POINTS (2): ")
# Use this function // weight final grade based on assignment group percentages "apply_assignment_group_weights": true
# to automatize this process so we don't need to ask the user
if (is_weighted == "1"):
    CalculateWeightedGrade(course)

elif (is_weighted == "2"):
    CalculateGradeOnPoints(course)

else:
    print("Invalid Input Entered")