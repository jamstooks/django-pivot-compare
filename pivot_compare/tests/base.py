import json
import time


class BasePivotTestMixin():
    """
        Base class for testing the performance and accuracy of pivot methods
        from up to 1000 results and 10 colums
    """

    def setUp(self):
        """
        Children must define:
            self.qs - the base queryset of CourseScore objects
            self.student_names - all the available student names
            self.course_names - all the available course names
        """

        self.test_configs = [
            {'num_courses': 5, 'num_students': 10},
            {'num_courses': 10, 'num_students': 100},
            {'num_courses': 20, 'num_students': 1000},
        ]

    def testPivot(self):

        print("\n---\nTesting on %d records" % self.qs.count())

        for config in self.test_configs:
            print("---\nFiltered Test (%d students, %d courses)" % (
                config['num_students'], config['num_courses']))

            start_time = time.time()
            pt = self.runPivot(**config)
            end_time = time.time()
            print("Elapased Time: %.3fs" % (end_time - start_time))

            self.runValidation(
                pt, config['num_students'], config['num_courses'])

            # for o in pt:
            #     print(json.dumps(o, indent=2))
            #     break

    def runPivot(self, num_students, num_courses):
        raise NotImplementedError

    def runValidation(self, pt, num_students, num_courses):
        raise NotImplementedError
