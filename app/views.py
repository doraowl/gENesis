from django.http import HttpResponse
from django.shortcuts import render, redirect
import re
from datetime import datetime
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
import app.forms
import app.models
import json


def home(request):

    if request.user.is_authenticated:

        texts = app.models.Text.objects.filter(user=request.user)
        texts_dict = {}
        tests_dict = {}
        for text in texts:
            texts_dict[text.id] = text.name
            for test in text.test_set.all():
                tests_dict[test.id] = test.name

        return render(request, 'app/hello.html', {'texts': texts_dict, 'tests': tests_dict})
    else:
        return render(request, 'app/hello.html')


def textLoad(request):
    if request.method == 'POST':
        form = app.forms.TextInputForm(request.POST)
        if request.user.is_authenticated:
            if form.is_valid():
                text = form.cleaned_data['text']
                name = form.cleaned_data['name']
                current_user = User.objects.get(id=request.user.id)
                txt = app.models.Text()
                txt.text = text
                txt.name = name
                txt.user = current_user
                txt.save()
                return redirect('textLoad')
    else:
        form = app.forms.TextInputForm()
        texts = app.models.Text.objects.filter(user=request.user)
        texts_dict = {}
        tests_dict = {}
        for text in texts:
            texts_dict[text.id] = text.name
            for test in text.test_set.all():
                tests_dict[test.id] = test.name

        return render(request, 'app/textLoad.html', {'form': form, 'texts': texts_dict, 'tests': tests_dict})


def getText(request, id):
    text = app.models.Text.objects.get(id=id)
    return HttpResponse(
        json.dumps({
            'name': text.name,
            'text': text.text

        }),
        content_type="application/json"
    )


def textShow(request, id):
    if request.user.is_authenticated:
        txt = app.models.Text.objects.get(id=id)
        texts = app.models.Text.objects.filter(user=request.user)
        texts_dict = {}
        tests_dict = {}
        for text in texts:
            texts_dict[text.id] = text.name
            for test in text.test_set.all():
                tests_dict[test.id] = test.name
        return render(request, 'app/textShow.html', {'name': txt.name, 'text': txt.text, 'texts': texts_dict, 'tests': tests_dict})
    else:
        return render(request, 'app/hello.html')


def testShow(request, id):
    if request.user.is_authenticated:
        tst = app.models.Test.objects.get(id=id)
        t_name = tst.name
        tst_dict = {}
        for task in tst.task_set.all():
            taskDict = {}
            taskDict['sentence'] = task.sentence
            taskDict['question'] = task.theme.question
            optionsDict = {}
            for opt in task.option_set.all():
                optDict = {}
                optDict['answer'] = opt.answer
                optDict['corr'] = opt.correctness
                optionsDict[opt.id] = optDict
            taskDict['options'] = optionsDict
            tst_dict[task.id] = taskDict
        texts = app.models.Text.objects.filter(user=request.user)
        texts_dict = {}
        tests_dict = {}
        for text in texts:
            texts_dict[text.id] = text.name
            for test in text.test_set.all():
                tests_dict[test.id] = test.name
        return render(request, 'app/testShow.html', {'tasks': tst_dict, 'texts': texts_dict, 'tests': tests_dict, 'name': t_name})
    else:
        return render(request, 'app/hello.html')


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()

            user = authenticate(
                username=form.cleaned_data['username'], password=form.cleaned_data['password1'],)
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'app/register.html', {'form': form})
