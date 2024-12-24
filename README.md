## Rules on Contribution
1. When you start working on a new issue, create a new branch. For that, check "Branching Strategy."
2. Pull requests are a must! When you make a contribution, make a pull request and assign Danylo as a reviewer.
3. You are totally free to make any other contribution or additional work, which is not discussed in issues. Just in that case, inform Danylo.
4. Any other question - ask Danylo.

## Requirements

1. Python version 3.11
2. Poetry is installed

## Installation

To get the project on your PC, follow the steps:

1. **Download the ZIP file:**
   Go to the repository page and click on "Code" > "Download ZIP."

2. **Extract the ZIP file:**
   Extract the contents to your desired directory.

3. **Initialize Git in the directory:**
   Open any console and navigate to the project folder. Then run:
   ```bash
   git init
   ```

4. **Add the remote repository:**
   ```bash
   git remote add origin https://github.com/Whisky04/ChillCleanBot.git
   ```

5. **Check the project in VSCode:**
   Open Visual Studio Code and load the project folder to start working on it. Check if you have a connection to the remote repository in Source Control tab. Alternitavely, write in the same console the following command:
   ```bash
   git remote -v
   ```
   If you see error - ask Danylo or ChatGPT

## Running the Bot

Down here it is described how to run the bot on your machine.

1. **Change Working Directiry:** 
   Navigate to the location of the project in your console.

2. **Create a Virtual Environemtn:**
   Write the following command in the console to create a Virtual Environment:
   ```bash
   python -m venv .venv
   ```

3. **Activate the Virtual Environment:**
   Write the following command to activate the Virtual Environment:
   
   For Windows:
   ```bash
   .venv\Scripts\activate
   ```

   For Linux/MacOS:
   ```bash
   source .venv/bin/activate
   ```

4. **Installing of Project's Dependencies:**
   To isntall project's libraries and dependencies, write the following command in the console:
   ```bash
   poetry install
   ```

5. **Running the Bot**
   To initialize and run the bot, write the following in the root directory of the project:
   ```bash
   python main.py
   ```

## Structure of the Project

There are described what are the packages in the project's repository.

- **Database Package**  
  It is where all configurations and relations with database are located.

- **Fucntionalities Package**  
  It is where all base fucntionalities of the bot are located.

- **Menu Package**  
  It is where menu of the bot is described.


## Branching Strategy

This section describes how to create proper naming for a new branch.
  
**Structure of the naming:**
```bash
<prefix>/<issue-id>-<short-description>
```
Where:
- `<prefix>` is one of:
  - `feature` for new features;
  - `bugfix` for bug fixes;
  - `refactor` for code refactoring/customization.
- `<issue-id>` is the ID of the related issue in your issue tracking system.
- `<short-description>` is a brief and hyphenated description of the change.

Examples:
- `feature/123-add-user-authentication`
- `bugfix/456-fix-login-error`
- `refactor/789-optimize-main-menu-code`