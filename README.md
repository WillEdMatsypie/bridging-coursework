# zenith-blog

This Repository holds the code for my website https://zenithos.pythonanywhere.com/

This README is primarily for personal use on how I do certain things to the website while developing

This site was developed following The Django Girls tutorial (https://tutorial.djangogirls.org/en/) and tested following Obey the Testing Goat (https://www.obeythetestinggoat.com/book/preface.html)

## Requirements
- Python 3 (3.6 or greater)
- Django 
- Selenium (For testing)
- geckodriver (For Testing)
- Firefox

## Access Virtual Env for development

1. Open WSL bash console in VS Code
2. Run this command `source myvenv/bin/activate`

## Putting new content on website

1.  Make changes in local Repo
2. `git add` and `git commit` all changes
3. `git push` to remote repository
4. Go to PythonAnywhere
5. Open a console 
6. `cd zenithos.pythonanywhere.com` then `workon zenithos.pythonanywhere.com`
7. `git pull`
8. IF there were changes to static elements like images or CSS `python manage.py collectstatic`
9. IF there were model changes `python manage.py migrate [OPTIONAL: APP_NAME]`
10. Reload Web App 

## Functional Testing the Website
_NOTE: Run Functional Tests separately to Unit Tests_
1. Open Git Bash
2. cd your way to the project directory
3. `source virtualenv/Scripts/activate`
4. `python functional-tests.py` OR `python manage.py test functional-tests`

## Unit Testing Code

1. Within project directory `python manage.py test TEST_MODULE_NAMES`

## Making new apps

1. `python manage.py startapp NAME_OF_APP`
2. Edit mysite/settings.py accordingly

## Making new models

1. Add model to relevant app
2. When complete, in terminal `python manage.py makemigrations [OPTIONAL: APP_NAME]`
3. `python manage.py migrate [OPTIONAL: APP_NAME]`

