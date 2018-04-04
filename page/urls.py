from django.conf.urls import  url
from django.contrib.auth.decorators import login_required
from django.urls import include

from page import views
from page.twviews import GoodListView, GoodDetailView, BookMap, OfferView,LoginViewCust,RegView, LogoutViewCust
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve

urlpatterns = [
    url(r'^(?:(?P<cat_id>\d+)/)?$', GoodListView.as_view(template_name = "index.html"), name = "index"), 
    url(r'^good/(?P<good_id>\d+)/$', GoodDetailView.as_view(template_name = "good.html"), name = "good"),
    url(r'^bookmap/(?:(?P<book_id>\d+)/)?$', login_required(BookMap.as_view(template_name = "bookmap.html")), name = "bookmap"),
    url(r'^offer$', OfferView.as_view(template_name = "offer.html"), name = "offer"),
    url(r'^accounts/registration/login', LoginViewCust.as_view(template_name = "./registration/login.html"),name="login"),
    url(r'^accounts/registration/registration', RegView.as_view(template_name = "./registration/registration.html"),name="registration"),
    url(r'^accounts/registration/logout', LogoutViewCust.as_view(template_name = "./registration/logout.html"),name="registration"),
    url(r'^media/(?P<path>.*)$', serve, {
            'document_root': settings.MEDIA_ROOT,
        })
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)