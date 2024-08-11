from django.db import models
from django.utils.text import slugify

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    publication_date = models.DateField()
    category = models.CharField(max_length=50)
    description = models.TextField()
    status = models.CharField(max_length=50)
    score = models.IntegerField()
    pdf = models.FileField(upload_to='books/pdfs/')
    cover_image = models.ImageField(upload_to='books/covers/')
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
