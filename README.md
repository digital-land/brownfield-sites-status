Brownfield sites validation status
==================================

This application shows a report of the status of brownfield sites validation runs.

It retrieves and displays results of validating browfield register files against this [validator](https://github.com/digital-land/validator-serverless)

Requirements

- [Python 3](https://www.python.org/)
- [Node](https://nodejs.org/en/) and [Npm](https://www.npmjs.com/)
- [Gulp](https://gulpjs.com/)

Getting Started
===============

Install Flask and python dependencies

    pipenv install orpip install -r requirements.txt

Install front end build tool (gulp)

    npm install && gulp scss

Create a db to store cached results

    createdb brownfield_status

Run migrations to set up db

    flask db upgrade

Run the app

    flask run
