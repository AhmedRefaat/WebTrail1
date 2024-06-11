from django.shortcuts import render, redirect
from .models import Job
from common_utils import logger
import random, time
from django.urls import reverse
from django.http import HttpResponseRedirect


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

def math_home (request):
    context = {}
    return render(request, 'job/home.html', context)

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


def generate_math_problem(problem_types, difficulty, multiplication_difficulty=None, division_difficulty=None):
    operators = {
        'addition': '+',
        'subtraction': '-',
        'multiplication': '*',
        'division': '/',
    }
    selected_type = random.choice(problem_types)

    if selected_type in ['addition', 'subtraction']:
        operand1 = random.randint(1, difficulty)
        operand2 = random.randint(1, difficulty)
        if selected_type == 'subtraction':
            operand1, operand2 = max(operand1, operand2), min(operand1, operand2)
        problem = f"{operand1} {operators[selected_type]} {operand2}"
        correct_answer = eval(problem)

    elif selected_type == 'multiplication':
        max_val = int(multiplication_difficulty)
        operand1 = random.randint(1, max_val)
        operand2 = random.randint(1, max_val)
        problem = f"{operand1} {operators[selected_type]} {operand2}"
        correct_answer = operand1 * operand2

    elif selected_type == 'division':
        divisor = random.randint(1, int(division_difficulty))
        # Ensuring the result is an integer by multiplying the divisor with a random integer
        dividend = divisor * random.randint(1, 10)
        problem = f"{dividend} {operators[selected_type]} {divisor}"
        correct_answer = dividend // divisor

    elif selected_type == '3r-addition':
        operand1 = random.randint(1, difficulty - 2)
        operand2 = random.randint(1, difficulty - operand1 - 1)
        operand3 = random.randint(1, difficulty - operand1 - operand2)
        # Use "\n" to create line breaks after each operand
        problem = f"  {operand1}\n+ {operand2}\n+ {operand3}"
        correct_answer = operand1 + operand2 + operand3

    elif selected_type == '3r-subtraction':
        operand1 = random.randint(2, difficulty)
        operand2 = random.randint(1, operand1 - 1)
        operand3 = random.randint(1, operand1 - operand2)
        subtraction_type = random.choice(['x-y-z', 'x+y-z', 'x-y+z'])
        if subtraction_type == 'x-y-z':
            problem = f"  {operand1}\n- {operand2}\n- {operand3}"
            eval_problem = f"{operand1}- {operand2}- {operand3}"
        elif subtraction_type == 'x+y-z':
            problem = f"  {operand1}\n+ {operand2}\n- {operand3}"
            eval_problem = f"  {operand1}+ {operand2}- {operand3}"
        elif subtraction_type == 'x-y+z':
            problem = f"  {operand1}\n- {operand2}\n+ {operand3}"
            eval_problem = f"{operand1}- {operand2}+ {operand3}"
        correct_answer = eval(eval_problem)

    return problem, correct_answer



def math_problem4(request):

    #Declare a var that will be used on detecting that current problem is 3r problem 
    is_3r_problem = False
    #if math_problem4 view is called as GET outside of "math_home", then redirect to "math_home"
    if request.method == 'GET':
        return redirect('math_home')

    if request.method == 'POST':
        referrer = request.META.get('HTTP_REFERER')
        home_url = request.build_absolute_uri(reverse('math_home'))

        if referrer == home_url:
            # The request comes from the home page, reset the session
            request.session.flush()
            request.session.create()

        parent_pass = request.POST.get('pass', '').lower()
        valid_passwords = ['hebatullah', 'ahmed', 'mohamed', 'asmaa']
        if parent_pass and parent_pass not in valid_passwords:
            return redirect('math_home')

        # Scenario 1: Handle the configuration submission from the "home" view
        if 'difficulty' not in request.session or 'timeout_duration' not in request.session:
            if request.method == 'POST':
                problem_types = request.POST.getlist('problem_types')
                difficulty_str = request.POST.get('difficulty', '10')
                difficulty = int(difficulty_str) if difficulty_str.isdigit() else 10
                # difficulty = int(request.POST.get('difficulty',10))
                timeout_duration = int(request.POST.get('timeout'))
                multiplication_difficulty = request.POST.get('multiplication_difficulty', None)
                division_difficulty = request.POST.get('division_difficulty', None)

                request.session['problem_types'] = problem_types
                request.session['difficulty'] = difficulty
                request.session['timeout_duration'] = timeout_duration
                request.session['multiplication_difficulty'] = multiplication_difficulty
                request.session['division_difficulty'] = division_difficulty
                request.session['Total_count'] = 0
                request.session['correct_count'] = 0
                request.session['wrong_count'] = 0
                request.session['timeout_count'] = 0
                request.session['problems'] = []

    Total_count = request.session.get('Total_count', 0)
    correct_count = request.session.get('correct_count', 0)
    wrong_count = request.session.get('wrong_count', 0)
    timeout_count = request.session.get('timeout_count', 0)
    problems = request.session.get('problems', [])

    if request.method == 'POST':
        user_answer = request.POST.get('answer')
        current_problem = request.session.get('current_problem')
        correct_answer = request.session.get('correct_answer')

        Total_count += 1
        if user_answer and int(user_answer) == correct_answer:
            correct_count += 1
            problems.append({'problem': current_problem, 'correct_answer': correct_answer, 'status': 'correct', 'user_answer': user_answer})
        else:
            if user_answer is not None:  # Handles the case where user_answer is an empty string
                wrong_count += 1
                problems.append({'problem': current_problem, 'correct_answer': correct_answer, 'status': 'incorrect', 'user_answer': user_answer})
            else:
                timeout_count += 1
                problems.append({'problem': current_problem, 'correct_answer': correct_answer, 'status': 'timeout'})

        request.session['Total_count'] = Total_count
        request.session['correct_count'] = correct_count
        request.session['wrong_count'] = wrong_count
        request.session['timeout_count'] = timeout_count
        request.session['problems'] = problems

        if 'finish' in request.POST:
            return redirect('report')

    problem_types = request.session.get('problem_types', [])
    difficulty = request.session.get('difficulty', 0)
    multiplication_difficulty = request.session.get('multiplication_difficulty', None)
    division_difficulty = request.session.get('division_difficulty', None)

    if problem_types:
        current_problem, correct_answer = generate_math_problem(problem_types, difficulty, multiplication_difficulty, division_difficulty)
        if '\n' in current_problem:
            is_3r_problem  = True

    else:
        current_problem, correct_answer = None, None

    request.session['current_problem'] = current_problem
    request.session['correct_answer'] = correct_answer

    context = {
        'problem': current_problem,
        'is_3r_problem': is_3r_problem,  # Replace 'selected_type' with your actual variable
        'timeout_duration': request.session.get('timeout_duration', 0),
        'Total_count': Total_count,
        'correct_count': correct_count,
        'wrong_count': wrong_count,
        'timeout_count': timeout_count,
    }

    return render(request, 'job/math_problem4.html', context)






def math_problem40(request):
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
        logger.LogDebugMsgs(f'Correct Answer: {request.session["correct_count"] } and POSTED answer: {request.POST.get("answer")}')
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
    total_count = request.session.get('Total_count', 0)
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
        'Total_count': total_count,
        'correct_count': correct_count,
        'wrong_count': wrong_count,
        'timeout_count': timeout_count,
        'note': note,
    }
    return render(request, 'job/report.html', context)
