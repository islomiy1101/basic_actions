import random
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from secondapp.models import PartQuestion, Contact_Us, Register, Question, AnswerQuestion, Result, \
    Question_Lang, Education, SchoolRegister, Science, Language
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import datetime
import time
from django.core.mail import EmailMessage, send_mail
from django.utils import timezone


def index(request):
    context={}
    data = Question_Lang.objects.filter(id=1)
    for start in data:
        time=start.start_time
        current_time = timezone.now()
        start = time-current_time
        day=str(start)[:2]
        hour=str(start)[9:11]
        minute=str(start)[12:14]
        secund=str(start)[15:17]

        context={'day':day,'hour':hour,'minute':minute,'secund':secund}
    return render(request, 'index.html',context)


#  About template uchun

def aboutpage(request):
    return render(request, 'about.html')


# Contact_Page template uchun


def contactpage(request):
    # bazadagi malumotlarni bitta ozgaruvchiga ozlashtrib templatega junatish

    # Post qilib malumotlarni bazaga saqlash
    if request.method == 'POST':
        country_cod = '+998'
        # post orqali jonatilvotgan qiymatlarni ozgaruvchilarga ozlashtirish
        name = request.POST['name']
        contact = request.POST['contact']
        email = request.POST['email']
        subject = request.POST['subject']
        message = request.POST['message']
        contact_number = country_cod + contact

        data = Contact_Us(name=name, contact_number=contact_number,
                          email=email, subject=subject,
                          message=message)  # Bazadagi tablelar nomini bizadagi yani post dagi qiymatlarni tenglash
        data.save()  # post orqali junatilvotgan qiymatlarni bazaga saqlash

        res = f"Hurmatli {name} Fikringiz uchun katta rahmat 😊"

        return render(request, "index.html", {'status': res})

    return render(request, 'contact.html')


# Ruyxatdan otish qismi uchun Post orqali bazaga yuklash

def register(request):
    country_cod = '+998'
    if request.method == 'POST':  # post orqali jonatilvotgan qiymatlarni ozgaruvchilarga ozlashtirish
        fname = request.POST['fname']
        lname = request.POST['lname']
        gender = request.POST['gtype']
        birth = request.POST['birth']
        uname = request.POST['uname']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        email = request.POST['email']
        cnumber = request.POST['pnumber']
        st = request.POST['state']
        prov = request.POST['province']
        ct = request.POST['district']
        train_center = request.POST['train_center']
        mobnumber = country_cod + cnumber
        mobnumber2 = str(mobnumber[4:6] + '***' + mobnumber[9:13])
        print(mobnumber2)
        usr = User.objects.create_user(uname, email, password1)
        usr.first_name = fname
        usr.last_name = lname
        usr.sert_id = "%05i" % (usr.id,)
        usr.save()
        reg = Register(user=usr, gender=gender, dateofbirth=birth,
                       contact_number=mobnumber, state=st, provin=prov, city=ct, balance=True,
                       training_center=train_center, contact_number2=mobnumber2)
        # Bazadagi tablelar nomini bizadagi yani post dagi qiymatlarni tenglash
        reg.sert_id = "%05i" % (usr.id,)
        reg.save()  # post orqali junatilvotgan qiymatlarni bazaga saqlash

        return render(request, 'register.html',
                      {'status': 'Tabriklaymiz! Hurmatli , {} Siz ro`yxatdan muvaffaqiyatli o`tdingiz'.format(fname)})
        # else:
        # messages.info(request, 'Password not matching')
        # return render(request,'register.html')

    return render(request, 'register.html')


# Login qismi uchun username va passwordni bazadagi malumotlar bn solishtirish
def check_user(request):
    if request.method == 'GET':
        un = request.GET['usern']
        check = User.objects.filter(username=un)
        if len(check) == 1:
            return HttpResponse('Exists')
        else:
            return HttpResponse('No exists')


