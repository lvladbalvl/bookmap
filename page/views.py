from django.shortcuts import render
from django.http import HttpResponse, Http404 
from page.models import Category, Good 
def index(request,cat_id): 
    cats = Category.objects.all().order_by("name") 
    if cat_id == None: 
        cat = Category.objects.first() 
    else: 
        cat = Category.objects.get(pk = cat_id) 
    goods = Good.objects.filter(category = cat).order_by("name")
    return render(request, "index.html", { "category": cat, "cats": cats,"goods": goods}) 
# Create your views here.
def good(request, good_id): 
    cats = Category.objects.all().order_by("name") 
    try: 
        good = Good.objects.get(pk = good_id) 
    except Good.DoesNotExist: 
        raise Http404 
    return render(request, "good.html", {"cats": cats, "good": good}) 
