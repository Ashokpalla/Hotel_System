from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.html import escape, mark_safe


class User(AbstractUser):
    is_customer = models.BooleanField(default=False)
    is_employer = models.BooleanField(default=False)


class RoomNumber(models.Model):
    name = models.CharField(max_length=30)
    color = models.CharField(max_length=7, default='#007bff')

    def __str__(self):
        return self.name

    def get_html_badge(self):
        name = escape(self.name)
        color = escape(self.color)
        html = '<span class="badge badge-primary" style="background-color: %s">%s</span>' % (color, name)
        return mark_safe(html)


class Room(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='rooms')
    name = models.CharField(max_length=255)
    roomnumber = models.ForeignKey(RoomNumber, on_delete=models.CASCADE, related_name='rooms')

    def __str__(self):
        return self.name



class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    rooms = models.ManyToManyField(Room, through='TakenRoom')
    interests = models.ManyToManyField(RoomNumber, related_name='interested_customers')


    def __str__(self):
        return self.user.username


class TakenRoom(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='taken_rooms')
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='taken_rooms')
    date = models.DateTimeField(auto_now_add=True)
