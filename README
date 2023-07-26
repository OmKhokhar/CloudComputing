# AWS Music Subscription Application
This repository contains a simple online music subscription application developed using AWS services, including EC2, S3, API Gateway, Lambda, and DynamoDB. The application allows users to register, log in, subscribe to music, query music information, and manage their subscriptions.

## File Structure
The repository has the following file structure:

- Task_1&2
  - a1.json
  - Task_1_2.py
  - Task_1_3.py
  - Task_2.py
- templates
  - index.html
  - login.html
  - mainpage.html
  - register.html
- flaskapp.py
- README.md

## Requirements
To run the application, you need the following:

An AWS account with necessary permissions to use EC2, S3, API Gateway, Lambda, and DynamoDB.
An EC2 instance with Ubuntu Server 20.04/18.04 LTS AMI.
Python and Flask installed on the EC2 instance.

## Getting Started
Set up your virtual environment (optional but recommended):
python3 -m venv venv
source venv/bin/activate

## Install required packages:
pip install Flask boto3

1. Configure AWS credentials on your EC2 instance. You can use the IAM role "LabRole" provided.

2. Create the DynamoDB tables and load initial data:

#### To create the "login" table:
python Task_1&2/Task_1_2.py

#### To create the "music" table and load data from "a1.json":
python Task_1&2/Task_1_3.py

#### Download and upload artist images to S3:
python Task_1&2/Task_2.py

#### Start the Flask server:
python flaskapp.py

Access the application in your web browser using the EC2 instance's public IPv4 DNS (in either https or http).

## Features
Login Page: Users can log in using their email and password. Invalid credentials show an error message.

Register Page: New users can register using their email, username, and password. Existing email addresses show an error message.

Main Page: After logging in, users are redirected to the main page. It consists of three areas:

User Area: Displays the corresponding user's username.
Subscription Area: Shows all the user's subscribed music information, along with artist images. Users can remove subscriptions from this area.
Query Area: Allows users to query music information based on title, year, and artist. Query results are displayed along with artist images, and users can subscribe to music from the query results.
Logout: Users can click the "Logout" link to log out of the application.

### Notes
The application must be fully hosted on the webserver environment using Apache2 or an alternative on the designated EC2 instance.

Elastic Beanstalk is not allowed for deploying the application, and non-standard HTTP ports (other than 80/443) are also not allowed.