from django.db import models
from datetime import datetime

# Create your models here.
class Word(models.Model):
    word = models.CharField(max_length=50)
    meaning = models.CharField(max_length=50)
    en_sentence = models.CharField(max_length=10000000)
    jp_sentence = models.CharField(max_length=10000000)
    created_at = models.DateTimeField(default=datetime.now, blank=True)
    cnt_correct = models.IntegerField(default=0)
    cnt_wrong = models.IntegerField(default=0)

class Ans(models.Model):
    my_ans = models.CharField(max_length=50)
    word = models.CharField(max_length=50)
    meaning = models.CharField(max_length=50)
    en_sentence = models.CharField(max_length=10000000)
    jp_sentence = models.CharField(max_length=10000000)
    created_at = models.DateTimeField(default=datetime.now, blank=True)

class Ans_choice(models.Model):
    ans_id = models.CharField(max_length=50)
    question_id = models.CharField(max_length=50)

class Correct_id(models.Model):
    correct_id = models.CharField(max_length=1000000000)

class Correct_id_choice(models.Model):
    correct_id = models.CharField(max_length=1000000000)