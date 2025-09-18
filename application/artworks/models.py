from django.db import models
from django.utils.text import slugify

from application.core.models import BaseModel
from application.profiles.models import Profile


class Category(BaseModel):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)

    class Meta:
        verbose_name_plural = "Categories"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Artwork(BaseModel):
    class ArtworkStatus(models.TextChoices):
        AVAILABLE = 'AVAILABLE', 'Available'
        SOLD = 'SOLD', 'Sold'
        NOT_FOR_SALE = 'NOT_FOR_SALE', 'Not for Sale (Display Only)'

    author = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='artworks')
    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=255, unique=True, blank=True, help_text="A unique, URL-friendly version of the title.")
    description = models.TextField()
    categories = models.ManyToManyField(Category, related_name='artworks', blank=True)
    status = models.CharField(max_length=20, choices=ArtworkStatus.choices, default=ArtworkStatus.AVAILABLE)
    dimensions = models.CharField(max_length=100, blank=True, help_text="e.g., 24x36 inches, 100x70 cm")
    creation_year = models.PositiveIntegerField(null=True, blank=True)
    is_on_sale = models.BooleanField(default=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    is_public = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return f'"{self.title}" by {self.author}'


class Collection(BaseModel):
    author = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='collections')
    title = models.CharField(max_length=100)
    description = models.TextField()
    artworks = models.ManyToManyField(Artwork, related_name='in_collections', blank=True)
    is_public = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.title} (by {self.author})'


class ArtworkImage(BaseModel):
    artwork = models.ForeignKey(Artwork, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='artworks_images')
    is_cover = models.BooleanField(default=False, help_text="Is this image's cover?")

    class Meta:
        ordering = ['-is_cover']

    def __str__(self):
        return f'Image for {self.artwork.title}'