from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib import admin




class MyUser(AbstractUser):
    address = models.CharField(
        verbose_name='Address',
        help_text='User address',
        max_length=100,
        null=False

    )
    is_collector = models.BooleanField(
        verbose_name='Is Collector',
        help_text='True if user is a collector, False if admin.',
        default=True
    )

    def __str__(self):
        return self.username

class ArtPiece(models.Model):
    name = models.CharField(
        verbose_name='Art Piece Name',
        help_text='The name of the art piece',
        max_length=50,
        null=False
    )
    artist = models.CharField(
        verbose_name='Artist Name',
        help_text='The name of the artist',
        max_length=50,
        null=False,
        default="Unknown"
    )

    size = models.CharField(
        verbose_name='Size',
        help_text='The size of the art piece',
        max_length=20,
        null=False,
        default="Not specified"
    )

    year = models.PositiveIntegerField(
        verbose_name='Year',
        help_text='The year when the art piece was created',
        null=False,
        default=0
    )
    

    collector = models.ForeignKey(
        MyUser,
        verbose_name='Collector',
        help_text='The collector who owns this art piece.',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    is_sold = models.BooleanField(
        verbose_name='Is Sold',
        help_text='True if the art piece has been sold.',
        default=False
    )
    price = models.DecimalField(
        verbose_name='Price',
        help_text='The price of the art piece.',
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True
    )
    minimum_price = models.DecimalField(
        verbose_name='Minimum Price',
        help_text='The minimum price of the art piece.',
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True
    )

    def __str__(self):
        return f"{self.name} - {self.id}"

    def is_in_active_auction(self):
        return self.auction_set.filter(is_active=True).exists()


    def __str__(self):
        return f"{self.name} - {self.id}"
    
    def is_in_active_auction(self):
        return self.auction_set.filter(is_active=True).exists()

class ArtPieceImage(models.Model):
    images = models.ImageField(upload_to='art_pieces/', null=True, blank=True)
    art_piece = models.ForeignKey(ArtPiece, related_name='artpiece_images', on_delete=models.CASCADE)

    def __str__(self):
        return self.images.name


class ArtPieceVideo(models.Model):
    video = models.FileField(upload_to='art_videos/') 
    art_piece = models.ForeignKey(ArtPiece, related_name='videos', on_delete=models.CASCADE)

    def __str__(self):
        return self.video.name

class Auction(models.Model):
    name = models.CharField(
        verbose_name='Auction Name',
        help_text='The name of the auction.',
        max_length=50,
        null=False
    )
    art_pieces = models.ManyToManyField(
        ArtPiece,
        verbose_name='Art Pieces',
        help_text='Art pieces included in this auction.'
    )
 
    winning_collector = models.ForeignKey(
        MyUser,
        verbose_name='Winning Collector',
        help_text='The collector who won the auction.',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    winning_bid = models.DecimalField(
        verbose_name='Winning Bid',
        help_text='The highest bid in the auction.',
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True
    )

    is_active = models.BooleanField(
        verbose_name='Is Active',
        help_text='True if the auction is active, False otherwise.',
        default=False
    )
    def __str__(self):
        return self.name


class Bid(models.Model):
    collector = models.ForeignKey(
        MyUser,
        verbose_name='Bid Collector',
        help_text='The collector who made this bid.',
        on_delete=models.CASCADE
    )
    art_piece = models.ForeignKey(
        ArtPiece,
        verbose_name='Bid Art Piece',
        help_text='The art piece the bid was made for.',
        on_delete=models.CASCADE
    )
    auction = models.ForeignKey(
        Auction,
        verbose_name='Auction',
        help_text='The auction the bid was made in.',
        on_delete=models.CASCADE
    )
    amount = models.DecimalField(
        verbose_name='Bid Amount',
        help_text='The amount of the bid.',
        max_digits=10,
        decimal_places=2
    )

    def __str__(self):
        return f"{self.collector.username} bid {self.amount} on {self.art_piece.name} in {self.auction.name}"