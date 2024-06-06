from django.shortcuts import render, redirect
from .models import Job
from common_utils import logger
import random, time


global timeout_count2
timeout_count2 = 0
timeout_count = 0
initized = False
Debug_Msg = True


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

    logger.LogDebugMsgs(f'Number of Timout issues222: {timeout_count}')
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


def math_problem4(request):
    # Set the timeout duration (in seconds)
    timeout_duration = 10  # 60 seconds

    # Generate a random math problem
    operand1 = random.randint(1, 10)
    operand2 = random.randint(1, 10)
    operator = random.choice(['+', '-'])
    problem = f"{operand1} {operator} {operand2}"

    # Evaluate the correct answer
    if operator == '+':
        correct_answer = operand1 + operand2
    else:
        # Ensure the answer is never negative
        if operand1 > operand2:
            correct_answer = operand1 - operand2
        else:
            correct_answer = operand2 - operand1

   # Get the counters from the session or initialize them
    if 'correct_count' not in request.session:
        request.session['correct_count'] = 0
    if 'wrong_count' not in request.session:
        request.session['wrong_count'] = 0
    if 'timeout_count' not in request.session:
        request.session['timeout_count'] = 0
    if 'problems' not in request.session:
        request.session['problems'] = []


    correct_count = request.session['correct_count']
    wrong_count = request.session['wrong_count']
    timeout_count = request.session['timeout_count']
    problems = request.session['problems']

    # # Handle the form submission
    # if request.method == 'POST':
    #     if 'finish' in request.POST:
    #         # Redirect to the report page
    #         return redirect('report')
    #     user_answer = request.POST.get('answer', None)
    #     # user_answer = int(request.POST.get('answer', ''))
    #     logger.LogDebugMsgs(f'**********************************************************************************')
    #     logger.LogDebugMsgs(f'UserAnswer: {user_answer} and the correctAnswer: {request.session["correct_answer"]}')
    #     logger.LogDebugMsgs(f'**********************************************************************************')
    #     if (user_answer is not None or user_answer != '' )and user_answer.isdigit():
    #         user_answer = int(user_answer)
    #         # if user_answer == correct_answer:
    #         if user_answer == request.session['correct_answer'] :
    #             correct_count += 1
    #             request.session['correct_count'] = correct_count
    #         else:
    #             wrong_count += 1
    #             request.session['wrong_count'] = wrong_count
    #         problems.append({'problem': problem, 'correct_answer': correct_answer, 'user_answer': user_answer})
    #         request.session['problems'] = problems
    #         request.session['timeout_count'] = timeout_count
    #     else:
    #         # Increment the timeout count if the user didn't submit the form
    #         timeout_count += 1
    #         request.session['timeout_count'] = timeout_count
    #         problems.append({'problem': problem, 'correct_answer': correct_answer, 'user_answer': None})
    #         request.session['problems'] = problems

    # Handle the form submission
    if request.method == 'POST':
        logger.LogDebugMsgs('**********************************************************************')
        logger.LogDebugMsgs(f'POST content: {request.POST}')
        logger.LogDebugMsgs('**********************************************************************')
        if 'finish' in request.POST:
            # Save the current problem and redirect to the report page
            if request.POST.get('answer', '').isdigit():
                user_answer = int(request.POST.get('answer'))
                if user_answer == correct_answer:
                    correct_count += 1
                    request.session['correct_count'] = correct_count
                else:
                    wrong_count += 1
                    request.session['wrong_count'] = wrong_count
            problems.append({'problem': problem, 'correct_answer': correct_answer, 'user_answer': request.POST.get('answer')})
            request.session['problems'] = problems
            request.session['timeout_count'] = 0
            return redirect('report')
        else:
            user_answer_str = request.POST.get('answer', '')
            if user_answer_str.isdigit():
                user_answer = int(user_answer_str)
                if user_answer == correct_answer:
                    correct_count += 1
                    request.session['correct_count'] = correct_count
                else:
                    wrong_count += 1
                    request.session['wrong_count'] = wrong_count
                problems.append({'problem': problem, 'correct_answer': correct_answer, 'user_answer': user_answer})
                request.session['problems'] = problems
            # Reset the timeout count
            request.session['timeout_count'] = 0
    else:
        # Increment the timeout count if the user didn't submit the form
        timeout_count += 1
        request.session['timeout_count'] = timeout_count
        problems.append({'problem': problem, 'correct_answer': correct_answer, 'user_answer': None})
        request.session['problems'] = problems

    if 'correct_answer' not in request.session:
        request.session['correct_answer'] = correct_answer
    request.session['correct_answer'] = correct_answer


    context = {
        'problem': problem,
        'correct_answer': correct_answer,
        'timeout_duration': timeout_duration,
        'correct_count': correct_count,
        'wrong_count': wrong_count,
        'timeout_count': timeout_count,
    }
    return render(request, 'job/math_problem4.html', context)


def report(request):
    problems = request.session.get('problems', [])
    total_problems = len(problems)
    correct_count = request.session.get('correct_count', 0)
    wrong_count = request.session.get('wrong_count', 0)
    timeout_count = request.session.get('timeout_count', 0)

    if total_problems == 0:
        note = 6
    else:
        correct_percentage = (correct_count / total_problems) * 100
        if correct_percentage >= 80:
            note = 1
        elif correct_percentage >= 70:
            note = 2
        elif correct_percentage >= 60:
            note = 3
        elif correct_percentage >= 55:
            note = 4
        elif correct_percentage >= 50:
            note = 5
        else:
            note = 6

    context = {
        'problems': problems,
        'correct_count': correct_count,
        'wrong_count': wrong_count,
        'timeout_count': timeout_count,
        'note': note,
    }
    return render(request, 'job/report.html', context)