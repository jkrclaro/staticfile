from django.db import models

from phonenumber_field.modelfields import PhoneNumberField


class Contact(models.Model):
    email = models.EmailField(max_length=254)
    phone = PhoneNumberField()
    job = models.CharField(max_length=254)
    website = models.URLField(max_length=200)
    address = models.CharField(max_length=254)
    birthday = models.DateField()
    company = models.CharField(max_length=254)
    agent = models.CharField(max_length=254)
    background = models.TextField()

    class Meta:
        db_table = 'sidefone_contacts'