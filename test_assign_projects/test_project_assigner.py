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
        self.first_dat = input_schema.csv.create_tic_dat(os.path.join(self.input_dir, "first_assignment"))
        self.first_sln = solution_schema.csv.create_tic_dat(os.path.join(self.sln_dir, "first_assignment"))

        # read second placement inputs and expected solutions
        self.second_dat = input_schema.csv.create_tic_dat(os.path.join(self.input_dir, "second_assignment"))
        self.second_sln = solution_schema.csv.create_tic_dat(os.path.join(self.sln_dir, "second_assignment"))

    def test_solve(self):
        """ check that the total penalty for each run matches the value we expect.
        There can be many assignments that are equally "good" so it's ok if which
        project each student is assigned to or the number of students assigned
        to each project changes between runs.

        :return:
        """
        # check first model created nets expected results
        project_assigner = ProjectAssigner(self.first_dat)
        sln = project_assigner.solve()
        penalty = project_assigner._get_penalty(False)
        reported_objective = sum(penalty[student, f["Project"]] for student, f
                                 in sln.assignments.items())
        expected_objective = sum(penalty[student, f["Project"]] for student, f
                                 in self.first_sln.assignments.items())
        actual_objective = project_assigner.mdl.ObjVal
        self.assertEqual(reported_objective, actual_objective)
        self.assertEqual(expected_objective, actual_objective)

        # check second model created nets expected results
        project_assigner = ProjectAssigner(self.second_dat)
        sln = project_assigner.solve()
        penalty = project_assigner._get_penalty(True)  # we have previous assignments this time
        reported_objective = sum(penalty[student, f["Project"]] for student, f
                                 in sln.assignments.items())
        expected_objective = sum(penalty[student, f["Project"]] for student, f
                                in self.second_sln.assignments.items())
        actual_objective = project_assigner.mdl.ObjVal
        self.assertEqual(reported_objective, actual_objective)
        self.assertEqual(expected_objective, actual_objective)


if __name__ == '__main__':
    unittest.main()
