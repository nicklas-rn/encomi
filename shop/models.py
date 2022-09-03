from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager, UserManager


class Seller(models.Model):
    name = models.CharField(max_length=50, null=True)
    logo = models.ImageField(upload_to="seller_logos", default="logos/logo.png")
    etsy_url = models.CharField(max_length=300, null=True)
    delivery_price = models.FloatField(default=0)

    def __str__(self):
        return self.name


class Category(models.Model):
    title = models.CharField(max_length=30)
    seller = models.ForeignKey('Seller', null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Image(models.Model):
    image = models.ImageField(upload_to="item_images")
    item = models.ForeignKey('Item', null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.image.name


class Item(models.Model):
    title = models.CharField(max_length=1200)
    keywords = models.CharField(blank=True, null=True, max_length=1200, default='All')
    price = models.FloatField(blank=True, null=True)
    old_price = models.FloatField(blank=True, null=True)
    details = models.TextField(max_length=5000, blank=True, null=True)
    description = models.TextField(max_length=5000, blank=True, null=True)
    categories = models.ManyToManyField(Category, null=True, blank=True)
    seller = models.ForeignKey('Seller', null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class StyleGroup(models.Model):
    type = models.CharField(max_length=30)
    item = models.ForeignKey('Item', null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.type


class Style(models.Model):
    title = models.CharField(max_length=30)
    price = models.FloatField(null=True, blank=True)
    style_group = models.ForeignKey('StyleGroup', null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


ORDER_STATUS_CHOICES = {
    ('completed', 'completed'),
    ('on the way', 'on the way'),
    ('not handled', 'not handled'),
}


class ParentOrder(models.Model):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    street_name = models.CharField(max_length=200)
    house_number = models.CharField(max_length=200)
    postal_code = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    message = models.TextField(max_length=1000, null=True, blank=True)
    subtotal = models.FloatField(default=0)
    total = models.FloatField(default=0)
    datetime = models.DateTimeField(null=True)


class Order(models.Model):
    parent_order = models.ForeignKey(ParentOrder, on_delete=models.CASCADE)
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE, null=True)
    status = models.CharField(max_length=200, choices=ORDER_STATUS_CHOICES, default='not handled')
    subtotal = models.FloatField(default=0)
    total = models.FloatField(default=0)


class OrderItem(models.Model):
    item = models.ForeignKey(Item, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True)
    price = models.FloatField()
    quantity = models.IntegerField(default=1)


class OrderItemStyleGroup(models.Model):
    style_group = models.ForeignKey(StyleGroup, on_delete=models.SET_NULL, null=True)
    order_item = models.ForeignKey(OrderItem, on_delete=models.CASCADE)
    selected_style = models.ForeignKey(Style, on_delete=models.SET_NULL, null=True)


class OrderItemStyle(models.Model):
    style = models.ForeignKey(Style, on_delete=models.SET_NULL, null=True)
    order_item_style_group = models.ForeignKey(OrderItemStyleGroup, on_delete=models.CASCADE)


class CustomUserManager(BaseUserManager):

    def _create_user(self, email, password, first_name, last_name, **extra_fields):
        if not email:
            raise ValueError('Email must be provided')
        if not password:
            raise ValueError('Password is not provided')

        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            **extra_fields
        )

        user.set_password(password)
        user.save()

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password, first_name, last_name, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, first_name, last_name, **extra_fields)

    def create_superuser(self, email, password, first_name, last_name, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_superuser', True)
        return self._create_user(email, password, first_name, last_name, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(db_index=True, unique=True, max_length=100)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)

    seller = models.ForeignKey(Seller, null=True, on_delete=models.SET_NULL)

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'


class SellerApplication(models.Model):
    email = models.EmailField(max_length=100)
    shop_name = models.CharField(max_length=400)

    def __str__(self):
        return self.shop_name


type_choices = {
    ('buyer', 'buyer'),
    ('seller', 'seller'),}


class FAQ(models.Model):
    title = models.CharField(max_length=300)
    answer = models.TextField(max_length=1000)
    type = models.CharField(max_length=30, choices=type_choices, null=True)

    def __str__(self):
        return self.title


class HelpMessage(models.Model):
    email = models.EmailField(max_length=100)
    message = models.TextField(max_length=1000)

    def __str__(self):
        return self.email


class NewsletterEmail(models.Model):
    email = models.EmailField(max_length=100)
    datetime = models.DateTimeField(null=True)

    def __str__(self):
        return self.email