def user_login(request):
    if request.method == 'POST':
        un = request.POST['email']
        pwd = request.POST['password']

        user = authenticate(username=un, password=pwd)
        if user:
            login(request, user)
            if user.is_superuser:
                return HttpResponseRedirect('/admin')
            elif user.is_staff:
                return HttpResponseRedirect('/teacher_dash')
            else:
                res = HttpResponseRedirect('/')
                if 'rememberme' in request.POST:
                    res.set_cookie('user__id', user.id)
                    res.set_cookie('date_login', datetime.datetime.now())
                return res

        else:
            return render(request, 'index.html', {'status': 'Foydaluvchi nomi yoki paroli xato'})

    return HttpResponse('called')


@login_required
def student_dash(request):
    data = Register.objects.get(user__id=request.user.id)
    return render(request, 'student_dashboard.html', {'data': data})


@login_required
def teacher_dash(request):
    data = SchoolRegister.objects.get(creator__id=request.user.id)
    return render(request, 'teacher_dashboard.html', {'data': data})


@login_required
def user_logout(request):
    logout(request)
    res = HttpResponseRedirect('/')
    res.delete_cookie('user_id')
    res.delete_cookie('date_login')
    return res


def edit_profile(request):
    context = {}
    data = Register.objects.get(user__id=request.user.id)
    context = {'data': data}
    if request.method == 'POST':
        fn = request.POST['fname']
        ln = request.POST['lname']
        em = request.POST['email']
        con = request.POST['contact']
        ct = request.POST['city']
        gen = request.POST['gender']
        occ = request.POST['occ']
        abt = request.POST['about']

        usr = User.objects.get(id=request.user.id)
        usr.first_name = fn
        usr.last_name = ln
        usr.email = em
        usr.save()

        data.contact_number = con
        data.city = ct
        data.gender = gen
        data.occupation = occ
        data.about = abt

        data.save()

        if "image" in request.FILES:
            img = request.FILES["image"]
            data.profile_pic = img
            data.save()

        context['status'] = 'O`zgarishlar muvaffaqiyatli saqlandi'
    return render(request, 'edit_profile.html', context)


def edit_profile_teacher(request):
    context = {}
    data = SchoolRegister.objects.get(creator__id=request.user.id)
    context = {'data': data}
    if request.method == 'POST':
        sn = request.POST['sname']
        pn = request.POST['provin']
        add = request.POST['address']
        science = request.POST['science']
        lang = request.POST['lang']
        contact = request.POST['contact']
        state = request.POST['state']
        website = request.POST['website']
        telegram = request.POST['telegram']
        youtube = request.POST['youtube']
        facebook = request.POST['facebook']
        instagram = request.POST['instagram']
        email = request.POST['email']

        usr = User.objects.get(id=request.user.id)
        usr.first_name =sn
        usr.email = email
        usr.save()

        data.contact_number = contact
        data.provin = pn
        data.address = add
        data.science = science
        data.lang = lang
        data.state = state
        data.website = website
        data.youtube = youtube
        data.facebook = facebook
        data.instagram = instagram
        data.telegram = telegram
        data.save()

        context['status'] = 'O`zgarishlar muvaffaqiyatli saqlandi'
    return render(request, 'edit_profile_teacher.html',context)


def languages(request):
    langs = Question_Lang.objects.all()
    context = {'data': langs}
    if request.method == 'POST':
        name_lang = request.POST['langs']
        user = request.user
        reg = Register.objects.get(user=request.user.id)
        balance = reg.balance
        is_exists = Result.objects.filter(
            user_id=user.id, question_langid__name_lang=name_lang).exists()
        langs = Question_Lang.objects.get(name_lang=name_lang)
        question = Question.objects.filter(question_langid=langs).exists()
        start_time = langs.start_time.strftime("%m/%d/%Y, %H:%M:%S")
        end_time = langs.end_time.strftime("%m/%d/%Y, %H:%M:%S")
        current_time = datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
        if is_exists:
            messages.error(
                request, f'Siz oldin <b>{langs}</b> ga doir testni yechib bo`lgansiz')
        else:
            if question == 0:
                messages.error(
                    request, f'<b>{langs}</b> Tez orada 2021 yil uchun')
            elif (balance < 50000):
                messages.error(
                    request, f'Hisobingizda yetarli miqdorda pul <b>{balance}</b> yo`q &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<a href="http://www.payme.uz" class="btn btn-primary btn-lg active" role="button" aria-pressed="true">To`lov qiling</a>')
            elif current_time < start_time:
                messages.error(
                    request, f'Imtixon soat <b>{start_time}</b> da boshlanadi')
            elif current_time > end_time:
                messages.error(
                    request, f'Kechirasiz,Imtixon soat <b>{end_time}</b> da yakunlandi.')
            else:
                return redirect('rules', name_lang=name_lang)
    return render(request, 'languages.html', context)


