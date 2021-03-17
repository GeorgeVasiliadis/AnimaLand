# AnimaLand

## Optional Main Workflow

1. Stay Organized
1. Brainstorm and Design
1. Develop
1. Test

## Git/ GitHub

### Setting Up
It is highly recommended to use Git Bash, instead of browser-based GitHub web-app. You may download Git Bash [here](https://git-scm.com/downloads).

After installing and configuring Git Bash, open Git Bash under a desired path and type `git clone https://github.com/GeorgeVasiliadis/AnimaLand.git`. This command will create a directory called _AnimaLand_ and it will automatically fetch the latest image to your machine. This is your local workspace.

### Workflow
In order to prevent messing each other's code up, we could follow the following predefined workflow:

1. Use `git pull` to update you local repo.
1. Use `git checkout -b <branchname>` to create a new local branch named _branchname_.
1. Implement the features you have been assigned to.
1. Use `git add <filename1> <filename2> ... <filenameN>` to include only the files contain the implementations you have been working on. Do not include irrelevant files that may have changed.
1. Use `git commit -m "<comments>"` to briefly explain what changes will be introduced to the main repo.
1. Use `git push` to upload committed changes back to main repo.
1. Repeat :)

### General Principles
- Avoid altering the same piece of code (e.g. the same file) while another member of the team is known to be working on it.
- That's all actually :D
