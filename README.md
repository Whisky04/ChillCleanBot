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
1. **Choose desired directory.**
In your console change directory to a desired one, where you want the project to be installed.

2. **Clone the Repository.**
Create a SSH-key, if not created yet. Write the following command to install and get a connection to a remote repository:
```bash
git clone git@github.com:Whisky04/ChillCleanBot.git
```
After cloning, the project will be installed in the desired directory on your PC.
   
3. **Check the remote repository connection.**
Write in the same console the following command:
```bash
git remote -v
```
If you see error - ask Danylo.

## Running the Bot

Down here it is described how to run the bot on your machine.

1. **Change working directory.** 
Navigate to a location of a root of the project in your console.

2. **Create a Virtual Environment.**
Write the following command in the console to create a Virtual Environment:
```bash
python -m venv .venv
```

3. **Activate the Virtual Environment.**
Write the following command to activate the Virtual Environment:

For Windows:
```bash
.venv\Scripts\activate
```

For Linux/MacOS:
```bash
source .venv/bin/activate
```

4. **Installation of Project's Dependencies.**
To isntall project's libraries and dependencies, write the following command in the console:
```bash
poetry install
```

5. **Running the Bot.**
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

This section describes how to create a proper naming for a new branch.
  
**Structure of the naming.**

Name the branch in the following way: 
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
