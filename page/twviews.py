#from django.views.generic.base import TemplateView
#from django.core.paginator import Paginator, InvalidPage
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import redirect
from django.urls import reverse

from page.models import Category, Good, Bookmap, Offer, Hero, Time, Point, UserProfile
from django.views.generic.list import ListView 
from django.views.generic.detail import DetailView 
from django.views.generic.base import ContextMixin
from django import forms 
from django.views.generic.edit import CreateView
#from django.views.generic.edit import ProcessFormView
#from django.core.urlresolvers import reverse
#from django.shortcuts import redirect
from django.http import JsonResponse, HttpResponseRedirect, request
#import codecs
import os.path
#import sys

class GoodForm(forms.ModelForm): 
    class Meta: 
        model = Offer 
        fields = [ "name", "surname", "eMail"]
    description = forms.CharField(widget = forms.Textarea, label = "Комментарии") 
class HeroForm(forms.ModelForm):
    class Meta:
        model = Hero
        fields = ["name"]
class TimeForm(forms.ModelForm):
    class Meta:
        model = Time
        fields = ["time", "name"]
    # def clean(self):
        # cleaned_data=super(HeroForm,self).clean()
        # print(cleaned_data['description'])
class PointForm(forms.ModelForm):
    class Meta:
        model = Point
        fields = ["x", "y", "place", "page", "text"]        
class UserRegForm(forms.ModelForm):
    name = forms.CharField(label="Name", max_length=30)
    login = forms.CharField(label="Login")
    password = forms.CharField(label="Password", widget=forms.PasswordInput)
    password_bis = forms.CharField(label="Password", widget=forms.PasswordInput)
    def clean(self):
        cleaned_data = super(UserRegForm, self).clean()
        password = self.cleaned_data.get('password')
        password_bis = self.cleaned_data.get('password_bis')
        if password and password_bis and password != password_bis:
            raise forms.ValidationError("Passwords are not identical.")
        return self.cleaned_data
    class Meta:
        model = UserProfile
        fields=["phone","born_date","email"]
class CategoryListMixin(ContextMixin): 
    def get_context_data(self, **kwargs): 
        context = super(CategoryListMixin, self).get_context_data(**kwargs) 
        context["cats"] = Category.objects.order_by("name")
        return context 
class GoodEditMixin(CategoryListMixin): 
    def get_context_data(self, **kwargs): 
        context = super(GoodEditMixin, self).get_context_data(**kwargs) 
        try: 
            context["pn"] = self.request.GET["page"] 
        except KeyError: 
            context[ "pn"] = "1" 
        return context
# class GoodListView(TemplateView): 
    # template_narne = "index.html" 
    # def get_context_data(self, **kwargs): 
        # context = super(GoodListView, self).get_context_data(**kwargs) 
        # try: 
            # page_num = self.request.GET["page"] 
        # except KeyError: 
            # page_num = 1 
            # context["cats"] = Category.objects.order_by("name") 
        # if kwargs["cat_id"] == None: 
            # context["category"] = Category.objects.first() 
        # else: 
            # context["category"] = Category.objects.get(pk = kwargs["cat_id"]) 
        # paginator = Paginator(Good.objects.filter(category = context["category"]).order_by("name"), 1) 
        # try: 
            # context["goods"] = paginator.page(page_num) 
        # except InvalidPage: 
            # context["goods"] = paginator.page(1) 
        # return context 

    

# class GoodDetailView(TemplateView): 
 # template_narne = "good.html" 
 # def get_context_data(self, **kwargs): 
     # context = super(GoodDetailView, self).get_context_data(**kwargs) 
     # try: 
         # context["pn"] = self.request.GET["page"] 
     # except KeyError: 
         # context["pn"] = 1 
         # context["cats"] = Category.objects.order_by("name") 
     # try: 
         # context["good"] = Good.objects.get(pk = kwargs["good_id"]) 
     # except Good.DoesNotExist: 
         # raise Http404 
     # return context
        
        
class GoodListView(ListView, CategoryListMixin): 
    template_name = "index.html" 
    paginate_by = 10 
    cat = None 
    def get(self, request, *args, **kwargs): 
        if self.kwargs["cat_id"] == None: 
            self.cat = Category.objects.first() 
        else: 
            self.cat = Category.objects.get(pk = self.kwargs["cat_id"]) 
        return super(GoodListView, self).get(request, *args, **kwargs) 
    def get_context_data(self, **kwargs): 
        context = super(GoodListView, self).get_context_data(**kwargs) 
       # context["cats"] = Category.objects.order_by("name") 
        context["category"] = self.cat 
        return context 
    def get_queryset(self): 
        return Good.objects.filter(category = self.cat).order_by("name") 
        
       
