import logging
from django.contrib.auth.models import User
from auction.models import MyUser
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from .models import ArtPiece, Auction
from .forms import ArtPieceForm, MyUserRegistrationForm
from django.db.models import Q
from django.core.mail import send_mail
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, get_object_or_404, redirect
from rest_framework.response import Response
from rest_framework.decorators import api_view


def index(request):
    auctions = Auction.objects.all()
    context = {
        'title': 'The Art Gallery',
        'auctions': auctions
    }
    return render(request, 'index.html', context)

def create_art_piece(request):
    if request.method == 'POST':
        form = ArtPieceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('art_pieces')
    else:
        form = ArtPieceForm()
    return render(request, 'create_art_piece.html', {'form': form})

def buy_now(request, art_piece_id):       
    try:
        if request.user.is_authenticated:
           art_piece = get_object_or_404(ArtPiece, pk=art_piece_id)
           if art_piece.is_sold or art_piece.is_in_active_auction():
             messages.error(request, "This art piece is already sold or in an active auction.")
             return redirect('my_collection')
            #  return redirect('art_piece_detail', art_piece_id=art_piece.id)
           if not art_piece.buy_now_price:
             messages.error(request, "This art piece does not have a buy-now price.")
             return redirect('my_collection')
             ##return redirect('art_piece_detail', art_piece_id=art_piece.id)
           if request.user.is_collector:
             art_piece.is_sold = True
             art_piece.collector = request.user
             art_piece.save()
             messages.success(request, f"Congratulations! You are now the owner of {art_piece.name}. See My Collection .")
             return redirect('my_collection')
            #  return redirect('art_piece_detail', art_piece_id=art_piece.id)
           else:
             messages.error(request, "Only collectors can buy art pieces.")
             return redirect('my_collection')
            #  return redirect('art_piece_detail', art_piece_id=art_piece.id)
        else:
          messages.error(request, "Please log in to buy this art piece.")
          return redirect('login')
    except Exception as a:    
        return redirect('login')
  


def buy_now_art_pieces(request):
    art_pieces = ArtPiece.objects.exclude(buy_now_price=None)
    return render(request, 'buy_now.html', {'art_pieces': art_pieces})

def auction_art_pieces(request):
    art_pieces = ArtPiece.objects.filter(auction__isnull=False).prefetch_related('artpiece_images')
    art_pieces_data = []
    for art_piece in art_pieces:
        images = [image.images.url for image in art_piece.artpiece_images.all()]
        art_piece_data = {
            'name': art_piece.name,
            'price': art_piece.price,
            'images': images,
            'minimum_price': art_piece.minimum_price if art_piece.is_in_active_auction() else None
        }
        art_pieces_data.append(art_piece_data)
    return render(request, 'auctions.html', {'art_pieces': art_pieces_data})

def bidd(request, art_piece_id):
    context={}
    art_piece = ArtPiece.objects.get(id=art_piece_id) 
    context['art_piece']=art_piece
    if request.user.is_authenticated:
      if request.method == 'POST':
         biddingPrice = request.POST['biddingPrice']
         if int(biddingPrice) < art_piece.minimum_price:
           print('a')
           context['message'] = 'The bid is too low. Please try again.'
         else:
           print('aa')
           art_piece.is_on_auction = False
           art_piece.is_sold = True 
           art_piece.collector = request.user
           art_piece.save()
           context['message'] = 'Congratulations!'
      print('b')     
      return render(request, 'bid.html', context)     
    print('c') 
    return render(request, 'bid.html', context)

def bid(request, art_piece_id):
    art_piece = get_object_or_404(ArtPiece, pk=art_piece_id)
    if request.method == "POST":
        form = ArtPieceForm(request.POST, instance=art_piece)
        if form.is_valid():
            form.save()
            return redirect('art_pieces') 
    else:
        form = ArtPieceForm(instance=art_piece)
    return render(request, 'update_art_piece.html', {'form': form})

def your_view(request):
    art_pieces = ArtPiece.objects.all()
    users = MyUser.objects.all() 
    context = {'art_pieces': art_pieces, 'users': users}
    return render(request, 'your_template.html', context)

def art_gallery(request):
    art_pieces = ArtPiece.objects.all()
    art_pieces = ArtPiece.objects.all().order_by('is_sold')
    return render(request, 'art_gallery.html', {'art_pieces': art_pieces})

def my_collection(request):
    user = request.user
    if user.is_authenticated:
        user_art_pieces = ArtPiece.objects.filter(collector=user)
        context = {
            'user_art_pieces': user_art_pieces
        }
        return render(request, 'my_collection.html', context)
    else:
        return redirect('login')

def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome dear {user.first_name} Collector!')
                return redirect('home')
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('home')

def register_view(request):
    if request.method == 'POST':
        form = MyUserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.save()
            messages.success(request, 'Registration successful. Please log in.')
            return redirect('login')
        else:
            messages.error(request, form.errors)
    else:
        form = MyUserRegistrationForm()
    return render(request, 'register.html', {'form': form})

def contact_us(request):
    return render(request, 'contact_us.html')

def search(request):
    query = request.GET.get('q')
    results = ArtPiece.objects.filter(name__icontains=query)
    return render(request, 'search_results.html', {'results': results})

def contact(request):
    if request.method == 'POST':
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        topic = request.POST.get('Topic')
        subject = request.POST.get('subject')

        if not firstname or not lastname or not topic or not subject:
            messages.error(request, "Please fill in all the fields.")
            return redirect('contact_us')

        send_mail(
            subject=f'Contact Form Submission: {topic}',
            message=f'Name: {firstname} {lastname}\nSubject: {subject}',
            from_email='theonlineartgalleryhl@gmail.com',
            recipient_list=['theonlineartgalleryhl@gmail.com'],
            fail_silently= False
        )

        messages.success(request, "Thank you for contacting us!")
        return redirect('contact_us')
    else:
        return redirect('contact_us')
    

