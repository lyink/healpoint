from django.db import models
from djmoney.models.fields import MoneyField
from django.db import models
from django.utils.html import mark_safe


#department model

class Department(models.Model):
    department_name=models.CharField(max_length=200,primary_key=True)
    def __str__(self):
        return self.department_name

class Programs(models.Model):
    program_name=models.CharField(max_length=200,primary_key=True)
    program_duration=models.IntegerField()
    program_fee=MoneyField(max_digits=14,decimal_places=2,default_currency='TZS')
    date_registered=models.DateField(auto_now_add=True)
    department=models.ForeignKey(Department,on_delete=models.CASCADE)
    def __str__(self):
        return self.program_name

class Course(models.Model):
    course_name=models.CharField(max_length=200)
    program=models.ForeignKey(Programs,on_delete=models.CASCADE)
    def __str__(self):
        return self.course_name

class Student(models.Model):

       #enumerated list

       class Region_List(models.TextChoices):
         Default="Tanzania"
         Dodoma="Dodoma"
         Tanga="Tanga"
         Arusha="Arusha"
         Tabora="Tabora"

       regno=models.CharField(max_length=200,primary_key=True)     
       full_name=models.CharField(max_length=200)
       passport_size=models.ImageField(upload_to='passports/')
       application_form=models.FileField(upload_to='applications/')
       program=models.ForeignKey(Programs,on_delete=models.CASCADE)
       date_registered=models.DateField(auto_now_add=True)
       resident=models.CharField(choices=Region_List.choices,max_length=100)

       def __str__(self):
             return self.regno
       def image_tag(self):
            return mark_safe('<img src="%s"width="50"style="border-radius:4px">'% (self.passport_size.url))

#herroes

class Herroes(models.Model):

     class Category(models.TextChoices):
       Best_Student="Best_Student"
       Best_Staff="Best_Staff"
       Best_Footbal_Winner="Best_Footbal_Winner"
       Best_Leader="Best_Leader"


     full_name=models.CharField(max_length=200)
     heading=models.CharField(max_length=200)
     title=models.CharField(choices=Category.choices,max_length=100)
     image=models.ImageField(upload_to='herroes/')
     date_registered=models.DateField(auto_now_add=True)
     program=models.ForeignKey(Programs,on_delete=models.CASCADE)
     department=models.ForeignKey(Department,on_delete=models.CASCADE)
     def __str__(self):
             return self.full_name
     def image_tag(self):
            return mark_safe('<img src="%s"width="50"style="border-radius:4px">'% (self.image.url))
from django.db import models

class Doctors(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    specialization = models.CharField(max_length=200)
    date_of_birth = models.DateField()
    date_joined = models.DateField(auto_now_add=True)
    contact_number = models.CharField(max_length=15)
    email = models.EmailField()
    profile_picture = models.ImageField(upload_to='doctors/', blank=True, null=True)
    bio = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    



from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Tag(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    publication_date = models.DateTimeField(default=timezone.now)
    categories = models.ManyToManyField(Category, related_name='posts')
    tags = models.ManyToManyField(Tag, related_name='posts', blank=True)
    featured_image = models.ImageField(upload_to='blog_images/', blank=True, null=True)
    slug = models.SlugField(unique=True, max_length=200)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-publication_date']