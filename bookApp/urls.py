from django.urls import path
from bookApp import views
from . import views

urlpatterns = [
    path('', views.home, name='home_page'),
    path('details/<int:id>', views.detail, name='detail'),
    path('login', views.login, name='login'),
    path("add", views.add_to_cart, name='add_cart'),
    path("remove_from_cart", views.remove_from_cart, name="remove_from_cart"),
    path('cart', views.show_cart, name='show_cart'),
    path('update_cart', views.update_cart, name='update_cart'),
    path('delivery', views.delivery_order, name='delivery'),
    path('logout', views.logout, name='logout'),
    path('book', views.addbook, name='book_add'),
    path('profile', views.profile, name='user_profile'),
    path('delete/<int:id>', views.delete, name='delete_book'),
    path('edit/<int:id>', views.edit, name='edit_book'),
    path('review', views.review, name='review_page'),
    path('addreview', views.add_review, name='review_add'),
]