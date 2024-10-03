from django.db import models
from user.models import User
from django.utils import timezone


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to="categories/", blank=True, null=True)
    slug = models.SlugField(max_length=100, unique=True)

    class Meta:
        verbose_name = "Kategoriya"
        verbose_name_plural = "Kategoriyalar"

    def __str__(self):
        return self.name

    def get_image(self):
        if self.image:
            return self.image.url
        return False

    def get_products(self):
        return self.products.filter(available=True)


class Product(models.Model):
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    description = models.TextField()
    information = models.TextField(null=True, blank=True, default="Ma'lumot yo'q")

    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Narx: $")
    measurement_unit = models.CharField(max_length=50, choices=[
        ('kg', 'Kilogram'),
        ('dona', 'Dona'),
        ('l', 'Litr'),
        ('m', 'Metr'),
    ], default='kg', verbose_name="Birlik")
    discount = models.DecimalField(max_digits=4, decimal_places=2, default=0)
    is_discount = models.BooleanField(default=False)
    stock = models.IntegerField()
    image = models.ImageField(upload_to='products/', blank=True, null=True)

    available = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Mahsulot'
        verbose_name_plural = 'Mahsulotlar'

    def __str__(self):
        return self.name

    def get_image(self):
        if self.image:
            return self.image.url
        return False

    def current_price(self):
        if self.is_discount:
            return round(self.price * (1 - self.discount/100), 2)
        return self.price

    def get_rating(self):
        comments = self.comments.all()
        if comments.exists():
            return '{:.2f}'.format(sum(comment.rating for comment in comments) / comments.count())
        return 0

    def get_rating2x(self):
        return self.get_rating() * 2


class Comment(models.Model):
    product = models.ForeignKey(Product, related_name='comments', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    rating = models.PositiveIntegerField(default=1, choices=[(i, i) for i in range(1, 6)])
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return f'Sharh {self.user.username} tomonidan {self.product.name} uchun'
