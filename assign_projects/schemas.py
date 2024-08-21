from ticdat import TicDatFactory

# Define the input schema
student_fields = ["First Name", "Last Name", "First Choice", "Second Choice",
                  "Third Choice", "Last Choice", "Previous Assignment"]
input_schema = TicDatFactory(
    projects=[["Name"], ["Min Capacity", "Max Capacity", "Even Numbered"]],
    students=[["Email"], student_fields + ["Previous Choice"]]
)  # previous choice is what choice was the previous assignment

# Define the foreign key relationships
input_schema.add_foreign_key("students", "projects", ["First Choice", "Name"])
input_schema.add_foreign_key("students", "projects", ["Second Choice", "Name"])
input_schema.add_foreign_key("students", "projects", ["Third Choice", "Name"])
input_schema.add_foreign_key("students", "projects", ["Last Choice", "Name"])
input_schema.add_foreign_key("students", "projects", ["Previous Assignment", "Name"])

# Define the data types
input_schema.set_data_type("projects", "Min Capacity", must_be_int=True)
input_schema.set_data_type("projects", "Max Capacity", must_be_int=True)
input_schema.set_data_type("projects", "Even Numbered", must_be_int=True, max=1,
                           inclusive_max=True)
for f in student_fields:
    input_schema.set_data_type("students", f, number_allowed=False, strings_allowed="*",
                               nullable=True)
possibilities = ("First Choice", "Second Choice", "Third Choice", "Last Choice",
                 "Other Choice", "Did Not Submit First Survey", "Did Not Submit Second Survey")
input_schema.set_data_type("students", "Previous Choice", number_allowed=False,
                           strings_allowed=possibilities, nullable=True)

# We also want to ensure that Max Capacity is at least Min Capacity
input_schema.add_data_row_predicate(
    "projects", predicate_name="Min Max Check",
    predicate=lambda row : row["Max Capacity"] >= row["Min Capacity"])

# define the output schema
solution_schema = TicDatFactory(
    assignments=[["Email"], ["First Name", "Last Name", "Project", "Assigned Choice"]],
    projects=[["Name"], ["Number Assigned"]],
)
