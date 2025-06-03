# GlucoQuest Backend

The **GlucoQuest Backend** powers the interactive features of the frontend by fetching data, managing APIs, and supporting ML tools. Developed in partnership with **Dexcom** through **PilotCity**, it provides real-world backend experience using modern frameworks and deployment tools.

## Project Goals

- Support frontend with dynamic and interactive content
- Enable AI-powered quizzes and feedback
- Practice backend architecture and API design
- Provide a prototype backend for real-world use

## Features

### RESTful APIs
- Serve quizzes, flashcards, and game and leaderboard data
- Handle user inputs and track progress
- Manage content delivery for games

### AI Quiz Feedback
- Evaluate answers using AI
- Provide instant responses to users

### Session Handling
- Track user progress and interactions
- Lightweight and stateless sessions

## Technical Stack

- **Language:** Python (Flask)
- **Hosting:** Local / AWS
- **Database:** SQLite3
- **CI/CD:** GitHub Actions

## Setup

### Getting Started

> Quick steps that can be used with MacOS, WSL Ubuntu, or Ubuntu; this uses Python 3.9 or later as a prerequisite.

- Open a Terminal, clone a project and `cd` into the project directory.  Use a `different link` and name for `name` for clone to match your repo.

```bash
mkdir -p ~/nighthawk; cd ~/nighthawk

git clone https://github.com/vibha1019/glucoquest_backend.git

cd glucoquest_backend
```

- Install python dependencies for Flask, etc.

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Open project in VSCode

- Prepare VSCode and run
  - From Terminal run VSCode

  ```bash
  code .
  ```

  - Open Setting: Ctrl-Shift P or Cmd-Shift
    - Search Python: Select Interpreter.
    - Match interpreter to `which python` from terminal.
    - Shourd be ./venv/bin/python

  - From Extensions Marketplace install `SQLite3 Editor`
    - Open and view SQL database file `instance/volumes/user_management.db`

  - Make a local `.env` file in root of project to contain your secret passwords

  ```shell
  # User Defaults
  ADMIN_USER='toby'
  ADMIN_PASSWORD='123Toby!'
  DEFAULT_USER='hop'
  DEFAULT_PASSWORD='123Hop!'
  ```

  - Make the database and init data.
  
  ```bash
  ./scripts/db_init.py
  ```

  - Explore newly created SQL database
    - Navigate too instance/volumes
    - View/open `user_management.db`
    - Loook at `Users` table in viewer

  - Run the Project
    - Select/open `main.py` in VSCode
    - Start with Play button
      - Play button sub option contains Debug
    - Click on loop back address in terminal to launch
      - Output window will contain page to launch http://127.0.0.1:8520
    - Login using password
