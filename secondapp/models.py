from django.db import models
from django.contrib.auth.models import User,auth
from datetime import datetime,date
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
from django.utils.safestring import mark_safe
#Contact_Us model

class Contact_Us(models.Model):
    name=models.CharField(max_length=250,verbose_name='Ism')
    contact_number=models.CharField(max_length=250,blank=True,unique=True,verbose_name='Telefon Nomer')
    email=models.EmailField(max_length=100,verbose_name='E-pochta')
    subject=models.CharField(max_length=250,verbose_name='Mavzu')
    message=models.TextField(verbose_name='Xabar')
    added_on=models.DateTimeField(auto_now_add=True,verbose_name='Jo`natilgan Sana')


    def __str__(self):
        return self.name        

    #set nickname for Table
    class Meta:
        verbose_name='Aloqa'
        verbose_name_plural='Biz bilan Aloqa'    

class Register(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)    
    province=(
        ('Andijon','Andijon'),('Buxoro','Buxoro'),('Fargʻona','Fargʻona'),
        ('Jizzax','Jizzax'),('Xorazm','Xorazm'),('Namangan','Namangan'),
        ('Navoiy','Navoiy'),('Qashqadaryo','Qashqadaryo'),
        ('Qoraqalpogʻiston','Qoraqalpogʻiston'),('Samarqand','Samarqand'),
        ('Sirdaryo','Sirdaryo'),('Surxondaryo','Surxondaryo'),
        ('Qashqadaryo','Qashqadaryo'),('Toshkent','Toshkent')
    )     
    provin=models.CharField(choices=province,null=True,blank=True,max_length=200,verbose_name='Viloyat')
    state=models.CharField(max_length=250,null=True,blank=True,verbose_name='Davlat')
    contact_number=models.IntegerField(verbose_name='Telefon Nomer')
    contact_number2=models.CharField(max_length=250,verbose_name='Shifrlangan T.Nomer')
    profile_pic=models.ImageField(upload_to='profiles/%Y/%m/%d',null=True,blank=True,verbose_name='Profil rasm')
    city=models.CharField(max_length=250,null=True,blank=True,verbose_name='Shahar')
    about=models.TextField(blank=True,null=True,verbose_name='O`zim haqimda')
    gender=models.CharField(max_length=250,null=True,default='Male',verbose_name='Jins')
    occupation=models.CharField(max_length=250,null=True,blank=True,verbose_name='Kasb')
    added_on=models.DateTimeField(auto_now_add=True,null=True,verbose_name='Qo`shilgan Sana')
    update_on=models.DateTimeField(auto_now=True,null=True,verbose_name='Yangilangan Sana')
    dateofbirth=models.DateField(verbose_name='Tug`ilgan Sana')
    sert_id = models.CharField(max_length=10,unique=True,null=True,verbose_name='Sertifikat Nomer')
    balance=models.IntegerField(default=False,verbose_name='Balans')
    training_center=models.CharField(max_length=250,verbose_name='O`quv Markazi')


    def __str__(self):
        return self.user.username


    class Meta:
        verbose_name='Ro`yxatga olish'
        verbose_name_plural='Ro`yxatdan O`tganlar'

class Science(models.Model):
    name=models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Language(models.Model):
    name=models.CharField(max_length=50)

    def __str__(self):
        return self.name
class SchoolRegister(models.Model):
    creator=models.OneToOneField(User,on_delete=models.CASCADE)
    province = (
        ('Andijon', 'Andijon'), ('Buxoro', 'Buxoro'), ('Fargʻona', 'Fargʻona'),
        ('Jizzax', 'Jizzax'), ('Xorazm', 'Xorazm'), ('Namangan', 'Namangan'),
        ('Navoiy', 'Navoiy'), ('Qashqadaryo', 'Qashqadaryo'),
        ('Qoraqalpogʻiston', 'Qoraqalpogʻiston'), ('Samarqand', 'Samarqand'),
        ('Sirdaryo', 'Sirdaryo'), ('Surxondaryo', 'Surxondaryo'),
        ('Qashqadaryo', 'Qashqadaryo'), ('Toshkent', 'Toshkent')
    )
    provin = models.CharField(choices=province, null=True, blank=True, max_length=200, verbose_name='Viloyat')
    science = models.CharField(null=True, blank=True, max_length=200, verbose_name='Fan')
    lang = models.CharField(null=True, blank=True, max_length=200, verbose_name='Til')
    school_name=models.CharField(max_length=250)
    school_logo = models.ImageField(upload_to='uploads/%Y/%m/%d', null=True, blank=True, verbose_name='O`quv markazi Logo')
    state = models.CharField(max_length=250, null=True, blank=True, verbose_name='Davlat')
    contact_number = models.IntegerField(verbose_name='Telefon Nomer')
    home_call=models.IntegerField(verbose_name="Domashniy Telefon yoki Faks",null=True,blank=True)
    contact_number2 = models.CharField(max_length=250, verbose_name='Shifrlangan T.Nomer',null=True,blank=True)
    website=models.CharField(max_length=50)
    telegram=models.CharField(max_length=100,null=True,blank=True)
    youtube = models.CharField(max_length=100,null=True,blank=True)
    facebook = models.CharField(max_length=100, null=True, blank=True)
    instagram = models.CharField(max_length=100, null=True, blank=True)
    address=models.CharField(max_length=250)

    class Meta:
        verbose_name='O`quv Markaz'
        verbose_name_plural='O`quv Markazlar'

