djbyexblog
=============================

Some blog project




 - coverage run -m pytest ==> i perfom it from conda_env, since from docker it
                              it doesnt work yet..To be fixed.

 - to successfully run tests from conda_env we have to be able to run python manage.py runsever 8001
                              from conda_env, so we sure db is running ok.





TODO:
 - run pytest from docker_container itself(now I run it from conda_env)
 - assertContain() doesnt work in tests.
