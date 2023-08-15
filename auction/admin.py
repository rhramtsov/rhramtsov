from django.contrib import admin
from .models import MyUser, ArtPiece, ArtPieceImage, ArtPieceVideo, Auction, Bid
from django.contrib.auth.admin import UserAdmin


class ArtPieceImageInline(admin.TabularInline):
    model = ArtPieceImage
    extra = 5


class ArtPieceVideoInline(admin.TabularInline):
    model = ArtPieceVideo
    extra = 5


class ArtPieceAdmin(admin.ModelAdmin):
    inlines = [ArtPieceImageInline, ArtPieceVideoInline]
    list_display = ['name']


admin.site.register(MyUser, UserAdmin)
admin.site.register(ArtPiece, ArtPieceAdmin)
admin.site.register(Auction)
admin.site.register(Bid)
