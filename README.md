# bridging-coursework

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
8. IF there were changes to static elements like images or CSS `python [manage.py](http://manage.py) collectstatic`
9. Reload Web App 

## Testing Code

1. Open Git Bash
2. cd your way to the project directory
3. `source virtualenv/Scripts/activate`
4. `python [manage.py](http://manage.py) test TEST_MODULE_NAMES`
