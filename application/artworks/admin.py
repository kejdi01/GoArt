from django.contrib import admin

from application.artworks.models import Category, Collection, Artwork, ArtworkImage

admin.site.register(Artwork)
admin.site.register(Collection)
admin.site.register(ArtworkImage)
admin.site.register(Category)


