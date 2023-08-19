from http.client import HTTPResponse
from multiprocessing import context
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.db import transaction
from .models import Ans_choice, Correct_id, Correct_id_choice, Word, Ans
import random
import nltk
nltk.download('all')
from nltk.stem.wordnet import WordNetLemmatizer 
import pandas as pd
import os

def index(request):
    return render(request, 'index.html')

def send(request): # 穴埋め問題の正否
    prob_id = request.POST["prob_id"]
    my_ans = request.POST["my_ans"]
    my_ans = my_ans.strip()
    correct_ans = request.POST["correct_ans"]
    correct_ans = correct_ans.strip()

    word = Word.objects.get(id=prob_id).word
    word = word.strip()
    meaning = Word.objects.get(id=prob_id).meaning
    en_sentence = Word.objects.get(id=prob_id).en_sentence
    jp_sentence = Word.objects.get(id=prob_id).jp_sentence

    new_obj = Ans.objects.create(
        word=correct_ans,
        meaning=meaning,
        en_sentence=en_sentence,
        jp_sentence=jp_sentence,
        my_ans=my_ans
    )
    new_obj.save()

    # 正解したのが初めてだったら、Correct_idに追加する
    #with transaction.atomic():
    if correct_ans == my_ans:
        if not Correct_id.objects.filter(correct_id=prob_id).exists():
            #id_obj = Correct_id.objects.create(
            #    correct_id = prob_id
            #)
            #id_obj.save()
            #
            Correct_id.objects.update_or_create(
                correct_id = prob_id
            )
            #
        # 正解したらcnt_correctのカウントを一個増やす
        cnt_correct = Word.objects.get(id=prob_id).cnt_correct
        Word.objects.filter(id=prob_id).update(cnt_correct=cnt_correct+1)
    elif correct_ans != my_ans:
        # 間違えたらcnt_wrongのカウントを一個増やす
        cnt_wrong = Word.objects.get(id=prob_id).cnt_wrong
        Word.objects.filter(id=prob_id).update(cnt_wrong=cnt_wrong+1)

    # 全ての単語を正解したら、正解リスト（correct_id）を初期化して
    # ホームに戻る
    if set(list(Word.objects.values_list("id", flat=True))) == set(list(Correct_id.objects.values_list("correct_id", flat=True))):
        Correct_id.objects.all().delete()
        Ans.objects.all().delete()
        return redirect("")
    else:
        #return render(request, "test.html") # 文章が表示されない
        return redirect("fill")
        
    #return HttpResponse("Answer")

def getResult(request):
    results = Ans.objects.all()
    return JsonResponse({"results": list(results.values())})

def getData(request):
    results = Word.objects.all()
    results_cnt = Word.objects.all().count()
    return JsonResponse({
        "results": list(results.values()),
        "results_cnt": results_cnt,
    })

def getData_wrong(request):
    results = Word.objects.all().order_by("cnt_wrong")
    results_cnt = Word.objects.all().count()
    return JsonResponse({
        "results": list(results.values()),
        "results_cnt": results_cnt,
    })

