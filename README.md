# GlucoQuest Backend

The **GlucoQuest Backend** powers the interactive features of the frontend by delivering data, managing APIs, and supporting AI-based tools. Developed by students in partnership with **Dexcom** and **PilotCity**, it provides real-world backend experience using modern frameworks and deployment tools.

## Project Goals

- Support frontend with dynamic and interactive content
- Enable AI-powered quizzes and feedback
- Practice backend architecture and API design
- Provide a prototype backend for real-world use

## Features

### RESTful APIs
- Serve quizzes, flashcards, and game data
- Handle user inputs and track progress
- Manage content delivery for games

### AI Quiz Feedback
- Evaluate answers using OpenAI API
- Provide instant responses to users

### Session Handling
- Track user progress and interactions
- Lightweight and stateless sessions

### Admin Tools
- Upload new content
- Reset or manage game data

## Technical Stack

- **Language:** Python (Flask) or Node.js (Express)
- **Hosting:** Local / Heroku / Render / Fly.io
- **AI Integration:** OpenAI API
- **Database:** (Optional) SQLite or MongoDB
- **CI/CD:** GitHub Actions

## Setup

### Flask (Python)

```bash
pip install -r requirements.txt
python app.py
