from decimal import Decimal
from django.shortcuts import get_object_or_404, render, redirect
from . models import *
from django.db.models import Q


# Create your views here.
def home(request):
    category = CategoryModel.objects.all()
    books = BookModel.objects.all()
    searched = ''
    if request.method == 'POST':
        searched = request.POST.get('search')
        category_filter = request.POST.get('category-filter')
        price_filter = request.POST.get('price-filter')

        if category_filter:
            books = books.filter(book_category__category_id=category_filter)

        if searched:
            books = books.filter(Q(book_name__icontains=searched) | Q(book_user__user_name__icontains=searched) | Q(book_category__category_name__icontains=searched))
        
        if price_filter == 'lowest':
            books = books.order_by('book_price')
        elif price_filter == 'highest':
            books = books.order_by('-book_price')

    return render(request, 'home.html', {'books': books, 'categorys': category, 'searched': searched})

def detail(request, id):
    books = BookModel.objects.get(book_id=id)
    review = ReviewModel.objects.filter(book_id=id)
    return render(request, 'detail.html', {'books': [books], 'reviews': review})

def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = UserModel.objects.filter(user_name=username, user_password=password).first()

        if user :
            request.session['user_id'] = user.user_id
            return redirect('/')
        else :
            return render(request, 'login.html')
        
    return render(request, 'login.html')

def add_to_cart(request):
    if 'user_id' in request.session:
        if request.method == 'POST':
            user_id = request.session.get('user_id')
            book_id = request.POST.get('book_id')
            quantity = int(request.POST.get('quantity'))

            user = get_object_or_404(UserModel, user_id=user_id)
            book = get_object_or_404(BookModel, book_id=book_id)

            # Check if the item already exists in the cart
            cart_item = CartItemModel.objects.filter(user=user, book=book).first()

            # If the item already exists, increment the quantity
            if cart_item:
                cart_item.quantity += quantity
            else:
                cart_item = CartItemModel(user=user, book=book, quantity=quantity)

            cart_item.save()

            # Fetch the book again to display on the details page
            books = BookModel.objects.filter(book_id=book_id)

            context = {
                'books': books,
                'reviews': ReviewModel.objects.filter(book=book)
            }
            return render(request, 'detail.html', context)
    
    return render(request, 'detail.html', context)

def show_cart(request):
    if 'user_id' in request.session:
        user_id = request.session['user_id']
        cart_items = CartItemModel.objects.filter(user_id=user_id)
        total_amount = sum(item.quantity * item.book.book_price for item in cart_items)
        for item in cart_items:
            item.total_price = Decimal(item.quantity) * item.book.book_price
            
        return render(request, 'cart.html', {'cart_items': cart_items, 'total_amount': total_amount})
    
    return redirect('/login')

def update_cart(request):
    if request.method == 'POST':
        cart_item_id = request.POST.get('cart_item_id')
        quantity = int(request.POST.get('quantity'))

        cart_item = get_object_or_404(CartItemModel, pk=cart_item_id)
        cart_item.quantity = quantity
        cart_item.save()

    return redirect('/cart')

def remove_from_cart(request):
    if request.method == 'POST':
        cart_item_id = request.POST.get('cart_item_id')
        cart_item = CartItemModel.objects.get(pk=cart_item_id)
        cart_item.delete()
        return redirect('/cart')
    
def delivery_order(request):
    if request.method == 'POST':
        total_amount = request.POST.get('total_amount')
        cart_items = request.POST.getlist('cart_items')
        context = {
            'total_amount': total_amount,
            'cart_items': cart_items,
        }
        return render(request, 'delivery.html', context)
    return render(request, 'delivery.html')


def logout(request):
    del request.session['user_id']
    return redirect('/')

