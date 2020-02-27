djbyexblog
=============================

This is a simple blog project. We use docker-containers here, one for django project and one
for postgresql database.


To RUN:

 - conda activate env38_dj_by_ex_blog

 - sudo docker-compose up




 - coverage run -m pytest ==> i perfom it from conda_env, since from docker it
                              it doesnt work yet..To be fixed.

 - to successfully run tests from conda_env we have to be able to run python manage.py runsever 8001
                              from conda_env, so we sure db is running ok.





TODO:

 - run pytest from docker_container itself(now I run it from conda_env)
 - assertContain() doesnt work in tests.

OBSERVATIONS:
 - p.240 (name="Stracchino") to be removed, for logical continuation.
 - p. ___ def test_good_cheese_detail_view(rf, admin_user):
      we dont need admin user here.
