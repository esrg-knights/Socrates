# Socrates

[![Build Status](https://travis-ci.org/esrg-knights/Socrates.svg)](https://travis-ci.org/esrg-knights/Socrates)

## Prerequisites

For the main project, the following is required:

- Python 2.7 (Installed on path)
- pip (Should be installed with python)

Want to build the react project?

- nodejs (latest)
- npm

## Recommended: Using a virtualenv

It's recommended to use a virtualenv. Use virtualenvwrapper to make it easier


## Main application

### First time set-up

This will install the project

`git clone https://github.com/esrg-knights/Socrates`
`cd Socrates`
`sudo pip install -r requirements.txt`
`python manage.py makemigrations`
`python manage.py migrate`
`python manage.py createsuperuser`

### Running the project

`python manage.py runserver`

Now navigate to [localhost:8000](http://localhost:8000)

## Running the new frontend

### First time setup

`cd assets/react`
`npm install`

### Running frontend

`npm start`

Now navigate to [localhost:7000](http://localhost:7000)

### Building frontend

`npm run build`