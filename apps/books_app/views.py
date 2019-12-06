from django.shortcuts import render, redirect, HttpResponse
from .models import User, Book
from django.contrib import messages
import bcrypt

def index(request):
    print('*'*80)
    print("in the index method")
    if 'user' in request.session:    
        del request.session['user']
    return render (request, 'books_app/index.html')

def register(request):
    print('*'*80)
    print("in the register method")
    if request.method =='POST':
        errors = User.objects.basic_validator(request.POST)
        if len(errors)>0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect ('/')
        else:
            password=request.POST['password']
            pw_hash=bcrypt.hashpw(password.encode(), bcrypt.gensalt())
            new_user = User.objects.create(first_name=request.POST['first_name'], last_name=request.POST['last_name'], email=request.POST['email'], password=pw_hash.decode())
            request.session['user']=request.POST['first_name']
            request.session['user_id']=new_user.id
            return redirect ('/books')
    return redirect ('/')

def login(request):
    print('*'*80)
    print("in the login method")
    if request.method =='POST':
        errors = User.objects.login_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/')
        else:
            user=User.objects.filter(email=request.POST['email'])
            logged_user=user[0]
            request.session['user'] = logged_user.first_name
            request.session['user_id']=logged_user.id
            return redirect ('/books')
    else:
        return redirect ('/')

def books(request):
    print('*'*80)
    print("in the books method")
    print("liked", User.objects.filter(id=request.session['user_id'])) 
    context = {
        'allbooks' : Book.objects.all(),
        'addedby' : Book.objects.first().uploaded_by,
        'liked' : User.objects.filter(id=request.session['user_id']).first().liked_books.all()
    }
    return render (request, 'books_app/books.html', context)

def books_id(request, book_id):
    print('*'*80)
    print("in the books_id method")
    thisuser=Book.objects.get(id=book_id).user_who_like.all()
    thisbook=Book.objects.get(id=book_id)
    likedthisbook=Book.objects.get(id=book_id).user_who_like.filter(id=request.session['user_id'])
    context = {
        'thisuser' : thisuser,
        'thisbook' : thisbook,
        'likedthisbook': likedthisbook,
    }
    return render (request, 'books_app/books_id.html', context)

def books_ad(request):
    print('*'*80)
    print("in the books_ad method")
    if request.method =='POST':
        errors = User.objects.book_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/books')
        else: 
            user_id=request.session['user_id']
            bookobject=Book.objects.create(title=request.POST['title'], description=request.POST['description'], uploaded_by=User.objects.get(id=user_id))
            this_user=User.objects.get(id=user_id)
            bookid=bookobject.id
            bookobject.user_who_like.add(this_user)
            return redirect ('/books/'+str(bookid))

def books_id_update(request, book_id):
    print('*'*80)
    print("in the books_id_update method")
    if request.method =='POST': 
        updates=Book.objects.get(id=book_id)
        updates.title=request.POST['title']
        updates.description=request.POST['description']
        updates.save()
        return redirect ('/books/'+book_id)
    else:
        return redirect ('/books')

def favorite(request, book_id):
    print('*'*80)
    print("in the favorite method")
    user_id=request.session['user_id']
    bookobject=Book.objects.get(id=book_id)
    this_user=User.objects.get(id=user_id)
    bookobject.user_who_like.add(this_user)
    return redirect ('/books')


def unfavorite(request, book_id):
    print('*'*80)
    print("in the unfavorite method")
    user_id=request.session['user_id']
    bookobject=Book.objects.get(id=book_id)
    this_user=User.objects.get(id=user_id)
    bookobject.user_who_like.remove(this_user)
    return redirect ('/books')

def destroy(request, book_id):
    print('*'*80)
    print("in the destroy method")
    deleted=Book.objects.get(id=book_id)
    deleted.delete()
    return redirect ('/books')

def books_id_edit(request, book_id):
    print('*'*80)
    print("in the edit method")
    thisbook=Book.objects.get(id=book_id)
    context = {
        'thisbook' : thisbook
    }
    return render (request, 'books_app/book_id_edit.html', context)
