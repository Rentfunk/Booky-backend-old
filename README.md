# Booky
Booky is a web application for schools trying to manage their books.

The application does not support multiple schools, each school needs it's own installation of this app.


# Developer setup

This guide is for developers **only**.

The first step is to install the requirements to develop on this project.

1.  Make sure you have python 3.8.1, if not then install it seperately.
    You will also require to have pip installed.

2.  Create a virtual enviroment according to this tutorial : https://docs.python.org/3/tutorial/venv.html
    
    Name this virtual enviroment `menv` or have it located seperately from rest of the project, it does *not* belong on the github repo.

3.  Clone the repository into your folder with `git clone https://github.com/SoTeKie/Booky.git`

4.  Install the packages found in requirements.txt
    The command is `pip3 install -r requirements.txt` or `pip install -r requirements.txt`

5.  The settings.py file relies on a `.env` file go to `myproject/myproject` and create a file named `.env` there.

    These are the values that you have to fill in depending on what database you're working with:   SECRET_KEY = 
                                                                                                    DEBUG = 
                                                                                                    ALLOWED_HOSTS= 
                                                                                                    DB_ENGINE = 
                                                                                                    DB_USER = 
                                                                                                    DB_PASS = 
                                                                                                    DB_HOST = 
                                                                                                    DB PORT = 
    For a development enviroment in sqlite3, SECRET_KEY, DEBUG and DB_ENGINE are the only values that need to be filled in.

6.  The master branch is the main development branch that should only be pushed to with merges from other `feature` or `hotfix/bugfix` branches.
    These branches should only be pulled from the master branch, do *NOT* work on a feature/bugfix by pulling from a different feature/bugfix branch,
    pull requests will only be accepted on error-free code that is up to standard.