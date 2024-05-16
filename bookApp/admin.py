from django.contrib import admin
from . models import *

# Register your models here.
admin.site.register(UserModel)
admin.site.register(CategoryModel)
admin.site.register(BookModel)
admin.site.register(ReviewModel)
admin.site.register(CartItemModel)
admin.site.register(PaymentModel)