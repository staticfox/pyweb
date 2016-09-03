# Initial setup

 1. Install packages:

    ~~~sh
    sudo apt-get install virtualenv
    ~~~

 2. Create a Python environment:

    ~~~sh
    virtualenv -p python3 venv
    ~~~

 3. Activate the environment for the current shell session:

    ~~~sh
    . venv/bin/activate
    ~~~

    **It is necessary to repeat this command later on if the shell session is
    closed or deactivated.**

 4. Install dependencies:

    ~~~sh
    pip install -r requirements.txt
    ~~~

# Configuration

There are two separate configuration files:

  - `etc/config.py` for server and database configuration
  - `etc/config.yaml` for pysrvx configuration

Examples are found in the `etc` directory.

# Running the development server

 1. Activate the Python environment if necessary (see section "Initial setup").

 2. Run the server as a module:

    ~~~sh
    FLASK_APP=main.py flask run --debugger -h 127.0.0.1 -p 8080
    ~~~
