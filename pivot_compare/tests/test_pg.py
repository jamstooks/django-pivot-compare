from django.db import connection
from django.test import TestCase
from django_pivot.pivot import pivot
from pivot_compare.apps.pg.models import CourseScore
import time

class PGPivotTestCase(TestCase):
    fixtures = ['course_scores_1M']

    def setUp(self):
        self.selected_students = [
            'JAMES', 'JOHN', 'ROBERT', 'MICHAEL', 'MARY']

    def testPivot(self):
        
        print("\n---\nTesting with %d records" % CourseScore.objects.count())
        
        
        # print("---\nUnfiltered Test")
        # qs = CourseScore.objects.all()
        # pt = self.runPivot(qs)
        # self.assertTrue('WILLIAM' in pt[0] and 'course_name' in pt[0])
        
        print("---\nFiltered Test")
        qs = CourseScore.objects.filter(student_name__in=self.selected_students)
        pt = self.runPivot(qs)
        self.assertTrue('WILLIAM' not in pt[0] and 'course_name' in pt[0])

    
    def runPivot(self, qs):
        start_time = time.time()
        pt = pivot(qs, 'course_name', 'student_name', 'score')
        end_time = time.time()
        print("Pivot Query Elapased Time: %.3fs" % (end_time - start_time))
        return pt
