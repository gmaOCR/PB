from django.db import models


class IFCFile(models.Model):
    file = models.FileField(upload_to='ifc')
