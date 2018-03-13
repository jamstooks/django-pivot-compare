from django.conf import settings
import os
from pivot_compare.apps.pg.models import CourseScore
import random
import string


def populate_fixtures():
    """
        Populate the database with ~1 million rows of example data
        to be exported for use as test fixtures
        
        Course | Student | Score
        ------ | ------- | -----
        A01    | Gary    | 20
        A02    | Gary    | 72
        ...    | ...     | ...
    """
    
    filename = os.path.join(
        settings.PROJECT_DIR,
        'tests',
        'static',
        'census-first-names.txt')
    
    count = 0
    MAX_STUDENTS = 2000
    MAX_COURSES = 21
    with open(filename,'r') as f:
        
        print("Removing all existing Course Scores")
        CourseScore.objects.all().delete()
        
        for line in f:
            
            student_name = line.split(None, 1)[0]
            
            count += 1
            if count > MAX_STUDENTS:
                break
            
            course_count = 0
            for char in string.ascii_uppercase:
                for i in range(1, MAX_COURSES):
                    course_name = "%s%02d" % (char, i)
                    score = random.randint(0,100)
                    
                    # print("%s\t%s\t%d" % (
                    #     student_name, course_name, score))

                    cs = CourseScore(
                        course_name=course_name,
                        student_name=student_name,
                        score=score)
                    cs.save()
    
    print("Total Course Scores: %d" % CourseScore.objects.count())
