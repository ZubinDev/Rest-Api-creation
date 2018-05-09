from django.db import models

class Customer(models.Model):
    customer_name = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=5)
    address = models.CharField(max_length=150)


class Circuit(models.Model):
    customer = models.ForeignKey('Customer', on_delete=models.CASCADE)
    circuit_id = models.CharField(max_length=50)
    mep_id = models.CharField(max_length=50)
    cir_az = models.IntegerField()
    cir_za = models.IntegerField()


class Site(models.Model):
    circuit = models.ForeignKey('Circuit', on_delete=models.CASCADE)
    ip = models.GenericIPAddressField()
    hw_version = models.CharField(max_length=30)
    type = models.CharField(max_length=10)