def rules(request, name_lang):
    context = {}
    name_lang = Question_Lang.objects.get(name_lang=name_lang)
    print(name_lang)
    if request.method == 'POST':
        din = request.POST['din']
        print(din)
        if din == 'Islom':
            messages.error(
                request,
                f"<p>Alloh taolo <b>Nahil</b> surasining <b>105</b>-oyatida marhamat qiladi.</p><p> «Yolg`onni faqat Allohning oyatlariga imon keltirmaydiganlargina to`qirlar. Ana o`shalar  o`zlari yolg`onchilardir», degan.</p><p>Shunday ekan siz ham ustoz yoki do`stlarning yordamisiz faqat o`z bilmingizga tayangan holda sinovdan o`ting. </p><p>Hurmatli foydalanuvchi rostgo`y bo`ling! Testni mustaqil o`zingiz yeching!</p><br/><form action='/exam_page/{name_lang}' method='get'><input type='checkbox'  id='chkAgree' onclick='goFurther()'>&nbsp;&nbsp;<input type='submit' value='roziman' class='btn btn-primary' id='btnSubmit' disabled></form>"
            )
        elif din == 'Xristian':
            messages.error(
                request,
                f"<b style='font-size:20px;padding-left:5px;'>Ayub 15:31</b><p>Behuda narsalarga umid bog`lab,o`zlarini aldamasinlar,ularning mukofoti o`sha behuda narsalar bo`ladi.</p><b style='font-size:20px;padding-left:5px;'>Ayub 15:32</b><p>Vaqti soati yetmay turib, ular to`liq jazo oladilar,novdalari gullab-yashnamaydi.</p><p>Hurmatli foydalanuvchi rostgo`y bo`ling! Testni mustaqil o`zingiz yeching!</p><br/> <form action='/exam_page/{name_lang}' method='get'><input type='checkbox'  id='chkAgree' onclick='goFurther()'>&nbsp;&nbsp;<input type='submit' value='roziman' class='btn btn-primary' id='btnSubmit' disabled></form>"
            )
        elif din == 'Yahudiy':
            messages.error(
                request,
                f"<p>Hurmatli foydalanuvchi rostgo`y bo`ling! Testni mustaqil o`zingiz yeching!</p><br/><form action='/exam_page/{name_lang}' method='get'><input type='checkbox'  id='chkAgree' onclick='goFurther()'>&nbsp;&nbsp;<input type='submit' value='roziman' class='btn btn-primary' id='btnSubmit' disabled></form>"
            )
        else:
            messages.error(
                request,
                f"<p>Hurmatli foydalanuvchi rostgo`y bo`ling! Testni mustaqil o`zingiz yeching!</p><br/><form action='/exam_page/{name_lang}' method='get'><input type='checkbox'  id='chkAgree' onclick='goFurther()'>&nbsp;&nbsp;<input type='submit' value='roziman' class='btn btn-primary' id='btnSubmit' disabled></form>"
            )
    return render(request, 'rules.html', context)


