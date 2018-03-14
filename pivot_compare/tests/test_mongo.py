from django.core.management import call_command
from django.test import TestCase
from pivot_compare.apps.grades.models import CourseScore
from subprocess import call
import time

from .base import BasePivotTestMixin

def setUpModule():
    print("\n###\nMongo Test\n###\n")
    start_time = time.time()
    print('loading fixture')

    call(
        "mongorestore pivot_compare/tests/fixtures/mongodump_1M --gzip --quiet",
        shell=True)
    
    # This took 9 hours!
    # call_command(
    #     'loaddata', 
    #     'course_scores_1M.json',
    #     verbosity=0,
    #     database='mongo'
    # )
    print('done loading fixture')
    end_time = time.time()
    print("Elapased Time: %.3fs" % (end_time - start_time))


def tearDownModule():
    # was used to export the data from the pg json fixture
    # call("mongodump --db mongo_auto_test --gzip", shell=True)
    call_command('flush', interactive=False, verbosity=0)


class MongoPivotTestCase(BasePivotTestMixin, TestCase):
    multi_db = True
    # fixtures = ['scores260.mongo.json']

    def setUp(self):
        super(MongoPivotTestCase, self).setUp()
        self.qs = CourseScore.mobjects.db_manager('mongo')
        self.student_names = self.qs.mongo_distinct('student_name')
        self.course_names = self.qs.mongo_distinct('course_name')

    def runPivot(self, num_students, num_courses):

        pipeline = [
            {'$match': {'student_name': {
                '$in': self.student_names[:num_students]}}},
            {'$match': {'course_name': {
                '$in': self.course_names[:num_courses]}}},
            {'$group': {
                '_id': '$student_name',
                'scores': {
                    '$push': {
                        'course_name': '$course_name',
                        'score': '$score'}}}}
        ]
        pt = self.qs.mongo_aggregate(pipeline)
        return pt

    def runValidation(self, pt, num_students, num_courses):
        pt_list = list(pt)
        self.assertEqual(len(pt_list), num_students)
        self.assertEqual(len(pt_list[0]['scores']), num_courses)
