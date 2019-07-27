from django.shortcuts import render, redirect
from .models import Course
import requests
import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

def splash():
    course_objects = list()
    #cis_courses = requests.get("http://api.penncoursereview.com/v1/semesters/2018c/cis?token=public").json()
    departments = requests.get("http://api.penncoursereview.com/v1/semesters/2018c/?token=public").json()
    #contains all of the departments
    departments_list = departments['result']['depts']
    #cis_list = cis_courses['result']['courses']
    for department in departments_list:

        department_name = department['id'].lower()
        #extract all of the courses in a department
        courses = requests.get("http://api.penncoursereview.com/v1/semesters/2018c/" + department_name +"?token=public", verify=False).json()
        course_list = courses['result']['courses']

        #for each course in each department, use api to get info
        for course in course_list:
            try:
                number = course['aliases']
                reviews = requests.get("http://api.penncoursereview.com/v1/courses/2018c-" + number[0] +"/reviews?token=Wt6OyrrlVjEF9F2FjqL3ydnD1SkeDi", verify=False).json()
                gen_info = requests.get("http://api.penncoursereview.com/v1/courses/2018c-" + number[0] +"/?token=Wt6OyrrlVjEF9F2FjqL3ydnD1SkeDi", verify=False).json()


                course_quality = reviews['result']['values'][0]['ratings']['rCourseQuality']
                try:
                    difficulty = reviews['result']['values'][0]['ratings']['rDifficulty']
                except:
                    difficulty = str(None)
                description = gen_info['result']['description']
                name = gen_info['result']['name']

                print(number[0] + '\n' + name + '\n' + "course quality " + course_quality + '\n' + "difficulty " + difficulty + '\n' + description)

                if Course.objects.filter(name=name).count() is 0:
                    course = Course.objects.create(name = name, number = number[0], course_quality = course_quality, difficulty = difficulty,
                        description = description)
                    course_objects.append(course)
            except json.decoder.JSONDecodeError:
                pass