@login_required
def exam_page(request, name_lang):
    user = User.objects.filter(id=request.user.id)
    reg = Register.objects.get(user_id=request.user.id)
    balance = reg.balance
    question_lang = Question_Lang.objects.get(name_lang=name_lang)
    audio = Question_Lang.objects.filter(name_lang=name_lang)
    current_time = timezone.now()
    start_time = question_lang.start_time
    end_time = question_lang.end_time
    leftime = end_time - current_time
    context = {}
    if start_time < current_time and end_time > current_time:
        global t
        x = time.strptime(str(leftime).split('.')[0], '%H:%M:%S')
        t = int(datetime.timedelta(hours=x.tm_hour,
                                   minutes=x.tm_min, seconds=x.tm_sec).total_seconds())
    for z in audio:
        audio = z.audio
        datapart = PartQuestion.objects.filter(question_langid=question_lang)
        data = Question.objects.filter(question_langid=question_lang)
        context = {'data': data, 'datapart': datapart,
                   'name_lang': name_lang, 'audio': audio, 'dif_time': t}
        if request.method == 'POST':
            user = request.user
            for item in data:
                try:
                    res = request.POST[f'optradio{item.id}']
                    if res in item.answer:
                        difference = balance - 50000
                        reg.balance = difference
                        reg.save()

                        result = AnswerQuestion.objects.create(
                            ansa=res, question_id_id=item.id, user_id=user, is_true=True, question_langid=question_lang)
                    else:
                        result = AnswerQuestion.objects.create(
                            ansa=res, question_id_id=item.id, user_id=user, is_true=False,
                            question_langid=question_lang)
                except:
                    result = AnswerQuestion.objects.create(
                        ansa='zero', question_id_id=item.id, user_id=user, is_true=False, question_langid=question_lang)
            result.save()
            return redirect('result', name_lang=name_lang)
        return render(request, 'exam.html', context)


@login_required
def result(request, name_lang):
    ball = 3.5
    user = User.objects.filter(id=request.user.id).first()
    is_exists = Result.objects.filter(user_id=user, question_langid__name_lang=name_lang).exists()
    if is_exists:
        return redirect('/')
    else:
        register = Register.objects.get(user=request.user)
        question_lang = Question_Lang.objects.get(name_lang=name_lang)
        data = Question.objects.filter(question_langid=question_lang)
        answers = AnswerQuestion.objects.filter(
            user_id=user.id, question_langid=question_lang, is_true=True)
        num_an = len(answers)
        num_qu = len(data)
        score = num_an * ball
        context = {'user': user.last_name + ' ' + user.first_name, 'email': user.email}
        result = Result.objects.create(
            user_id=user, total_questions=num_qu, correct_answers=num_an, result=score,
            question_langid=question_lang, register_id=register)
        result.save()
    return render(request, 'result.html', context)


@login_required
def change_password(request):
    context = {}
    ch = Register.objects.filter(user__id=request.user.id)
    if len(ch) > 0:
        data = Register.objects.get(user__id=request.user.id)
        context = {'data': data}
    if request.method == 'POST':
        current = request.POST['cpwd']
        newpass = request.POST['npwd']

        user = User.objects.get(id=request.user.id)
        un = user.username
        check = user.check_password(current)
        if check == True:
            user.set_password(newpass)
            user.save()
            context['msz'] = 'Parol muvaffaqiyatli yangilandi!!!'
            context['col'] = 'alert alert-success'
            user = User.objects.get(username=un)
            login(request, user)
        else:
            context['msz'] = 'Amaldagi Parol Xato'
            context['col'] = 'alert alert-danger'
    return render(request, 'change_password.html', context)


@login_required
def sendemail(request):
    context = {}
    user = User.objects.get(id=request.user.id)
    if user.is_superuser:
        if request.method == 'POST':
            rec = request.POST['to'].split(',')
            sub = request.POST['sub']
            msz = request.POST['msz']
            try:
                em = EmailMessage(sub, msz, to=rec)
                em.send()
                context['status'] = 'Xabar muvaffaqiyatli yuborildi'
                context['cls'] = 'alert-success'
            except:
                context[
                    'status'] = 'Xabar yuborish amalga oshmadi.Iltimos internetingizni tekshirib qaytadan xarakat qilib ko`ring'
                context['cls'] = 'alert-danger'
    return render(request, 'sendemail.html', context)


def forgotpass(request):
    context = {}
    if request.method == "POST":
        un = request.POST["username"]
        pwd = request.POST["npass"]

        user = get_object_or_404(User, username=un)
        user.set_password(pwd)
        user.save()

        login(request, user)
        if user.is_superuser:
            return HttpResponseRedirect("/admin")
        else:
            return HttpResponseRedirect("/student_dash")
        # context["status"] = "Password Changed Successfully!!!"

    return render(request, "forgot_pass.html", context)


