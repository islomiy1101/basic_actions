from django.contrib import admin
from secondapp.models import Contact_Us,Register,Question_Lang,Question,AnswerQuestion,PartQuestion,Result,Education,Science,Language,SchoolRegister
from django.utils.safestring import mark_safe
from django.contrib.admin.models import LogEntry

LogEntry.objects.all().delete()

class Contact_UsAdmin(admin.ModelAdmin):
    fields=['contact_number','email','name','subject','message']
    list_display=['id','contact_number','email','name','subject','message','added_on']
    search_fields=['name']
    list_filter=['added_on']
    list_per_page=5
class Question_LangAdmin(admin.ModelAdmin):
    list_display=['name_lang','id','desc']
    list_per_page=6
class QuestionAdmin(admin.ModelAdmin):
    list_display=['id','Savol','answer']
    list_filter=('question_langid','partquestion_id')
    list_per_page=5

class PartQuestionAdmin(admin.ModelAdmin):
    list_display=['Savollar_Bolimi','Tavsifi']
    list_filter=('question_langid',)
    list_per_page=5
class ResultAdmin(admin.ModelAdmin):
    list_display = ['user_id','result']
    list_filter=('question_langid',)
    change_list_template='admin/secondapp/change_list.html'
    list_per_page=5
class AnswerAdmin(admin.ModelAdmin):
    list_display = ['id','ansa','user_id','question_id']
    list_per_page=5
class RegisterTableAdmin(admin.ModelAdmin):
     list_display = ['user_id','provin','city','sert_id','contact_number','balance']
     list_per_page=5


class EducationAdmin(admin.ModelAdmin):
    list_display = ['provin','name', 'address', 'phone', 'website']
    list_per_page = 5

class SchoolRegisterAdmin(admin.ModelAdmin):
    list_display = ['id','school_name']

class ScienceAdmin(admin.ModelAdmin):
    list_display = ['id','name']

class LanguageAdmin(admin.ModelAdmin):
    list_display = ['id','name']
admin.site.register(Science,ScienceAdmin)
admin.site.register(Language,LanguageAdmin)
admin.site.register(SchoolRegister,SchoolRegisterAdmin)
admin.site.register(Education,EducationAdmin)
admin.site.register(Question_Lang,Question_LangAdmin)
admin.site.register(PartQuestion,PartQuestionAdmin)    
admin.site.register(Contact_Us,Contact_UsAdmin)
admin.site.register(Register,RegisterTableAdmin)
admin.site.register(AnswerQuestion,AnswerAdmin)
admin.site.register(Question,QuestionAdmin)
admin.site.register(Result,ResultAdmin)