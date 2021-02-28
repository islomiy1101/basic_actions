"""secondproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from secondapp import views
from django.conf import settings
from django.conf.urls.static import static

admin.site.site_title='Action.Uz Admin Paneliga Xush kelibsiz!'
admin.site.index_title='Admin Paneliga Xush kelibsiz'
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.index,name='index'),
    path('rules/<str:name_lang>/',views.rules,name='rules'),
    path('about/',views.aboutpage,name='about'),
    path('contact/',views.contactpage,name='contact'),
    path('signup/',views.register,name='register'),
    path('signup-corporate/',views.register_corporate,name='register_corporate'),
    path('check_user/',views.check_user,name='check_user'),
    path('user_login/',views.user_login,name='user_login'),
    path('student_dash/',views.student_dash,name='student_dash'),
    path('teacher_dash/',views.teacher_dash,name='teacher_dash'),
    path('user_logout/',views.user_logout,name='user_logout'),
    path('edit_profile/',views.edit_profile,name='edit_profile'),
    path('edit_profile_teacher/',views.edit_profile_teacher,name='edit_profile_teacher'),
    path('change_password/',views.change_password,name='change_password'),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('exam_page/<str:name_lang>/',views.exam_page,name='exam_page'),
    path('result/<str:name_lang>/',views.result,name='result'),
    path('sendemail/',views.sendemail,name='sendemail'),
    path('forgot_pass/',views.forgotpass,name='forgot_pass'),
    path('result_section/',views.result_section,name='result_section'),
    path('result_section_country/',views.result_section_country,name='result_section_country'),
    path('result_view/<str:name_lang>/<str:province>/',views.result_view,name='result_view'),
    path('result_view_country/<str:name_lang>/',views.result_view_country,name='result_view_country'),
    path('place_number/',views.place_number,name='place_number'),
    path('place_number_country/',views.place_number_country,name='place_number_country'),
    path('success/',views.success,name='success'),
    path('reset_password/',views.reset_password,name='reset_password'),
    path('search/',views.search,name='search'),
    path('news/',views.news,name='news'),
    path('education_center/',views.education_center,name='education_center'),
    path('languages/',views.languages,name='languages'),
    path('topic/',views.topic,name="topic"),
    path('ielts/',views.ielts,name="ielts"),
    path('hsk/',views.hsk,name="hsk"),
    path('act/',views.act,name="act"),
    path('ap/',views.ap,name="ap"),
    path('ept/',views.ept,name="ept"),
    path('cae/',views.cae,name="cae"),
    path('caeli/',views.caeli,name="caeli"),
    path('duolingo/',views.duolingo,name="duolingo"),
    path('gmat/',views.gmat,name="gmat"),
    path('jlpt/',views.jlpt,name="jlpt"),
    path('klat/',views.klat,name="klat"),
    path('cefr/',views.cefr,name="cefr"),
    path('sat/',views.sat,name="sat"),
    path('toefl/',views.toefl,name="toefl"),
    path('gre/',views.gre,name="gre"),
    path('psat/',views.psat,name="psat")
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
