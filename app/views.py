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
import spacy
import datetime
import random

nlp = spacy.load("en_core_web_sm")
test_preps = ['at', 'in', 'on', 'for', 'by', 'to', 'of']


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


def testSave(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            textid = request.POST['txt']

            test = app.models.Test()
            txt = app.models.Text.objects.get(id=textid)

            test.text = txt
            test.name = txt.name+' '+str(datetime.date.today())
            test.save()

            for i in range(len(request.POST)):

                if 'sentence'+str(i) in request.POST:
                    task = app.models.Task()
                    task.test = test
                    themeid = request.POST['theme'+str(i)]
                    task.theme = app.models.Theme.objects.get(id=themeid)
                    task.sentence = request.POST['sentence'+str(i)]
                    task.save()
                    for j in range(4):
                        opt = app.models.Option()
                        opt.task = task
                        opt.answer = request.POST['answer'+str(i)+str(j)]
                        if 'check'+str(i)+str(j) in request.POST:
                            opt.correctness = True
                        else:
                            opt.correctness = False
                        opt.save()
            return redirect('testShow', id=test.id)


def prepositions(sentences, n, num, text):
    thm = app.models.Theme.objects.get(name='Prepositions')
    tasks = {}

    for sent in sentences:
        allwords = app.models.Token.objects.filter(
            text=text, sentence=sent)
        adps = allwords.filter(
            pos='ADP', tag="IN")

        for prep in adps:
            if n < num and prep.sentence in sentences:
                task = {}
                task['num'] = n
                task['theme'] = thm.id
                task['sent'] = []
                for w in allwords:
                    if w.in_text == prep.in_text:
                        task['sent'].append('___')
                    else:
                        task['sent'].append(w.in_text)
                task['sent'] = " ".join(task['sent'])
                n += 1
                task['options'] = []
                i = 0
                task['options'].append([prep.in_text.lower(), True])
                answers = []
                answers.append(prep.in_text.lower())
                while i < 3:
                    rand = random.choice(test_preps)
                    if rand not in answers:
                        task['options'].append([rand, False])
                        i += 1
                        answers.append(rand)
                random.shuffle(task['options'])
                for i in range(4):
                    task['options'][i].append(i)
                tasks[prep.position] = task
                sentences.remove(prep.sentence)

    return(sentences, tasks, n)


def tenses(sentences, n, num, text):
    pass


'''
    thm = app.models.Theme.objects.get(name='Prepositions')
    tasks = {}

    for sent in sentences:
        allwords = app.models.Token.objects.filter(
            text=text, sentence=sent)
        adps = allwords.filter(
            pos='ADP', tag="IN")

        for prep in adps:
            if n < num and prep.sentence in sentences:
                task = {}
                task['num'] = n
                task['theme'] = thm.id
                task['sent'] = []
                for w in allwords:
                    if w.in_text == prep.in_text:
                        task['sent'].append('___')
                    else:
                        task['sent'].append(w.in_text)
                task['sent'] = " ".join(task['sent'])
                n += 1
                task['options'] = []
                i = 0
                task['options'].append([prep.in_text.lower(), True])
                answers = []
                answers.append(prep.in_text.lower())
                while i < 3:
                    rand = random.choice(test_preps)
                    if rand not in answers:
                        task['options'].append([rand, False])
                        i += 1
                        answers.append(rand)
                random.shuffle(task['options'])
                for i in range(4):
                    task['options'][i].append(i)
                tasks[prep.position] = task
                sentences.remove(prep.sentence)

    return(sentences, tasks, n)'''


def generation(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            form = app.forms.TestGenForm(request.POST)
            tks = {}
            form.fields['text'].choices = [
                (h.id, h.name) for h in app.models.Text.objects.filter(user=request.user)]
            if form.is_valid():
                text = form.cleaned_data['text']
                prepositions_num = int(form.cleaned_data['prepositions'])
                tenses_num = int(form.cleaned_data['tenses'])
                thm = app.models.Theme.objects.get(name='Prepositions')
                txt = app.models.Text.objects.get(id=text)

                tokens = app.models.Token.objects.filter(text=txt)
                sent_count = tokens.order_by('-sentence').first().sentence

                sent_list = []

                for i in range(1, sent_count+1):
                    sent_list.append(i)
                random.shuffle(sent_list)
                n = 0
                sent_list, tasks, n = prepositions(
                    sent_list, n, prepositions_num+n, text)
                sent_list, tasks_t, n = prepositions(
                    sent_list, n, tenses_num+n, text)

            themes = app.models.Theme.objects.all()
            texts = app.models.Text.objects.filter(user=request.user)
            texts_dict = {}
            tests_dict = {}
            themes_dict = {}

            for t in themes:
                themes_dict[t.id] = t.name
            for text in texts:
                texts_dict[text.id] = text.name

                for test in text.test_set.all():
                    tests_dict[test.id] = test.name
            form.fields['text'].choices = [(h.id, h.name) for h in texts]
            return render(request, 'app/generation.html', {'texts': texts_dict, 'tests': tests_dict, 'form': form, 'themes': themes_dict, 'output': tasks, 'txtid': txt.id, 'thmid': thm.id})

    else:
        form = app.forms.TestGenForm()
        themes = app.models.Theme.objects.all()
        texts = app.models.Text.objects.filter(user=request.user)
        texts_dict = {}
        tests_dict = {}
        themes_dict = {}

        for t in themes:
            themes_dict[t.id] = t.name
        for text in texts:
            texts_dict[text.id] = text.name

            for test in text.test_set.all():
                tests_dict[test.id] = test.name
        form.fields['text'].choices = [(h.id, h.name) for h in texts]
        return render(request, 'app/generation.html', {'texts': texts_dict, 'tests': tests_dict, 'form': form, 'themes': themes_dict})


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

                tokens = nlp(text)
                position = 1
                sentence = 1
                for t in tokens:
                    token = app.models.Token()
                    token.in_text = t.text
                    token.lemma = t.lemma_
                    token.pos = t.pos_
                    token.tag = t.tag_
                    token.text = txt
                    token.position = position
                    token.sentence = sentence
                    token.save()
                    position += 1
                    if token.in_text == '.':
                        sentence += 1
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
            # random.shuffle(optionsDict)
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
