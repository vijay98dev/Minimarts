from django.db import models
from django.urls import reverse




# Create your models here.
class Category(models.Model):
    category_name=models.CharField(max_length=50,unique=True)
    slug=models.SlugField(max_length=50,unique=True)
    description=models.TextField(max_length=255,blank=True)

    class Meta:
        verbose_name = ("Category")
        verbose_name_plural = ("Categories")

    def __str__(self):
        return self.category_name

    def get_absolute_url(self):
        return reverse("Category_detail", kwargs={"pk": self.pk})
