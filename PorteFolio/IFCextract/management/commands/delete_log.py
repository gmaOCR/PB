from django.core.management.base import BaseCommand
import os


def run():
    cmd = Command()
    cmd.handle()


class Command(BaseCommand):
    help = 'Deletes the log.txt file in the log directory of the project'

    def handle(self, *args, **options):
        project_root = os.path.dirname(os.path.abspath(__file__))  # localise le répertoire du projet
        log_path = os.path.join(project_root, '..', '..', '..', 'log', 'log.txt')

        if os.path.exists(log_path):
            os.remove(log_path)
        else:
            pass