class GoodDetailView(DetailView, CategoryListMixin): 
    template_name = "good.html" 
    model = Good 
    pk_url_kwarg = "good_id"  
    def get_context_data(self, **kwargs): 
        context = super(GoodDetailView, self).get_context_data(**kwargs) 
        try: 
            context["pn"] = self.request.GET["page"] 
        except KeyError: 
            context["pn"]  = "1"
         #   context["cats"] = Category.objects.order_by("name") 
        return context        
def seekUTF(fid,point,start):
    while True:
        try:
            fid.seek(point,1)
            fid.read(1).decode("utf8")
            break
        except UnicodeDecodeError:
            fid.seek(-point-1,1)
            point-=1
    fid.seek(start)
    return point
def seekUTFrev(fid,point,start):
    while True:
        try:
            fid.seek(-point,1)
            fid.read(1).decode("utf8")
            break
        except UnicodeDecodeError:
            fid.seek(point,1)
            point+=2
    return point
class BookMap(DetailView): 
    template_name = "bookmap.html" 
    model = Bookmap 
    pk_url_kwarg = "book_id"

    def get_context_data(self, **kwargs): 
        context = super(BookMap, self).get_context_data(**kwargs) 
        try: 
            context["pn"] = self.request.GET["page"] 
        except KeyError: 
            context["pn"]  = "1"
         #   context["cats"] = Category.objects.order_by("name") 
        textFilePath=self.object.upload;
        textFid=open(os.path.dirname(os.path.realpath(__file__))+textFilePath.url, 'rb')
        textFid.seek(0)
        endPoint=seekUTF(textFid,10000,0)
        text=textFid.read(endPoint).decode("utf8",errors='ignore')
        dotPoint=text.rfind(r".")+1
        context["text"]=text[1:dotPoint];
        context["startPoint"]=0;
        L=len(text[0:dotPoint].encode("utf8"))
        textFid.seek(0)
        textFid.read(L).decode("utf8",errors='replace')
        context["endPoint"]=textFid.tell()
        context["heroes"]=Hero.objects.filter(book=self.kwargs["book_id"]);
        numSteps=Time.objects.filter(book=self.kwargs["book_id"]).count()
        if (numSteps):
            context["step"]=int(1000/(numSteps-1))
        else:
            context["step"]=int(1000)
        return context
    def get(self, request, *args, **kwargs):
        if self.kwargs["book_id"] == None:
            self.kwargs["book_id"]=1
        return super(BookMap, self).get(request, *args, **kwargs)
    def post(self, request, *args, **kwargs):
            #heroDumb=Hero(name="test",book=Bookmap.objects.get(pk=self.kwargs["book_id"]));
        if (request.POST["type"]=='hero'):
            self.form=HeroForm(request.POST)
            if(self.form.is_valid()):
                new_hero=self.form.save(commit=False)
                new_hero.book=Bookmap.objects.get(pk=self.kwargs["book_id"])
                new_hero.description="sdfs";
                new_hero.save();
                #return redirect("bookmap",book_id=self.kwargs["book_id"])
                return JsonResponse({'hero_id':new_hero.id})
        elif (request.POST["type"]=='selHero'):
            heroSelected=Hero.objects.get(pk=self.request.POST["hero_id"])
            return JsonResponse({'heroSelUrl':heroSelected.photo.url})
        elif (request.POST["type"]=='time'):
            self.form=TimeForm(request.POST);
            if (self.form.is_valid()):
                bookTimes=Time.objects.filter(book=self.kwargs["book_id"]).order_by("time")
                floor = True
                steps=len(bookTimes)+2
                if (steps):
                    stepSize=1000/steps
                    for times in bookTimes:
                        if (times.time):
                            if (times.time > int(request.POST["time"])):
                                floor=False
                            if (floor):
                                times.time=int( times.time - times.time % stepSize)
                                print(times.time)
                            else:
                                times.time=int( times.time - times.time % stepSize + stepSize)
                            times.save()
                new_time=self.form.save(commit=False)
                new_time.book=Bookmap.objects.get(pk=self.kwargs["book_id"])
                try:
                    new_time.save()
                except:
                    cur_time=Time.objects.get(time=int(request.POST["time"]))
                    cur_time.name=request.POST["name"]
                    cur_time.save()
                return JsonResponse({'success':"success"})
        elif (request.POST["type"]=='sliderChange'):
            timeName=Time.objects.get(time=request.POST["time"],book=self.kwargs["book_id"]).name;
            return JsonResponse({'timeName':timeName})
        elif (request.POST["type"]=='addPoint'):
            print(request.POST["page"])
            self.form=PointForm(request.POST)
            if(self.form.is_valid()):
                new_point=self.form.save(commit=False)
                new_point.book=Bookmap.objects.get(pk=self.kwargs["book_id"])
                new_point.time=Time.objects.get(time=request.POST["time"],book=self.kwargs["book_id"]);
                new_point.name=Hero.objects.get(name=request.POST["name"][1:-1],book=self.kwargs["book_id"]);
                new_point.save();
                #return redirect("bookmap",book_id=self.kwargs["book_id"])
                return JsonResponse({'success':"success"})
        elif (request.POST["type"]=='changePage'):
            textFilePath=Bookmap.objects.get(pk=self.kwargs["book_id"]).upload;
            textFid=open(os.path.dirname(os.path.realpath(__file__))+textFilePath.url, 'rb')
            if (request.POST["direction"]=="next"):
                stPoint=int(request.POST["prevEnd"])
                endPoint=seekUTF(textFid,10000,stPoint)
                text=textFid.read(endPoint).decode("utf8",errors='ignore')
                dotPoint=text.rfind(r".")+1
                L=len(text[0:dotPoint].encode("utf8"))
                textFid.seek(stPoint)
                textFid.read(L).decode("utf8",errors='replace')
                endPointData=textFid.tell()
                return JsonResponse({'text':text[0:dotPoint], 'endPoint':endPointData, 'startPoint':stPoint})
            elif (request.POST["direction"]=="prev"):
                endPoint=int(request.POST["prevStart"])
                textFid.seek(endPoint)
                stPoint=seekUTFrev(textFid,10000,endPoint)
                textFid.seek(-1,1)
                text=textFid.read(stPoint).decode("utf8",errors='ignore')
                dotPoint=text.find(r".")+1
                L=len(text[0:dotPoint].encode("utf8"))
                textFid.seek(-stPoint,1)
                textFid.read(L).decode("utf8",errors='replace')
                startPointData=textFid.tell()
                return JsonResponse({'text':text[dotPoint:], 'startPoint':startPointData, 'endPoint':endPoint})

