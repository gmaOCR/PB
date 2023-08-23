from django.core.management.base import BaseCommand
from django.conf import settings
import os
import datetime


def run():
    cmd = Command()
    cmd.handle()


def delete_ifc_files(folder_path, retention_period_minutes=5):
    current_time = datetime.datetime.now()
    ifc_files = [filename for filename in os.listdir(folder_path) if filename.endswith(".ifc")]

    for filename in ifc_files:
        file_path = os.path.join(folder_path, filename)
        if os.path.isfile(file_path):
            creation_time = datetime.datetime.fromtimestamp(os.path.getctime(file_path))
            if current_time - creation_time > datetime.timedelta(minutes=retention_period_minutes):
                os.remove(file_path)
                timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                print(f"[{timestamp}] Deleted: {folder_path}/{filename}")

    # Check for subdirectories and call the function recursively
    for item in os.listdir(folder_path):
        item_path = os.path.join(folder_path, item)
        if os.path.isdir(item_path):
            delete_ifc_files(item_path, retention_period_minutes)


class Command(BaseCommand):
    help = 'Cleans the IFC files in the media/ifc directory recursively'

    def handle(self, *args, **options):
        base_folder = os.path.join(settings.MEDIA_ROOT, 'ifc')
        if not os.listdir(base_folder):
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.stdout.write(f"[{timestamp}] Rien à supprimer.")
            return

        delete_ifc_files(base_folder)
