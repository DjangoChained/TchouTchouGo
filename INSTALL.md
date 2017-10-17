# Installation

Ce manuel présente comment effectuer l'installation sans permissions d'utilisateur suprême (`sudo`), pour son utilisation sur un des ordinateurs de l'IUT. Il est parfaitement possible de court-circuiter certaines étapes, notamment pour le développement, avec des permissions de super-utilisateur.

## Installation de l'environnement virtuel

Assurez-vous que les environnements virtuels sont installés sur la machine :

```
python -m venv
```

Si un message d'aide sur l'utilisation de `venv` s'affiche, les environnements virtuels sont installés. Sinon, installez-le avec la commande :

```
pip install --user virtualenv
```

Ensuite, installez `virtualenvwrapper`, un assistant qui facilitera la manipulation des environnements virtuels :

```
pip install --user virtualenvwrapper
```

> `virtualenvwrapper` offre les commandes suivantes :
> * `mkvirtualenv <nom>` pour créer un environnement virtuel nommé `<nom>` ;
> * `workon <nom>` pour changer d'environnement virtuel ;
> * `rmvirtualenv <nom>` pour supprimer un environnement virtuel.

Il sera ensuite nécessaire d'ajouter à un script d'initialisation de shell (par exemple `~/.bashrc`) les lignes suivantes :

```bash
export WORKON_HOME=~/.virtualenvs
mkdir -p $WORKON_HOME
source ~/.local/bin/virtualenvwrapper.sh
```

> Modifiez la valeur de `$WORKON_HOME` pour définir le dossier qui contiendra tous vos environnements virtuels.

Vous pouvez ensuite créer immédiatement un environnement virtuel et le définir comme votre environnement de travail. Nommez-le comme vous voulez — dans ce tutoriel, on l'appellera `tchou`.

```
mkvirtualenv tchou
workon tchou
```

> Utilisez la commande `deactivate` pour sortir à tout moment d'un environnement virtuel.

## Installation des packages

Commencez par cloner le dépôt Git là où vous le souhaitez, puis installez les prérequis depuis le fichier `requirements.txt`.

```
~$ git clone https://github.com/DjangoChained/TchouTchouGo
~/TchouTchouGo$ pip3 install --user -r requirements.txt
```

## Configuration de l'application

Éditez le fichier `TchouTchouGo/settings.py` pour modifier les paramètres de connexion à la base de données. Par défaut, TchouTchouGo utilisera une base de données SQLite dans le dossier de l'application. Ensuite, créez la base de données ainsi qu'un administrateur pour l'interface d'administration :

```
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py createsuperuser
```

Vous pouvez ensuite démarrer le serveur.

```
python3 manage.py runserver
```

L'application sera disponible par défaut sur `http://localhost:8000/train/` et l'administration sur `http://localhost:8000/admin/`. Les administrateurs se connectant via l'application TchouTchouGo sont automatiquement redirigés vers l'administration.

## Importation GTFS

Dans l'application TchouTchouGo, connectez-vous en tant qu'administrateur, et accédez à `/admin/gtfs-import`. Un formulaire vous permettra d'envoyer les archives au format ZIP pour les données TER et Intercités de l'Open Data SNCF au format GTFS. Inutile d'effectuer le moindre traitement sur ces archives ; l'application se charge de traiter les archives, telles qu'elles sont proposées sur le site, toute seule.
