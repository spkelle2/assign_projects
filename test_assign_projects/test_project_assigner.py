import os
import unittest

from assign_projects.schemas import input_schema, solution_schema
from assign_projects.project_assigner import ProjectAssigner


class TestProjectAssigner(unittest.TestCase):

    def setUp(self) -> None:

        # get data directories
        self.input_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'test_inputs')
        self.sln_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'test_solutions')

        # read first placement inputs and expected solutions
        self.first_dat = input_schema.csv.create_tic_dat(os.path.join(self.input_dir, "first_placement"))
        self.first_sln = solution_schema.csv.create_tic_dat(os.path.join(self.sln_dir, "first_placement"))

        # read second placement inputs and expected solutions
        self.second_dat = input_schema.csv.create_tic_dat(os.path.join(self.input_dir, "second_placement"))
        self.second_sln = solution_schema.csv.create_tic_dat(os.path.join(self.sln_dir, "second_placement"))

    def test_static_solve(self):
        # check first model created nets expected results
        sln1 = ProjectAssigner.static_solve(self.first_dat)
        for dept, f in sln1.projects.items():
            # which students get assigned to which department can change but
            # the total number of students assigned to each department should not
            self.assertEqual(f['Number Assigned'], self.first_sln.projects[dept]['Number Assigned'])

        # check second model created nets expected results
        sln2 = ProjectAssigner.static_solve(self.second_dat)
        for dept, f in sln2.projects.items():
            # which students get assigned to which department can change but
            # the total number of students assigned to each department should not
            self.assertEqual(f['Number Assigned'], self.second_sln.projects[dept]['Number Assigned'])


if __name__ == '__main__':
    unittest.main()
