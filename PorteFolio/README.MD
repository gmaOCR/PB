## Résumé
Developpement de divers fonctionnalités et présentation sous forme de site navigable via
barres de menus
---
## Développement local
### Prérequis
- Interpréteur Python, version 3.11 ou supérieure
- Gestionnaire de paquets "Pip"
- Gestionnaire de paquets "npm"

Dans le reste de la documentation sur le développement local, 
il est supposé que la commande `python` de votre OS shell exécute l'interpréteur Python ci-dessus (à moins qu'un environnement virtuel ne soit activé).

#### macOS / Linux
- Recompiler Python 3.11.4 avec libbz2-dev

### Cloner le repository
- `cd /path/to/put/project/in`
- `git clone https://github.com/gmaOCR/PB.git`

### Créer et lancer l'environnement virtuel
- `pip install pipenv --user`
- `cd /path/to/PorteFolio`
- `pipenv install`
- `pipenv shell`

### Installer les modules nodes JS
S'assurer que le fichier des dépendances package.json est présent dans le répertoire "PorteFolio":
- `cd /path/to/PorteFolio/`
- `npm install`

### Créer un super user
Depuis le répertoire "PorteFolio":

- `python manage.py createsuperuser`

### Exécuter le site
- `./run_web_server.sh` ou depuis le répertoire "PorteFolio" `python manage.py runserver` 
- Aller sur `http://localhost:8000` dans un navigateur.

### Executer les migrations
- `./run_web_server.sh` ou depuis le répertoire "PorteFolio" `python manage.py makemigrations` ensuite `python manage.py migrate`

#### Base de données et création d'utilisateur
Gestion faite avec sqlite3. Pas de contrôle de mail et de sécurité à ce stade du développement.
