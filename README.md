# About

This project is designed as a way to track progress of mentees and provide feedback from both mentors and mentees

## Stack
• Django/Python - backend
• Vue - frontend
• GraphQL (Graphene) - APIs


## Getting Started
• Clone this project
• In the terminal, run `python manage.py makemigrations`, followed by `python manage.py migrate`
• Create a superuser locally to access the admin by running `python manage.py createsuperuser` in the terminal
• To run the server, run `docker-compose up --build`
• To run the front-end, open a new terminal window and run `npm run dev`

## API Endpoints
Endpoints can be found inside of the `mentorship` directory in a file called `api_schema.py`
Since this project uses GraphQL, there is a single endpoint `/graphql`