from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^product$', views.product, name='product'),
    url(r'^admin$', views.admin, name="admin"),
    url(r'^orders$', views.orders, name="orders"),
    url(r'^products$', views.products, name='products'),
    url(r'^show(?P<id>\d+)$', views.show, name='show'),
    url(r'^test$', views.test, name='test'),
    url(r'^add_product$', views.add_product, name='add_product'),
    url(r'^delete/(?P<id>\d+)$', views.delete, name='delete'),
    url(r'^edit/(?P<id>\d+)$', views.edit, name='edit'),
    url(r'^testcreate$', views.testcreate, name='test_create'),
    url(r'^update$', views.update, name='update'),
    url(r'^updatetest$', views.updatetest, name='updatestest'),
    url(r'^delete_category$', views.delete_category, name='delete_category'),
    url(r'^cart$', views.cart, name='cart'),
    url(r'^ship$', views.ship, name='ship')
]