def fill(request):  # 穴埋め問題の生成
    id_list = Word.objects.values_list("id", flat=True)
    id_list = list(id_list)
    correct_id_list = Correct_id.objects.values_list("correct_id", flat=True)
    correct_id_list = list(map(lambda x: int(x), correct_id_list))
    prob_list = list(set(id_list) - set(correct_id_list))
    if not prob_list:
        Correct_id.objects.all().delete()
        Ans.objects.all().delete()
        return redirect("/")
    random.shuffle(prob_list)
    prob_id = random.choice(prob_list)


    ans_word = Word.objects.get(id=prob_id).word # 答えの単語
    ans_word = ans_word.strip()
    en = Word.objects.get(id=prob_id).en_sentence # 英文
    jp = Word.objects.get(id=prob_id).jp_sentence # 日文
    morph = nltk.word_tokenize(en)
    lemmatizer = WordNetLemmatizer()
    sentence = []
    correct_ans = ""
    for i, w in enumerate(morph):  # 単語を抜いて文章再構成
        original_form = lemmatizer.lemmatize(w, pos="v")
        original_form = original_form.lower()
        if original_form[-1] == "s":
            original_form = lemmatizer.lemmatize(original_form, pos="n")
        if w == ".":
            # 1
            sentence.append(w)
            #
            continue
        elif w == "," and i > 0:
            try:
                sentence[-1] = sentence[-1]+w
            except:
                sentence.append(w)
        elif "\'" in w and i > 0:  # 形態素解析した文字w に ' が含まれていたら前の文字と連結する
            try:
                sentence[-1] = sentence[-1]+w
            except:
                sentence.append(w)
        elif original_form == ans_word or \
            w == ans_word:
            position = i
            correct_ans = w
            w = "□□□□"
            sentence.append(w)
        else:
            # correct_ans = ans_word
            sentence.append(w)
    if correct_ans == "":
        correct_ans = ans_word
    # 1
    # sentence = " ".join(sentence) + "."
    # sentence = " ".join(sentence)
    temp = sentence[0]
    for s in sentence[1:]:
        if s == "." or s == "?":
            temp = temp + s
        else:
            temp = temp + " " + s
    sentence = temp
    # 

    results = Ans.objects.all().order_by("id").reverse()

    context = {
        "prob_list": prob_list,
        "prob_id": prob_id,
        "sentence_blank": sentence,
        "correct_ans": correct_ans,
        "jp": jp,
        "clist": correct_id_list,
        "results": results,
    }
    # return render(request, "test.html", context)
    return render(request, "fill.html", context)

#def checkview(request):
#    pass

def register(request):
    if request.method == "POST":
        word = request.POST["word"]
        word = word.strip()  # 空白を取り除く
        meaning = request.POST["meaning"]
        en_sentence = request.POST["en"]
        jp_sentence = request.POST["jp"]

        if not Word.objects.filter(word=word).exists():
            new_list = Word.objects.create(
                word=word,
                meaning=meaning, 
                en_sentence=en_sentence, 
                jp_sentence=jp_sentence, 
            )
            new_list.save()
            return render(request, "register.html", {"message": "registered"})
        else:
            return render(request, "register.html")
    else:
        return render(request, "register.html")

def registData(request):
    word = request.POST["word"]
    meaning = request.POST["meaning"]
    en_sentence = request.POST["en"]
    jp_sentence = request.POST["jp"]

    if not Word.objects.filter(word=word).exists():
        new_list = Word.objects.create(
            word=word,
            meaning=meaning, 
            en_sentence=en_sentence, 
            jp_sentence=jp_sentence, 
        )
        new_list.save()
    #return HttpResponse('Message sent successfully')
    else:
        return HttpResponse('The word is already registered.')

def toCSV(request):
    word_list = Word.objects.values_list("word", flat=True)
    meaning_list = Word.objects.values_list("meaning", flat=True)
    en_list = Word.objects.values_list("en_sentence", flat=True)
    jp_list = Word.objects.values_list("jp_sentence", flat=True)
    cnt_correct = Word.objects.values_list("cnt_correct", flat=True)
    cnt_wrong = Word.objects.values_list("cnt_wrong", flat=True)
    df = pd.DataFrame({
        "word": word_list,
        "meaning": meaning_list,
        "en": en_list,
        "jp": jp_list,
        "cnt_correct": cnt_correct,
        "cnt_wrong": cnt_wrong,
    })
    path = os.getcwd()
    df.to_csv(path+"/word_list.csv")
    return redirect("register")

def modify(request):
#    if request.method == "POST":
#        id = request.PSOT["id"]
#        word = request.PSOT["word"]
#        meaning = request.PSOT["meaning"]
#        en = request.PSOT["en"]
#        jp = request.PSOT["jp"]
#        Word.objects.filter(id=id).word = word
#        Word.objects.filter(id=id).meaning = meaning
#        Word.objects.filter(id=id).en_sentence = en
#        Word.objects.filter(id=id).jp_sentence = jp
#        Word.save()
#        return HttpResponse("modified")
#
    lists = Word.objects.all().order_by("id").reverse()
    context = {
        "lists": lists,
    }
    return render(request, "modify.html", context)