class Question_Lang(models.Model):
    name_lang=models.CharField(max_length=250,verbose_name='Til Nomi')
    desc=models.CharField(max_length=250,blank=True,verbose_name='Tavsifi')
    start_time=models.DateTimeField(verbose_name='Boshlanish Vaqti')
    end_time=models.DateTimeField(verbose_name='Yakunlanish Vaqti')
    audio=RichTextUploadingField(verbose_name='Audio')

    def __str__(self):
        return self.name_lang
    class Meta:
        verbose_name='Til Qo`sish'
        verbose_name_plural='Tillar Nomi (Test yechish uchun)'  

class PartQuestion(models.Model):
    question_langid=models.ForeignKey(Question_Lang,on_delete=models.CASCADE,verbose_name='Til')
    parttitle=models.CharField(max_length=1500,verbose_name='Savollar Bo`limi')
    partdesc=models.CharField(max_length=1500,blank=True,verbose_name='Bo`lim Tavsifi')

    def Savollar_Bolimi(self):
        """Remove html tags from a string"""
        import re
        clean = re.compile('<.*?>')
        return re.sub(clean, '', self.parttitle)

    def Tavsifi(self):
        """Remove html tags from a string"""
        import re
        clean = re.compile('<.*?>')
        return re.sub(clean, '', self.partdesc)

    class Meta:
        verbose_name='Savol Bo`limi'
        verbose_name_plural='Test Bo`limlari Nomi'

class Question(models.Model):
    question_langid=models.ForeignKey(Question_Lang,on_delete=models.CASCADE,verbose_name='Til')
    partquestion_id=models.ForeignKey(PartQuestion,on_delete=models.CASCADE,verbose_name='Savol Bo`limi')
    qname=RichTextUploadingField(verbose_name='Savol')
    qitem1=models.CharField(max_length=250,blank=True,verbose_name='Variant 1')
    qitem2=models.CharField(max_length=250,blank=True,verbose_name='Variant 2')
    qitem3=models.CharField(max_length=250,blank=True,verbose_name='Variant 3')
    qitem4=models.CharField(max_length=250,blank=True,verbose_name='Variant 4')
    answer=models.CharField(max_length=250,blank=True,verbose_name='To`g`ri Javob')


    def Savol(self):
        """Remove html tags from a string"""
        import re
        clean = re.compile('<.*?>')
        return re.sub(clean, '', self.qname)

    class Meta:
        verbose_name='Savol'
        verbose_name_plural='Savollar'  

class AnswerQuestion(models.Model):
     user_id=models.ForeignKey(User,on_delete=models.CASCADE,verbose_name='Foydalanuvchi')
     question_langid=models.ForeignKey(Question_Lang,on_delete=models.CASCADE,verbose_name='Til')
     question_id=models.ForeignKey(Question,on_delete=models.CASCADE,verbose_name='Savol')
     ansa=models.CharField(max_length=300,null=True,verbose_name='Ishtirokchi Javobi')
     is_true=models.BooleanField(blank=True,null=False,verbose_name='To`gri/Xato')

     def __str__(self):
        return self.ansa    

     class Meta:
        verbose_name='Javob'
        verbose_name_plural='Javoblar'  


class Result(models.Model):
    user_id=models.ForeignKey(User,on_delete=models.CASCADE,verbose_name='Foydalanuvchi')
    question_langid=models.ForeignKey(Question_Lang,on_delete=models.CASCADE,verbose_name='Til')
    register_id=models.ForeignKey(Register,on_delete=models.CASCADE,verbose_name='Ishtirokchi')
    total_questions=models.CharField(max_length=100,verbose_name='Umumiy Savollar Soni')
    correct_answers=models.CharField(max_length=100,verbose_name='To`g`ri Javoblar Soni')
    result=models.CharField(max_length=250,verbose_name='Ishtirokchi To`plagan Bal')
    place_number=models.CharField(max_length=250,blank=True,verbose_name='Ishtirokchi Reytingi(Viloyat)')
    place_number_country=models.CharField(max_length=250,blank=True,verbose_name='Ishtirokchi Reytingi(Respublika)')
    def __str__(self):
        return self.result
    class Meta:
        verbose_name='Natija'
        verbose_name_plural='Natijalar'


class Education(models.Model):
    province = (
        ('Andijon', 'Andijon'), ('Buxoro', 'Buxoro'), ('Fargʻona', 'Fargʻona'),
        ('Jizzax', 'Jizzax'), ('Xorazm', 'Xorazm'), ('Namangan', 'Namangan'),
        ('Navoiy', 'Navoiy'), ('Qashqadaryo', 'Qashqadaryo'),
        ('Qoraqalpogʻiston', 'Qoraqalpogʻiston'), ('Samarqand', 'Samarqand'),
        ('Sirdaryo', 'Sirdaryo'), ('Surxondaryo', 'Surxondaryo'),
        ('Qashqadaryo', 'Qashqadaryo'), ('Toshkent', 'Toshkent')
    )
    provin = models.CharField(choices=province, null=True, blank=True, max_length=200, verbose_name='Viloyat')
    name=models.CharField(max_length=50,verbose_name='Markaz nomi')
    logo=RichTextUploadingField(verbose_name='Logo')
    list_of_courses=models.CharField(max_length=250,verbose_name='Kurs Nomi')
    address=models.CharField(max_length=100,verbose_name='Manzil')
    phone=models.CharField(max_length=50,verbose_name='Telefon Nomer')
    website=models.CharField(max_length=50,verbose_name='Sayt manzili')

    def __str__(self):
        return self.name
    class Meta:
        verbose_name='Markaz'
        verbose_name_plural='Markazlar'