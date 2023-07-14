import os

from PIL import Image
from django.db import models
from django.conf import settings


class Photo(models.Model):
    title = models.CharField(max_length=128, verbose_name='Titre')
    description = models.TextField(max_length=2048, blank=True)
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    image = models.ImageField(blank=True, null=True)
    thumbnail = models.ImageField(blank=True, null=True, upload_to='thumbnails')
    time_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.title}'

    IMAGE_MAX_SIZE = (200, 200)

    def save(self, *args, **kwargs):
        if not self.pk:
            # Nouvelle instance, sauvegarde normale
            super().save(*args, **kwargs)
            print("Appel de la méthode save() pour l'instance Photo")
            if self.image:
                print("L'image est présente")
                self.create_thumbnail()
        else:
            # Instance existante, vérifier si le champ image a été modifié
            original_image = Photo.objects.get(pk=self.pk).image
            if original_image != self.image:
                super().save(*args, **kwargs)
                print("Appel de la méthode save() pour l'instance Photo")
                if self.image:
                    print("L'image est présente")
                    self.create_thumbnail()
            else:
                super().save(*args, **kwargs)

    def create_thumbnail(self):
        try:
            print("Redimensionnement de l'image...")
            with Image.open(self.image.path) as image:
                image.thumbnail(self.IMAGE_MAX_SIZE)
                print("Redimensionnement thumbnail.")
                # Sauvegarder l'image redimensionnée (miniature)
                thumbnail_filename = os.path.basename(self.image.name)
                thumbnail_filename = f"thumbnail_{thumbnail_filename}"
                thumbnail_path = os.path.join(settings.MEDIA_ROOT, 'thumbnails', thumbnail_filename)
                image.save(thumbnail_path)

                # Mettre à jour l'URL du thumbnail dans le champ correspondant
                self.thumbnail = os.path.join('thumbnails', thumbnail_filename)
                self.save()
            print("Redimensionnement terminé avec succès.")
        except (IOError, OSError) as e:
            # Gérer l'erreur selon vos besoins
            print(f"Une erreur s'est produite lors du redimensionnement de l'image : {e}")
