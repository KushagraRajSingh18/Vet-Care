from django.db import models

class Doctor(models.Model):
    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15, unique=True)
    address = models.TextField()
    email = models.EmailField(unique=True)
    village_assign = models.CharField(max_length=100)
    password = models.CharField(max_length=128)

    def __str__(self):
        return self.name

class Villager(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='villagers')
    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    address = models.TextField()
    husband_name = models.CharField(max_length=100, blank=True, null=True)
    father_name = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.name
    
class Animal(models.Model):
    villager = models.ForeignKey(Villager, on_delete=models.CASCADE, related_name='animals')
    species = models.CharField(max_length=50)
    breed = models.CharField(max_length=50)
    tag_no = models.CharField(max_length=50)
    sex = models.CharField(max_length=10)
    color = models.CharField(max_length=30)
    age = models.CharField(max_length=30)
    height_cm = models.IntegerField()
    horn_type = models.CharField(max_length=30)
    tail_switch = models.CharField(max_length=30)
    purpose = models.CharField(max_length=50)
    milk_yield = models.FloatField()
    approx_cost = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.species} - {self.tag_no}"
