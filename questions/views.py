from __future__ import unicode_literals

from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .models import Question, Answer
from .forms import QuestionForm, AnswerForm

def question_list(request):
    question_list = Question.objects.all().order_by('-date')
    paginator = Paginator(question_list, 5)

    try:
        page = request.GET.get('page')
        questions = paginator.page(page).object_list
    except PageNotAnInteger:
        page = 1
        questions = paginator.page(page).object_list
    except EmptyPage:
        page = 1
        questions = paginator.page(page).object_list

    return render(request, 'questions/question_list.html', {'title': 'Questions', 'questions': questions, 'paginator': paginator, 'page': paginator.page(page)})

def question(request, questionid):
    question = get_object_or_404(Question, id=questionid)
    title = question.title
    best_answer = None
    if question.answers.filter(best_answer=True).count() is 1:
        best_answer = question.answers.filter(best_answer=True).first()

    form = AnswerForm(request.POST or None)
    if form.is_valid():
        answer = form.save(commit=False)
        answer.author = request.user
        answer.question = question
        answer.save()

        return redirect('question', answer.question.id)

    return render(request, 'questions/answer_new.html', {'title': title, 'question': question, 'form': form, 'best_answer': best_answer})

def question_new(request):
    if request.user.is_authenticated() == False:

        return redirect('signup')

    form = QuestionForm(request.POST or None)
    if form.is_valid():
        question = form.save(commit=False)
        question.author = request.user
        question.save()

        return redirect('question', question.id)

    return render(request, 'questions/question_new.html', {'title': 'Ask a Question', 'form': form})

def question_edit(request, questionid):
    question = get_object_or_404(Question, id=questionid)

    form = QuestionForm(request.POST or None, instance=question)
    if form.is_valid():
        question = form.save(commit=False)
        question.save()

        return redirect('question', question.id)

    return render(request, 'questions/question_new.html', {'title': 'Edit your Question', 'form': form})

def question_delete(request, questionid):
    question = get_object_or_404(Question, id=questionid)
    question.delete()

    return redirect('question_list')

def answer_delete(request, answerid, questionid):
    answer = get_object_or_404(Answer, id=answerid)
    answer.delete()

    return redirect('question', answer.question.id)

def answer_best(request, answerid, questionid):
    answer = get_object_or_404(Answer, id=answerid)

    if answer.best_answer is True:
        answer.best_answer = False
    else:
        answer.best_answer = True
    answer.save()

    return redirect('question', answer.question.id)
