#!/bin/bash

strings=("genai-check-zero-shot" "acme_project" "corp_django_course3_1" "corp_django_course3_2" "corp_django_course3" "acme_project_es" "corp_django_course3_1_es" "corp_django_course3_2_es" "corp_django_course3_es" "iris4friends" "Iris4Friends_es" "corp_django_course1" "corp_django_course1_es" "corp_django_course2_1" "corp_django_course2_1_es" "corp_django_course2_2" "corp_django_course2_2_es" "corp_django_course2" "corp_django_course2_es" "TripleNote_without_tests" "TripleNote_without_tests_es" "TripleNews_without_tests" "TripleNews_without_tests_es" "TripleNote_with_tests" "TripleNote_with_tests_es" "TripleNews" "TripleNews_es" "TripleNote" "TripleNote_es" "TripleNews_with_unit_tests" "TripleNews_with_unit_tests_es" "kittygram_en" "kittygram_es" "Wordicum-1" "Wordicum-1-es" "kittygram_plus_en" "kittygram_plus_es" "kittygram2_en" "kittygram2_es" "python_kittygram2plus" "python_kittygram2plus_es" "api_wordicum" "api_wordicum_es" "python_kittygram_backend" "python_kittygram_backend_es" "python_kittygram_frontend" "python_kittygram_frontend_es" "Wordicum-3" "Wordicum-3-es" "tasks-docker" "python-docker-1" "python-docker-1-es" "python-docker-2" "python-docker-2-es" "movie_review" "what_to_watch" "python-flask-1" "python-flask-movie-review-precode" "python-flask-2" "genai-week1-task2" "genai-advanced-structured-output" "genai-check-self-consistency" "genai-check-cot" "genai-check-few-shot" "backend-developer" "django_logic" "django_basics_1_b2b_experiment" "b2b-backend-on-django" "iris1course" "iris1course_es" "ice-creamology-base-project-structure-es" "django_custom_handlers_task_es" "ice-creamology-first-app_es" "todo_es" "hw04_tests_es" "hw03_forms_es" "hw05_final_es" "hw02_community_es" "hw_python_oop_es" "character_creation_module_es" "calc_and_win_es" "backend_test_homework_es")

for str in "${strings[@]}"; do
    echo "------------------"
    echo $str
    cd "repos/$str"
    git init
    git remote add origin "git@github.com:nebius-academy-templates/$str.git"
    git add .
    git commit -am 'Initial config' --author="Konfuze <art.korsunov@gmail.com>"
    git push --force
    cd ../..
    pwd
    echo "------------------"
done