class OfferView(CreateView, GoodEditMixin): 
    model = Offer 
    form_class = GoodForm 
    template_name = "offer.html" 
    # def get(self, request, *args, **kwargs): 
        # if self.kwargs["cat_id"] != None: 
            # self.initial["category"] = Category.objects.get(pk = self.kwargs["cat_id"]) 
        # return super(GoodCreate, self).get(request, *args, **kwargs) 
    # def post(self, request, *args, **kwargs): 
        # self.success_url = reverse("index", kwargs ={"cat_id": Category.objects.get(pk = self.kwargs["cat_id"]).id}) 
        # return super(OfferView, self).post(request, *args, **kwargs) 
    # def get_context_data(self, **kwargs):
        # context = super(OfferView, self).get_context_data(**kwargs) 
        # context ["category"] = Category.objects.get (pk = self.kwargs [ "cat_id"]) 
        # return context 
class LoginViewCust(LoginView,GoodEditMixin):
    model = UserProfile
    def get(self, request, *args, **kwargs):
        getRet=super(LoginViewCust, self).get(request, *args, **kwargs)
        if (request.GET.get('next') is not None) and  (request.user.is_authenticated):
            return redirect(request.GET['next'])
        return getRet
class LogoutViewCust(LogoutView,GoodEditMixin):
    model = UserProfile
class RegView(CreateView,GoodEditMixin):
    model = UserProfile
    form_class = UserRegForm
    def post(self, request, *args, **kwargs):
        form = UserRegForm(request.POST)
        print(form.is_valid())
        name = form.cleaned_data['name']
        login = form.cleaned_data['login']
        password = form.cleaned_data['password']
        phone = form.cleaned_data['phone']
        born_date = form.cleaned_data['born_date']
        email = form.cleaned_data['email']
        new_user = User.objects.create_user(username=login, email= email, password=password)
        new_user.is_active = True
        new_user.last_name = name
        new_user.save()
        user_prof = UserProfile(user_auth=new_user, phone=phone,born_date=born_date,email=email)
        user_prof.save()
        return HttpResponseRedirect(reverse('bookmap'))