def addbook(request):
    categories = CategoryModel.objects.all()
    if 'user_id' in request.session:

        if request.method == 'POST':
            book_name = request.POST.get('book_name')
            book_image = request.FILES.get('book_image')
            book_price = request.POST.get('book_price')
            book_description = request.POST.get('book_description')
            book_category = CategoryModel.objects.get(category_id=request.POST.get('book_category'))
            user_id = request.session['user_id']
            user_instance = UserModel.objects.get(pk=user_id)

            new_book = BookModel()
            new_book.book_name = book_name
            new_book.book_image = book_image
            new_book.book_price = book_price
            new_book.book_description = book_description
            new_book.book_category = book_category
            new_book.book_user = user_instance
            new_book.save()
            return redirect('/')
    else:
        return render(request, 'login.html')
    return render(request, 'addbook.html', {'categories': categories})

def profile(request):
    if 'user_id' in request.session:
        user_id = request.session['user_id']
        
        user = UserModel.objects.get(user_id=user_id)
        
        uploaded_books = BookModel.objects.filter(book_user=user)
        
        return render(request, 'profile.html', {'books': uploaded_books, 'user': [user]})
    else:
        return redirect('/login')
    return render(request, 'profile.html', {'books': uploaded_books, 'user': [user]})

def delete(request, id):
    book = BookModel.objects.get(book_id=id)
    book.delete()
    return redirect('/profile')

def edit(request, id):
    book = BookModel.objects.get(book_id=id)
    category = CategoryModel.objects.all()

    if request.method == 'POST':
        book_name = request.POST.get('new_book_name')
        book_price = request.POST.get('new_book_price')
        book_description = request.POST.get('new_book_description')
        book_category = CategoryModel.objects.get(category_id=request.POST.get('new_book_category'))
        
        user_id = request.session.get('user_id')
        user = UserModel.objects.get(pk=user_id)

        if 'new_book_image' in request.FILES:
            book_image = request.FILES['new_book_image']
            book.book_image = book_image

        # Update other attributes
        book.book_name = book_name
        book.book_price = book_price
        book.book_description = book_description
        book.book_category = book_category
        book.book_user = user 
        book.save()
        return redirect('/profile')
    return render(request, 'update.html', {'book': [book], 'category': category})


def form(request):
    if 'user_id' in request.session:
        if request.method == 'POST':
            user_id = request.session.get('user_id')
            book_id = request.POST.get('book_id')
            quantity = int(request.POST.get('Quantity'))

            user = UserModel.objects.get(user_id=user_id)
            book = BookModel.objects.get(book_id=book_id)
            
            total_amount = quantity * book.book_price

            # client = razorpay.Client(auth=('rzp_test_ZJHh8RBa1ckszG', 'TCRgeUs7oLYLjFeRemriGyAu')) 
            # payment = client.order.create({'amount': total_amount, 'currency': 'INR', 'payment_capture': 1})

            # new = PaymentModel()

            
            context = {
                'user': user,
                'book': book,
                'quantity': quantity,
                'total_amount': total_amount  
            }
            return render(request, 'pay.html', context)
    return redirect('/login')

def review(request):
    user_id = request.session.get('user_id')
    if user_id:
        user = UserModel.objects.filter(pk=user_id).first()
        if request.method == 'POST':
            book_id = request.POST.get('book_id')
            book = BookModel.objects.filter(pk=book_id).first()
            if book and user:
                username = user.user_name
                return render(request, 'review.html', {'book': book, 'username': username})
            else:
                return redirect('/error')
        else:
            return render(request, 'review.html', {'username': user.user_name})
    else:
        return redirect('/login')

def add_review(request):
    user_id = request.session.get('user_id')
    if user_id:
        if request.method == 'POST':
            book_id = request.POST.get('book_id')
            review_text = request.POST.get('review')
            user = UserModel.objects.filter(pk=user_id).first()
            book = BookModel.objects.filter(pk=book_id).first()
            if user and book:
                review = ReviewModel(review_name=review_text, user=user, book=book)
                review.save()
                return redirect('/')
            else:
                return redirect('/error')
        else:
            return redirect('/')
    else:
        return redirect('/login')