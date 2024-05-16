from django.db import models

# Create your models here.
class UserModel(models.Model):
    user_id = models.AutoField(primary_key=True)
    user_name = models.CharField(max_length=100)
    user_email = models.EmailField(max_length=100, null=True)
    user_image = models.ImageField(upload_to='user_images/', null=True)
    user_password = models.CharField(max_length=100)

    class Meta():
        db_table = 'user'

    def __str__(self):
        return f'{self.user_name}'

class CategoryModel(models.Model):
    category_id = models.AutoField(primary_key=True)
    category_name = models.CharField(max_length=100)

    class Meta():
        db_table = 'category'

    def __str__(self):
        return f'{self.category_name}'

class BookModel(models.Model):
    book_id = models.AutoField(primary_key=True)
    book_name = models.CharField(max_length=100)
    book_image = models.ImageField(upload_to='images/', null=True)
    book_price = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    book_description = models.TextField()
    book_category = models.ForeignKey(CategoryModel, on_delete=models.CASCADE)
    book_user = models.ForeignKey(UserModel, on_delete=models.CASCADE)

    class Meta():
        db_table = 'book'

    def __str__(self):
        return f'{self.book_name}'

class ReviewModel(models.Model):
    review_id = models.AutoField(primary_key=True)
    review_name = models.TextField()
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, null=True)
    book = models.ForeignKey(BookModel, on_delete=models.CASCADE)

    class Meta():
        db_table ='review'

    def __str__(self):
        return f'{self.book}'
    
class CartItemModel(models.Model):
    cart_item_id = models.AutoField(primary_key=True)
    book = models.ForeignKey(BookModel, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)

    class Meta:
        db_table = 'cart_item'

    def __str__(self):
        return f'{self.user} - {self.book}'
    
class PaymentModel(models.Model):
    amount = models.CharField(max_length=100)
    payment_id = models.CharField(max_length=100)
    paid = models.BooleanField(default=False)
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    book = models.ForeignKey(BookModel, on_delete=models.CASCADE)
    
    class Meta():
        db_table = 'payment'

    def __str__(self):
        return f'{self.user} - {self.book}'