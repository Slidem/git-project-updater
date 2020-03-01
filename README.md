# Git project updater

> Update your maven projects effortlessly

When working with multiple maven projects that depend on each other, it's often very cumbersome to
update each project and choose which dependency to update and wich to leave as it is.

This projects aims to simplify this process, and make the updating of maven git projects very easy for a given user.

# Table of contents

- Motivation
- General info
- The CLI
- The rest APIs
- The GUI
- Tehnologies used

## Motivation

---

When having multiple maven projects, and they depend on each other, in order to know exactly which version of the project is used in which project, and in order to update / build multiple projects without having to manually go into each project's root folder and excute a git / maven command, a tool to automize this came into mind.

## General Info

---

- This project is written in python, and uses a DFS / BFS approach to scan a root folder (where your maven projects exist), and gather information about these projects.
- The projects are presented in a tree - like structure, and illustrates the exact dependencies between your projects inside the defined root folder
- A CLI and a webapp that exposes REST endpoints are also available in order to interact with these projects and perform operations like: read information, build the maven projects, update the git sources, change the version of the projects used in parent projects, etc.

## The CLI

---

The CLI can be run executing the .sh file `run-updater-cli.sh`.
When running the CLI it provides 11 different commands:

    1.  Set project settings
    2.  Print project settings
    3.  List projects
    4.  List project children ids
    5.  Print project dependency tree
    6.  Get project version
    7.  Get project version used in...
    8.  Change project version
    9.  Get project git info
    10. Update project git sources
    11. Build project
    0.  Exit

## The rest APIs

---

> Rest APIs were implemented using the Flask framework.

### Start the REST APIs service

In order to start the REST APIs service, perform the following:

- Go to ./git_project_updater_webapp
- Run pipenv shell by executing: `pipenv shell`
- Execute `flask run`
- Your REST endpoints should be available at http://localhost:5000

### REST endpoints

- GET `/projects` - returns a json array with all your maven project ids
- GET `/projects/settings` - returns a json representation of your project's settings ( to modify your project's settings modify the `settings.json` file in `./git_project_updater_business/settings`)
- GET `/projects/<project_id>/tree` - returns a tree like json representation of the project_id and it's dependencies
- GET `/projects/<project_id>/info` - returns a json representation of the project's detailed info (maven information like artifact, packaging, version..)
- GET `/projects/<project_id>/git` - returns a json representation of the project's GIT information (Current branch, last commit, working directory )
- POST `/projects/<project_id>/build` - performs a maven build on the project_id set on the path
- POST `/projects/<project_id>/git` - performs a git update on the project_id set on the path

## The GUI:

---

The GUI for this app was written as a React web project. The front-end project can be found here:
https://github.com/Slidem/git-project-updater-frontend

## Tehnologies used

---

Project was written in python 3.6+. Required python libraries for this projects can be found in the `requirements.txt` file.

Requirements:

- python 3.6+
- pip (for installing required dependencies)
- python libraries - can be installed through pip: xmltodict, pygit2, flask. nxpy
