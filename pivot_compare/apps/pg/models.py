from django.db import models

class CourseScore(models.Model):
    """
        This represents the multiple rows that will be
        pivoted to columns...
        
        Course | Student | Score
        ------ | ------- | -----
        A101   | Gary    | 20
        A101   | Cindy   | 21
        
        >>>
        
        Student | A101 Score
        ------- | ----------
        Gary    | 20
        Cindy   | 21
    """
    course_name = models.CharField(max_length=4)
    student_name = models.CharField(max_length=16)
    score = models.IntegerField()
