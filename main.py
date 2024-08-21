from ticdat import standard_main

from assign_projects.schemas import input_schema, solution_schema
from assign_projects.project_assigner import ProjectAssigner

# command line call "python main.py --input <path to input file or folder> --output <path to output file or folder>"
if __name__ == "__main__":
    standard_main(input_schema, solution_schema, ProjectAssigner.static_solve)
