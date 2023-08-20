import uuid
from django.db import models

# Create your models here.
class Category (models.Model):
    id=models.UUIDField(primary_key=True ,default=uuid.uuid4, editable=False)
    name=models.TextField()

class Mode (models.Model):
     id=models.UUIDField(primary_key=True ,default=uuid.uuid4, editable=False)
     name=models.TextField()

class Transaction (models.Model):
    id=models.UUIDField(primary_key=True ,default=uuid.uuid4, editable=False)
    category=models.ForeignKey(Category,on_delete=models.PROTECT,null=True)
    type=models.TextField(null=True)
    date=models.DateField()
    amount=models.DecimalField(decimal_places=2,max_digits=10)
    mode=models.ForeignKey(Mode,on_delete=models.PROTECT,null=True)
    note=models.TextField()

class ImportHistory (models.Model):
    id=models.UUIDField(primary_key=True ,default=uuid.uuid4, editable=False)
    datetime=models.DateTimeField()
    file = models.FileField(upload_to='uploads/')