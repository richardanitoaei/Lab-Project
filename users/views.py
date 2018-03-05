from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.contrib.auth import (
    authenticate,
    get_user_model,
    login,
    logout,
)
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from questions.models import Question, Answer
from .forms import UserLoginForm, UserRegistrationForm

def user_list(request):
    user_list = User.objects.all().order_by('-date_joined')
    paginator = Paginator(user_list, 10)

    try:
        page = request.GET.get('page')
        users = paginator.page(page).object_list
    except PageNotAnInteger:
        page = 1
        users = paginator.page(page).object_list
    except EmptyPage:
        page = 1
        users = paginator.page(page).object_list

    return render(request, 'users/user_list.html', {'title': 'Users', 'users': users, 'paginator': paginator, 'page': paginator.page(page)})

def user_profile(request, userid):
    user = User.objects.filter(id=userid).first()

    if user is None:
        return redirect('/users')

    questions = Question.objects.filter(author=userid).order_by('-date')
    answers = Answer.objects.filter(author=userid).order_by('-date')
    questions_count = questions.count
    answers_count = answers.count
    return render(request, 'users/user_profile.html', {'title': 'User ' + user.username, 'targetuser': user, 'questions': questions[:5], 'answers': answers[:5], 'questions_count': questions_count, 'answers_count': answers_count})

def user_questions(request, userid):
    user = User.objects.filter(id=userid).first()

    if user is None:
        return redirect('/users/')

    questions = Question.objects.filter(author=userid).order_by('-date')
    questions_count = questions.count

    return render(request, 'users/user_questions.html', {'title': 'User' + user.username, 'targetuser': user, 'questions': questions, 'questions_count': questions_count})

def user_answers(request, userid):
    user = User.objects.filter(id=userid).first()

    if user is None:
        return redirect('/users/')

    answers = Answer.objects.filter(author=userid).order_by('-date')
    answers_count = answers.count

    return render(request, 'users/user_answers.html', {'title': 'User' + user.username, 'targetuser': user, 'answers': answers, 'answers_count': answers_count})

def login_view(request):
    if request.user.is_authenticated():

        return redirect('/')

    print(request.user.is_authenticated())

    form = UserLoginForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        login(request, user)

        return redirect(request.GET['next'])

    return render(request, 'users/form.html', {'form': form, 'title': 'Login'})

def signup_view(request):
    if request.user.is_authenticated():

        return redirect('/')

    form = UserRegistrationForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        password = form.cleaned_data.get('password')
        user.set_password(password)
        user.save()

        new_user = authenticate(username=user.username, password=password)
        login(request, new_user)

        return redirect(request.GET['next'])

    return render(request, 'users/form.html', {'form': form, 'title': 'Sign Up'})

def logout_view(request):
    logout(request)

    return redirect(request.GET['next'])
