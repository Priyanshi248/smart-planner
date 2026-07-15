# AI-Powered Smart Planner

An intelligent task management web application that helps users organize their daily activities with AI-powered scheduling recommendations, automated reminders, and secure user authentication.

Built using **Flask**, **SQLite**, and **APScheduler**, the application provides each user with a personalized dashboard where tasks can be created, managed, and intelligently prioritized.

**Live Demo:** https://smart-planner-nvta.onrender.com/

---

## Features

- Secure user authentication (Signup/Login)
- Personalized dashboards with user-specific task management
- Create, update, delete, and restore tasks
- Mark tasks as completed
- AI-powered task scheduling recommendations based on priority
- Automated reminder system using APScheduler
- Task history and status tracking
- Password hashing and session-based authentication
- Deployed on Render

---

## Tech Stack

### Backend

- Python
- Flask

### Database

- SQLite

### Frontend

- HTML
- CSS

### Scheduling

- APScheduler

### Deployment

- Render

---

## Project Structure

```
smart-planner/
│
├── app.py
├── requirements.txt
├── templates/
│   ├── index.html
│   ├── edit.html
│   └── history.html
├── utils/
│   └── ai_scheduler.py
├── static/
├── instance/
│   └── planner.db
└── README.md
```

---

## Key Features

### User Authentication

- User registration and login
- Secure password hashing
- Session management
- Route protection
- Logout functionality

---

### Task Management

Users can

- Create tasks
- Edit existing tasks
- Delete tasks
- Mark tasks as completed
- Restore completed tasks
- View task history

---

### AI-Based Scheduling

The planner recommends an appropriate completion time for each task based on its priority.

Example:

| Priority | Suggested Time |
|-----------|----------------|
| High | As soon as possible |
| Medium | Within the day |
| Low | Flexible schedule |

This helps users organize their workload more effectively.

---

### Reminder System

A background scheduler periodically checks pending tasks and triggers reminders based on user-defined timings.

Powered by **APScheduler**.

---

###  Personalized Dashboard

Each user's tasks are securely isolated using database relationships.

Every task is linked to its owner through a **user_id**, ensuring users can only access their own data.

---

## System Architecture

```
User
   │
   ▼
HTML / CSS Interface
   │
   ▼
Flask Application
   │
   ├── Authentication
   ├── Task Management
   ├── AI Scheduler
   └── Reminder Service
   │
   ▼
SQLite Database
```

---

## Database Schema

### Users

- id
- username
- password (hashed)

### Tasks

- id
- title
- priority
- status
- recommended_time
- task_date
- user_time
- user_id

---

## Installation

Clone the repository

```bash
git clone https://github.com/Priyanshi248/smart-planner.git
```

Move into the project

```bash
cd smart-planner
```

Install dependencies

```bash
pip install -r requirements.txt
```

Run the application

```bash
python app.py
```

Visit

```
http://127.0.0.1:5000
```

---

## Screenshots

- Login Page
<img width="712" height="541" alt="image" src="https://github.com/user-attachments/assets/2861641a-9e90-4b1b-9c91-7e5842b5f9ba" />

- Dashboard
<img width="1905" height="813" alt="image" src="https://github.com/user-attachments/assets/424fa139-d5a3-4849-a96f-11ecafac20ec" />

- Task History
<img width="1851" height="817" alt="image" src="https://github.com/user-attachments/assets/05ae3c5e-9cb5-4119-abf1-4cc47d6f88af" />

---

## Challenges Solved

During development, several real-world issues were resolved:

- Fixed database schema mismatch causing production errors
- Added user-specific data isolation using `user_id`
- Protected routes with session validation
- Improved authentication workflow
- Handled duplicate user registration gracefully
- Integrated background scheduling with APScheduler
- Resolved deployment issues on Render

---

## Future Improvements

- Email reminders
- SMS notifications
- Productivity analytics dashboard
- AI-based priority prediction
- Google Calendar integration
- Dark mode
- Docker support
- CI/CD pipeline

---

## Author

**Priyanshi Saxena**