def reset_password(request):
    username = request.GET["username"]
    try:
        user = get_object_or_404(User, username=username)
        otp = random.randint(1000, 9999)
        msz = "Janob/Honim {} \n{} sizning bir martalik tasdiqlash kodingiz \nBuni hech kimga ko`rsatmang \nRahmat va Ehtirom bilan \nAction.uz Jamoasi".format(
            user.username, otp)
        try:
            email = EmailMessage("Account Tekshirish", msz, to=[user.email])
            email.send()
            return JsonResponse({"status": "sent", "email": user.email, "rotp": otp})
        except:
            return JsonResponse({"status": "error", "email": user.email})
    except:
        return JsonResponse({"status": "failed"})


def result_section(request):
    provinces = ['Toshkent', 'Andijon', 'Buxoro', 'Fargʻona', 'Jizzax', 'Namangan',
                 'Xorazm', 'Navoiy', 'Qashqadaryo', 'Qoraqalpogʻiston', 'Samarqand', 'Sirdaryo', 'Surxondaryo']
    data = Question_Lang.objects.all()
    context = {'data': data, 'provinces': provinces}
    if request.method == 'POST':
        name_lang = request.POST['langs']
        province = request.POST['province']
        is_exists = Result.objects.filter(
            question_langid__name_lang=name_lang, register_id__provin=province).exists()
        if is_exists:
            return redirect('result_view', name_lang=name_lang, province=province)

        else:
            messages.error(
                request,
                f'<b>{province}</b> viloyati bo`yicha hech kim <b>{name_lang}</b>  bo`yicha testda qatnashmagan'
            )
    return render(request, 'result_section.html', context)


def result_section_country(request):
    data = Question_Lang.objects.all()
    context = {'data': data}
    if request.method == 'POST':
        name_lang = request.POST['langs']
        is_exists = Result.objects.filter(
            question_langid__name_lang=name_lang).exists()
        if is_exists:
            return redirect('result_view_country', name_lang=name_lang)
        else:
            messages.error(
                request, f' Hech kim <b>{name_lang}</b>  bo`yicha testda qatnashmagan'
            )
    return render(request, 'result_section_country.html', context)


def result_view(request, name_lang, province):
    results = Result.objects.filter(
        question_langid__name_lang=name_lang, register_id__provin=province)
    data = Result.objects.filter(
        question_langid__name_lang=name_lang)
    context = {'data': results, 'resultes': data}
    return render(request, 'result_view.html', context)


def result_view_country(request, name_lang):
    data = Result.objects.filter(question_langid__name_lang=name_lang)
    context = {'data': data}
    return render(request, 'result_view_country.html', context)


def place_number(request):
    data = []
    provinces = ['Toshkent', 'Andijon', 'Buxoro', 'Fargʻona', 'Jizzax', 'Namangan',
                 'Xorazm', 'Navoiy', 'Qashqadaryo', 'Qoraqalpogʻiston', 'Samarqand', 'Sirdaryo', 'Surxondaryo']
    langs = Question_Lang.objects.all()
    for provin in provinces:
        print(provin)
        for lang in langs:
            results = Result.objects.filter(
                register_id__provin=provin, question_langid__name_lang=lang.name_lang).order_by('result').reverse()
            print(results)
            data.append(results)
            for index, result in enumerate(results):
                result.place_number = index + 1
                result.save()

    context = {'data': data}
    return redirect('/success')
    return render(request, 'place_number.html', context)


def place_number_country(request):
    data = []
    langs = Question_Lang.objects.all()
    for lang in langs:
        results = Result.objects.filter(
            question_langid__name_lang=lang.name_lang).order_by('result').reverse()
        data.append(results)
        for index, result in enumerate(results):
            result.place_number_country = index + 1
            result.save()

    context = {'data': data}
    return redirect('/success')
    return render(request, 'place_number_country.html', context)


