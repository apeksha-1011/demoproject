from django.db import models

# Create your models here.
class ProductDetails(models.Model):
    product_name = models.CharField(max_length=100, verbose_name="Item name")
    image = models.ImageField(null=True, blank=True)
    product_description = models.TextField(null=True, blank=True)
    #product_sku = models.CharField(max_length=100, unique=True)
    product_price = models.FloatField()
    product_active = models.BooleanField(default=False)
    created_date = models.DateTimeField()

    def __str__(self):
        return self.product_name 
        
    class Meta: #this is for changing the name of the table at django adminstration.
        verbose_name_plural = "Product Details"

class Employee:
    pass

class InsuaranceDetail:
    pass

class HRDetail:
    pass 

