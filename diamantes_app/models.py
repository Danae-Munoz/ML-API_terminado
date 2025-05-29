from django.db import models

class Diamond(models.Model):
    carat = models.FloatField()
    cut = models.CharField(max_length=20)
    color = models.CharField(max_length=1)
    clarity = models.CharField(max_length=10)
    depth = models.FloatField()
    table = models.FloatField()
    price = models.IntegerField()
    x = models.FloatField()
    y = models.FloatField()
    z = models.FloatField()

    def __str__(self):
        return f"{self.carat} - {self.cut} - ${self.price}"
