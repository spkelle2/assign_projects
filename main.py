from ticdat import standard_main

from assign_projects.schemas import input_schema, solution_schema
from assign_projects.project_assigner import ProjectAssigner

if __name__ == "__main__":
    standard_main(input_schema, solution_schema, ProjectAssigner.static_solve)
    