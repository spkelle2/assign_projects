# project_assigner
The purpose of this repository is to provide a python package for assigning students to
class projects. A user inputs a csv of students with their project preferences
and a csv of projects with their capacities. The package formulates and solves
a mixed-integer linear program to maximize the overall student satisfaction.
The package outputs a csv of the student-project assignments as well as the total
number of students assigned to each project. Details on installing and running
the package can be found below.


### Installation
1. Install [miniconda](https://docs.conda.io/en/latest/miniconda.html) if you
haven't already. Make sure it has been added to path and that it is activated.
You'll know this is the case when you open a terminal tab and you see `(base)`
next to your working directory.
2. Clone this repository.
3. From this project's root directory, create a conda environment from the `environment.yml` file:
    ```bash
    conda env create -f environment.yml
    ```
4. Get a free academic gurobi [license](https://www.gurobi.com/academia/academic-program-and-licenses/).
You can skip the parts on installing Gurobi as the conda environment handled that. You just need to make
sure to run the `grbgetkey` command.

### Usage
1. Activate the conda environment:
    ```bash
    conda activate project_assigner
    ```
2. Create a directory `<path/to/input>` to store the input data files `students.csv`
and `projects.csv`. Input data files should adhere to the data model provided in
`project_assigner/schemas.py`. See `test_assign_projects/test_inputs/first_assignment`
and `test_assign_projects/test_inputs/second_assignment` for examples.
3. From this project's root directory, run the script:
    ```bash
    python main.py --input <path/to/input> --output <path/to/output>
    ```
    For example:
    ```bash
    python main.py --input test_assign_projects/test_inputs/first_assignment --output example_output
    ```

### Common Errors
* To get your Gurobi academic license, you may need to be connected to your
institution's network or create your account with your institution's email.
* If you get an error like "Version number is 11.0, license is for version 10.0"
or "license is expired", try repeating step 4 of Installation
* If you get an error saying "Previous Assignment" or "Previous Choice" are missing
from the students table, add them to the table and try again. It's ok for the columns
to be empty, but the header is required.
