from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length = 30, unique = True)
    description = models.TextField()
    def __unicode__(self):
        return self.name
    class Meta:
        verbose_name = "category"
        verbose_name_plural = "categories"
        

class Good(models.Model):
    name=models.CharField(max_length = 50, unique = True, verbose_name = "Name")
    in_stock = models.BooleanField(default = True, db_index = True, verbose_name = "Present")
    category = models.ForeignKey(Category, null = True, blank = True,on_delete=models.CASCADE)
    description = models.TextField()
    price = models.IntegerField()
    def get_is_stock(self):
        if self.in_stock:
            return "+"
        else:
            return ""
    def __unicode__(self):
        s = self.name
        if not self.in_stock:
            s = s + " (not present)"
        return s
    class Meta:
        ordering = ["price","name"]
        unique_together = ("category","name","price")
        verbose_name = "good"
        verbose_name_plural = "goods"
class Offer(models.Model):
    name = models.CharField(max_length = 50, verbose_name = "Name")
    surname = models.CharField(max_length = 50, verbose_name = "Surame")
    eMail = models.EmailField(max_length = 50, verbose_name = "E-mail")
    good = models.ForeignKey(Good,on_delete=models.CASCADE)
    dateTime = models.DateTimeField(auto_now_add = True)
    dateTimeVertified = models.DateTimeField(null = True, blank = True)
    dateTimeSent = models.DateTimeField(null = True, blank = True)
    status = models.CharField(choices = ((1,"Offer from client"),(2,"Verified"),(3,"Done"),(4,"Not verified"),(5,"Troubles")),max_length = 100)
    
class Bookmap(models.Model):
    def __unicode__(self):
        return self.book
    book = models.CharField(max_length = 50, verbose_name = "Book")
    author = models.CharField(max_length = 50, verbose_name = "Author")
    upload = models.FileField(upload_to='uploads/',default='test')
    map = models.ImageField(upload_to='uploads/maps',default='test')

class Hero(models.Model):
    name = models.CharField(max_length = 50, verbose_name = "Name")
    book = models.ForeignKey(Bookmap,on_delete=models.CASCADE)
    description=models.TextField(null=True)
    photo = models.ImageField(upload_to='uploads/images',default='test')
    class Meta:
        unique_together = ("name","book")

class Time(models.Model):
    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name

    time = models.IntegerField()
    book = models.ForeignKey(Bookmap,on_delete=models.CASCADE)
    name = models.CharField(max_length = 50, verbose_name = "Name")
    class Meta:
        unique_together = ("time","book")

    
class Point(models.Model):
    x = models.FloatField();
    y = models.FloatField();
    time = models.ForeignKey(Time,on_delete=models.CASCADE);
    place = models.CharField(max_length = 50, verbose_name = "Place")
    name = models.ForeignKey(Hero,on_delete=models.CASCADE);
    book = models.ForeignKey(Bookmap,on_delete=models.CASCADE);
    text = models.TextField();
    page = models.IntegerField(default=1);
class UserProfile(models.Model):
    user_auth = models.OneToOneField(User, primary_key=True,on_delete=models.CASCADE)
    email = models.EmailField(verbose_name="email",default=None)
    phone = models.CharField(max_length=20, verbose_name="Phone number", null=True, default=None, blank=True)
    born_date = models.DateField(verbose_name="Born date", null=True,default=None, blank=True)
    last_connexion = models.DateTimeField(verbose_name="Date of last connexion", null=True, default=None, blank=True)
    permissions = models.IntegerField(verbose_name="Seniority",  default=0)
    def __str__(self):
        return self.user_auth.username