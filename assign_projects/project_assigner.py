import gurobipy as gu

from schemas import input_schema, solution_schema


class ProjectAssigner:

    @staticmethod
    def static_solve(dat: input_schema.TicDat) -> solution_schema.TicDat:
        """ A single function for calling instantiation and solve to make for a nicer UI

        :param dat: a TicDat of projects and students
        :return: A TicDat conforming to solution_schema assigning students to projects
        """
        pa = ProjectAssigner(dat)
        return pa.solve()

    def __init__(self, dat: input_schema.TicDat) -> None:
        """ An object to manage assigning students to projects

        :param dat: a TicDat of projects and students
        :return: None
        """

        self.check_inputs(dat)
        self.dat = dat
        self.mdl, self.x = self.create_model()

    @staticmethod
    def check_inputs(dat: input_schema.TicDat) -> None:
        """ Checks dat to make sure its contents conform to the expectations of
        input_schema

        :param dat: a TicDat of projects and students
        :return: None
        """

        assert input_schema.good_tic_dat_object(dat)
        assert not input_schema.find_foreign_key_failures(dat)
        assert not input_schema.find_data_type_failures(dat)
        assert not input_schema.find_data_row_failures(dat)

    def create_model(self) -> tuple[gu.Model, dict[tuple[str, str], gu.Var]]:
        """ Creates an integer program to assign students to class projects

        :return: the model object and a dictionary mapping student-project
        pairings to a binary variable
        """
        # convert student preferences to penalty weights for the objective
        penalty = {
            (student, project): 0 if f["First Choice"] == project else 1 if
            f["Second Choice"] == project else 2 if f["Third Choice"] == project
            else 4 if f["Last Choice"] == project else 3
            for student, f in self.dat.students.items() for project in self.dat.projects
        }

        # create model
        mdl = gu.Model("assign_projects")

        # create variables
        # x is 1 if student gets assigned to project, 0 else
        x = {(student, project): mdl.addVar(vtype=gu.GRB.BINARY, name=f"assign_{student}_{project}")
             for student in self.dat.students for project in self.dat.projects}

        # y represents half the sum of the students assigned to project
        y = {project: mdl.addVar(vtype=gu.GRB.INTEGER, name=f"half_sum_{project}")
             for project, f in self.dat.projects.items if f["Even Numbered"]}

        # set objective
        # minimize the penalty incurred from the assignment
        mdl.setObjective(gu.quicksum(penalty[student, project] * x[student, project]
                                     for student in self.dat.students for project in self.dat.projects),
                         sense=gu.GRB.MINIMIZE)

        # set constraints
        for project, f in self.dat.projects.items():

            # 1) project must have an acceptable number of students assigned to it
            mdl.addConstr(gu.quicksum(x[student, project] for student in self.dat.students)
                          >= f["Min Capacity"], name=f"{project}_min_cap")
            mdl.addConstr(gu.quicksum(x[student, project] for student in self.dat.students)
                          <= f["Max Capacity"], name=f"{project}_max_cap")

            if f["Even Numbered"]:
                # 2) some projects require an even number of students to be assigned
                mdl.addConstr(gu.quicksum(x[student, project] for student in self.dat.students)
                              == 2 * y[project], name=f"even_numbered_{project}")

        # 3) each student must be assigned to exactly one project
        for student in self.dat.students:
            mdl.addConstr(gu.quicksum(x[student, project] for project in self.dat.projects) == 1,
                          name=f"{student}_assignment")

        return mdl, x

    def solve(self):
        """ Solves an integer program to assign students to class projects

        :return: a TicDat assigning students to projects
        """

        # solve the model
        self.mdl.optimize()
        assert self.mdl.status == gu.GRB.OPTIMAL, "the model should solve to optimality"
        return self.save_solution()

    def save_solution(self) -> solution_schema.TicDat:
        """ Converts integer programming solution to outputs conforming to solution schema

        :return: A TicDat conforming to solution_schema assigning students to projects
        """
        sln = solution_schema.TicDat()
        for student, project in self.x:
            if self.x[student, project].x > 0:
                sln.assignments[student] = {
                    "First Name": self.dat.students[student]["First Name"],
                    "Last Name": self.dat.students[student]["Last Name"],
                    "Project": project
                }
                sln.priority[student] = {
                    "First Name": self.dat.students[student]["First Name"],
                    "Last Name": self.dat.students[student]["Last Name"],
                    "Assigned Choice": "First Choice" if project == self.dat.students[student]["First Choice"]
                    else "Second Choice" if project == self.dat.students[student]["Second Choice"]
                    else "Third Choice" if project == self.dat.students[student]["Third Choice"]
                    else "Last Choice" if project == self.dat.students[student]["Last Choice"]
                    else "Other Choice"
                }
