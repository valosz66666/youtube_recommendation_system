# Create your models here.
from django.db import models
from django.utils import timezone
from django.contrib import admin


class Post(models.Model):
    author = models.ForeignKey('auth.User',  # 寫入使用者的ID
                               on_delete=models.CASCADE,
                               null=False)
    title = models.CharField(max_length=200)  # 寫入使用者的標題
    text = models.TextField()  # 寫入使用者的內容
    created_date = models.DateTimeField(  # 被創造的資料 默認是現在的時間
        default=timezone.now)


class Restaurant(models.Model):
    name = models.CharField(max_length=20)
    phone_number = models.CharField(max_length=15)
    address = models.CharField(max_length=50, blank=True)


class Food(models.Model):
    name = models.CharField(max_length=20)
    price = models.DecimalField(max_digits=3, decimal_places=0)
    comment = models.CharField(max_length=50, blank=True)
    is_spicy = models.BooleanField(default=False)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)  # 包含了重要的資料表關聯性的概念

    def __str__(self):
        return self.name
