# fc_assignment
This repository contains the solution to the SDET Assignment

Pre-Requisites for setting up and running the project

1. 'Python' of latest version must be installed along with any supported IDE's(Python IDLE, Pycharm, etc)
2. Latest version 'Git' should be installed in the executor and all the pre-requisites related to git folder initialization and setting up the user account should be done.
3. Clone the source code from the 'main' branch using this command : 'git clone https://github.com/jajaykumar/fc_assignment.git'
4. Install the required python libraries with the following pip commands:
   A) pip install requests
5. Navigate to the source code folder and Run the script 'sdet_assignment_1.py' from command line. (Default call parameters - city_name : Fancode, expected_completion_percentage : 50)
6. To update the parameters, navigate to the 'sdet_assignment_1.py' script from an IDE and update the values in the function call block.

Note : The function 'validate_the_completion_requirement' can be called from the other scripts depending on the use-case and the framework. Ex: If the framework used is a Python Behave BDD Framework, the function can be called with the user defined parameters passed from the 'step definition', which can be executed from a 'BDD Feature' file
