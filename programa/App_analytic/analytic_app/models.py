from django.db import models

class Type(models.TextChoices):
    GASTOS = "Gastos"
    INGRESOS = "Ingresos"

class FileJSON(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    name_type = models.CharField(
        max_length = 10,
        choice = Type.choices,
        default = Type.GASTOS
    )
    file = models.JSONField()
