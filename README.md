# homemade_ansible François UTZMANN
Home Made Ansible written in Python using Paramiko And Jinja2

## Prerequisites: 

- Python installed on your local machine
- At least one virtual machine available through SSH
- A list of todos and inventory ready to be treated (You can use the templates that can be found in the /templates directory)

## Installation

**Creating python virtual environment**

- At the root of the project:
```
$ python3 -m venv venv
$ source venv/bin/activate
```
**Build & Install project**
- At the root where the setup.py file is located:
```
$ pip install .
```
**Run Project**
```
hma -f path/to/<todo_list>.yml -i path/to/<inventory>.yml
```