def success(request):
    return render(request, 'success.html')


def search(request):
    context = {}
    if request.method == 'GET':
        query = request.GET['username']
        queryn=query.capitalize()
        edu=SchoolRegister.objects.filter(school_name=queryn)
        data = Result.objects.filter(user_id__username=queryn)
        is_exists = Result.objects.filter(user_id__username=queryn).exists()
        if is_exists:
            context = {'data': data,'query':queryn}
        elif edu:
            context = {'edu': edu,'query':queryn}
        else:
            messages.error(
                request,
                f'<span style="font-size:30px;">Kechirasiz, <b>{queryn}</b> bu so`rov bo`yicha xech qanday ma`lumot topilmadi <i class="fa fa-frown-o" aria-hidden="true"></i></span>.'
            )

    return render(request, 'search.html', context)


def news(request):
    return render(request, 'news.html')


def education_center(request):
    context={}
    edu_center=[]
    data_provin=[]
    data = SchoolRegister.objects.all()  
    provinces = ['Toshkent', 'Andijon', 'Buxoro', 'Fargʻona', 'Jizzax', 'Namangan',
                 'Xorazm', 'Navoiy', 'Qashqadaryo', 'Qoraqalpogʻiston', 'Samarqand', 'Sirdaryo', 'Surxondaryo']
    for provin in provinces:
        data_provin.append(provin)
    if request.method=='POST':
        name=request.POST['pro']
        edu_center=SchoolRegister.objects.filter(provin=name)
        
    context = {'data': data,'data_provin':data_provin,'edu_center':edu_center}
    return render(request, 'education_center.html', context)


def register_corporate(request):
    country_cod = '+998'
    science = Science.objects.all()
    lang = Language.objects.all()
    context = {'data': science, 'lang': lang}
    if request.method == 'POST':  # post orqali jonatilvotgan qiymatlarni ozgaruvchilarga ozlashtirish
        schoolname = request.POST['schoolname']
        science = request.POST.getlist('science')
        science1 = request.POST['science']
        print(science1)
        lang_ = request.POST.getlist('slang')
        print(lang_)
        uname = request.POST['uname']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        email = request.POST['email']
        cnumber = request.POST['pnumber']
        st = request.POST['state']
        prov = request.POST['province']
        website=request.POST['website']
        address = request.POST['address']
        mobnumber = country_cod + cnumber
        mobnumber2 = str(mobnumber[4:6] + '***' + mobnumber[9:13])
        usr = User.objects.create_user(uname, email, password1)
        usr.first_name = schoolname
        # usr.last_name = lname
        usr.save()
        reg = SchoolRegister.objects.create(creator=usr, contact_number=mobnumber, state=st, provin=prov,
                                            contact_number2=mobnumber2, science=science, lang=lang_,
                                            address=address, school_name=schoolname,website=website)
        if "image" in request.FILES:
            img = request.FILES["image"]
            reg.school_logo = img
            reg.save()
        return render(request, 'register_corporate.html',
                      {'status': 'Tabriklaymiz! Hurmatli , {} Siz ro`yxatdan muvaffaqiyatli o`tdingiz'.format(
                          schoolname)})

    return render(request, 'register_corporate.html', context)

def topic(request):
    return render(request,'topik.html')

def ielts(request):
    return render(request,'ielts.html')

def hsk(request):
    return render(request,'hsk.html')

def act(request):
    return render(request,'act.html')

def ap(request):
    return render(request,'ap.html')

def ept(request):
    return render(request,'ept.html')

def cae(request):
    return render(request,'cae.html')

def caeli(request):
    return render(request,'caeli.html')

def duolingo(request):
    return render(request,'duolingo.html')

def gmat(request):
    return render(request,'gmat.html')

def jlpt(request):
    return render(request,'jlpt.html')

def klat(request):
    return render(request,'klat.html')

def cefr(request):
    return render(request,'cefr.html')

def sat(request):
    return render(request,'sat.html')

def toefl(request):
    return render(request,'toefl.html')

def gre(request):
    return render(request,'gre.html')

def psat(request):
    return render(request,'psat.html')