from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class User(AbstractUser):

    first_name = None
    last_name = None

    name = models.CharField(max_length=16)
    email = models.EmailField(max_length=128, blank=False, null=False, unique=True)
    username = models.CharField(max_length=64, blank=False, null=False, unique=True)
    phone = models.CharField(max_length=12, blank=False, null=False, unique=True)
    otp = models.CharField(max_length=4, blank=True, null=True)
    update_date = models.DateTimeField(auto_now=True)

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    class Meta:
        db_table = "auth_user"

    def __str__(self):
        return f"{str(self.pk)}:\t{str(self.name)}"


class ClassBase(models.Model):
    STATUS = (
        (0, "Inactive"),
        (1, "Active"),
    )

    is_active = models.IntegerField(choices=STATUS, default=1)
    insert_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Product(ClassBase):

    # category, brand, name, price, quantity, img_url, is_active, update_date, insert_date
    name = models.CharField(max_length=128)
    category = models.CharField(max_length=16)
    brand = models.CharField(max_length=16)
    price = models.PositiveIntegerField(default=10, )
    quantity = models.PositiveIntegerField(default=10, )
    image = models.ImageField(upload_to='product_images/')

    class Meta:
        db_table = "tbl_product"


class Order(ClassBase):
    """
    This will store users order.
    """
    # products = models.CharField(max_length=128, default='', help_text="Storing products id in list format")
    # product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    placed = models.BooleanField(default=True)
    total_quantity = models.PositiveIntegerField(default=1, )
    total_price = models.PositiveIntegerField(default=1, )
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    class Meta:
        db_table = "tbl_order"


class OrderList(ClassBase):
    """
    THis will store order list.
    """

    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    order = models.ForeignKey(Order, related_name='order_list', on_delete=models.CASCADE, null=True)

    class Meta:
        db_table = "tbl_order_list"

    def id(self):
        return self.product.id

    def category(self):
        return self.product.category

    def brand(self):
        return self.product.brand

    def name(self):
        return self.product.name

    def price(self):
        return self.product.price

    def quantity(self):
        return self.product.quantity

    def image(self):
        return self.product.image.url
