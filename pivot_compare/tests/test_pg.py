from django.core.management import call_command
from django.test import TestCase
from django_pivot.pivot import pivot
from pivot_compare.apps.grades.models import CourseScore
import time

from .base import BasePivotTestMixin

def setUpModule():
    print("\n###\nPostgres Test\n###\n")
    start_time = time.time()
    print('loading fixture')
    call_command(
        'loaddata', 
        'course_scores_1M.json',
        verbosity=0,
        database='default'
    )
    print('done loading fixture')
    end_time = time.time()
    print("Elapased Time: %.3fs" % (end_time - start_time))


def tearDownModule():
    call_command('flush', interactive=False, verbosity=0)


class PGPivotTestCase(BasePivotTestMixin, TestCase):
    fixtures = ['course_scores_10K']

    def setUp(self):
        super(PGPivotTestCase, self).setUp()
        self.qs = CourseScore.objects.all()
        self.student_names = self.qs.values_list('student_name').distinct()
        self.course_names = self.qs.values_list('course_name').distinct()

    def runPivot(self, num_students, num_courses):
        qs = self.qs.filter(
            student_name__in=self.student_names[:num_students])
        qs = qs.filter(
            course_name__in=self.course_names[:num_courses])
        pt = pivot(qs, 'student_name', 'course_name', 'score')
        return pt

    def runValidation(self, pt, num_students, num_courses):
        self.assertTrue('Z01' not in pt[0] and 'student_name' in pt[0])
        self.assertEqual(len(pt), num_students)