def search(request):
    # search_word = request.POST.get("search_word") 
    if request.method == "POST":
        search_word = request.POST["search_word"]
        results = Word.objects.filter(word__contains=search_word)
        context = {
            "search_word": search_word,
            "results": results
        }
        # return render(request, "boot_test.html", context)
        return render(request, "modify.html", context)
    else:
        lists = Word.objects.all().order_by("id").reverse()
        context = {
            "lists": lists,
        }
        return render(request, "modify.html", context)
        return render(request, "modify.html")

def update(request, id):
    word = request.POST["word"]
    meaning = request.POST["meaning"]
    en = request.POST["en"]
    jp = request.POST["jp"]
    #Word.objects.filter(id=id).word = word
    #Word.objects.filter(id=id).meaning = meaning
    #Word.objects.filter(id=id).en_sentence = en
    #Word.objects.filter(id=id).jp_sentence = jp
    Word.objects.update_or_create(
        id = id,
        defaults={
        "word": word,
        "meaning": meaning,
        "en_sentence": en,
        "jp_sentence": jp
        }
    )

    context = {
        "id": id,
        "word": word,
        "meaning": meaning,
        "en": en,
        "jp": jp,
    }
    #return render(request, "update.html", context)
    return redirect("modify")

def delete(request):
    if request.method == "POST":
        id = request.POST["id"]
        record = Word.objects.filter(id=id)
        record.delete()
    else:
        return redirect("/")

def choice(request): # 選択問題
    id_list = Word.objects.values_list("id", flat=True)
    id_list = list(id_list)
    correct_id_list = Correct_id_choice.objects.values_list("correct_id", flat=True)
    correct_id_list = list(map(lambda x: int(x), correct_id_list))
    prob_list = list(set(id_list) - set(correct_id_list))
    if not prob_list:
        Correct_id_choice.objects.all().delete()
        Ans.objects.all().delete()
        return redirect("/")
    random.shuffle(prob_list)
    prob_id = random.choice(prob_list)  # 答えのid
    num = 5  # 出題数

    q_list = []
    questions = Word.objects.exclude(id=prob_id).order_by("?")[:num]
    ans = Word.objects.get(id=prob_id)
    q_list.append(ans)
    q_list.extend(questions)
    random.shuffle(q_list)

    try:
        past_ans_id = Ans_choice.objects.order_by("id").last().ans_id
        past_q_id = Ans_choice.objects.order_by("id").last().question_id
        past_ans = Word.objects.get(id=past_ans_id)
    except:
        past_ans_id = ""
        past_q_id = ""
        past_ans = ""

    context = {
        # "prob_id": prob_id,
        "ans": ans,
        "questions": questions,
        "q_list": q_list,
        "past_ans_id": past_ans_id,
        "past_q_id": past_q_id,
        "past_ans": past_ans,
    }
    
    return render(request, "choice.html", context)

def judge(request):
    ans_id = request.POST["ans_id"] # 正解id
    q_id = request.POST["q_id"] # 選択した単語id
    Ans_choice.objects.create( # 正解idと選択idをAns_choiceに保存する
        ans_id = ans_id,
        question_id = q_id,
    ).save()
    # 正解したのが初めてだったら、Correct_id_choiceに追加する
    if ans_id == q_id:
        if not Correct_id_choice.objects.filter(correct_id=ans_id).exists():
            Correct_id_choice.objects.update_or_create(
                correct_id = ans_id
            )
            #
        # 正解したらcnt_correctのカウントを一個増やす
        cnt_correct = Word.objects.get(id=ans_id).cnt_correct
        Word.objects.filter(id=ans_id).update(cnt_correct=cnt_correct+1)
    elif ans_id != q_id:
        # 間違えたらcnt_wrongのカウントを一個増やす
        cnt_wrong = Word.objects.get(id=ans_id).cnt_wrong
        Word.objects.filter(id=ans_id).update(cnt_wrong=cnt_wrong+1)

    # 全ての単語を正解したら、正解リスト（correct_id）を初期化して
    # ホームに戻る
    if set(list(Word.objects.values_list("id", flat=True))) == set(list(Correct_id.objects.values_list("correct_id", flat=True))):
        Correct_id_choice.objects.all().delete()
        return redirect("")
    else:
        return redirect("choice")


def config(request):
    lists = Word.objects.all().order_by("id").reverse()
    context = {
        "lists": lists,
    }
    return render(request, "config.html", context)