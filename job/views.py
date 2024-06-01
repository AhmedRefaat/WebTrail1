from django.shortcuts import render, redirect
from .models import Job
import random


global timeout_count2
timeout_count2 = 0
timeout_count = 0
initized = False


# Create your views here.

def job_list(request):
    job_list = Job.objects.all()
    context = {'jobs':job_list}
    return render(request, 'job/job_list.html', context)

def job_detail(request, id):
    job_detail = Job.objects.get(id=id)
    context = {'job':job_detail}
    return render(request, 'job/job_detail.html', context)

def Add_Sub_Problems(request):
    problem = get_problem()
    context = {'problem':problem}
    return render(request, 'job/problems1.html', context)


def get_problem():
    problem_args = {}
    problem_args['arg1'] = random.randint(0,100)
    problem_args['arg2'] = random.randint(0,100)
    if random.randint(0,1):
        problem_args['op'] = '+'
    else:
        problem_args['op'] = '-'

    return problem_args

def math_problem1(request):
    global problem_result
    if request.method == 'POST':
        answer = request.POST.get('answer')
        # Check the user's answer and provide feedback
        if int(answer) == problem_result:
            return redirect('success_page')
        else:
            return redirect('math_problem')

    # Generate a simple math problem
    a = random.randint(1, 10)
    b = random.randint(1, 10)
    problem = f"{a} + {b}"
    # global problem_result
    problem_result = a + b

    context = {
        'problem': problem
    }
    return render(request, 'job/math_problem.html', context)

def math_problem2(request):
    global problem_result

    # global timeout_counter
    if request.method == 'POST':
        answer = request.POST.get('answer')
        # Check the user's answer and provide feedback
        if answer != '' and int(answer) == problem_result:
            return redirect('success_page')
        elif answer=="":
            timeout_count2 +=1
            return redirect(math_problem2)

    # Generate a simple math problem
    a = random.randint(1, 10)
    b = random.randint(1, 10)
    problem = f"{a} + {b}"

    problem_result = a + b

    context = {
        'problem': problem,
        'time_limit': 10,  # Configurable time limit in seconds
        'timeout_counter': timeout_count2
    }
    return render(request, 'job/math_problem2.html', context)


def math_problem3(request):
    # Initialize the timeout count
    global timeout_count, initized
    global problem_result
    # initized = False
    # if not initized:
    #     initized = True
    #     timeout_count = 0
    print(f'Number of Timout issues: {timeout_count}')
    if request.method == 'POST':
        answer = request.POST.get('answer')
        # Check the user's answer and provide feedback
        if answer != '' and int(answer) == problem_result:
            return redirect('success_page')
        else:
            timeout_count += 1  # Increment the timeout count
            return redirect(math_problem3)

    # Generate a simple math problem
    a = random.randint(1, 10)
    b = random.randint(1, 10)
    problem = f"{a} + {b}"

    problem_result = a + b

    # Get the configurable time limit from the view function
    time_limit =  3 # Default time limit



    context = {
        'problem': problem,
        'time_limit': time_limit,
        'timeout_count': timeout_count
    }
    return render(request, 'job/math_problem3.html', context)
