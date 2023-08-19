from django.contrib import admin
from .models import Ans_choice, Correct_id, Word, Ans, Correct_id_choice

# Register your models here.
admin.site.register(Word)
admin.site.register(Ans)
admin.site.register(Ans_choice)
admin.site.register(Correct_id)
admin.site.register(Correct_id_choice)