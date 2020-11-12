from django.db import models


class Product(models.Model):
    title = models.CharField(max_length=50)
    price = models.IntegerField()
    description = models.TextField(max_length=400)
    seller = models.ForeignKey('auth.user', on_delete=models.CASCADE)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def get_image_filename(instance, filename):
        id = instance.product.id
        return "post_images/%s" % (id)


class Category(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class ProductImage(models.Model):
    product = models.ForeignKey('store.Product', on_delete=models.CASCADE, related_name='images')
    img = models.ImageField(upload_to='images/', verbose_name='')

    def __str__(self):
        return self.img.url
