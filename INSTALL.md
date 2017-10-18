# Installation

Ce manuel présente comment effectuer l'installation sans permissions d'utilisateur suprême (`sudo`), pour son utilisation sur un des ordinateurs de l'IUT. Il est parfaitement possible de court-circuiter certaines étapes, notamment pour le développement, avec des permissions de super-utilisateur.

## Table des matières

* [Installation de l'environnement virtuel](#1)
* [Installation des packages](#2)
* [Configuration de l'application](#3)
* [Importation GTFS](#4)
* [Documentation technique](#5)

<a id="1"></a>
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

<a id="2"></a>
## Installation des packages

Commencez par cloner le dépôt Git là où vous le souhaitez, puis installez les prérequis depuis le fichier `requirements.txt`.

```
~$ git clone https://github.com/DjangoChained/TchouTchouGo
~/TchouTchouGo$ pip3 install --user -r requirements.txt
```

<a id="3"></a>
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

<a id="4"></a>
## Importation GTFS

Dans l'application TchouTchouGo, connectez-vous en tant qu'administrateur, et accédez à `/admin/gtfs-import`. Un formulaire vous permettra d'envoyer les archives au format ZIP pour les données TER et Intercités de l'Open Data SNCF au format GTFS. Inutile d'effectuer le moindre traitement sur ces archives ; l'application se charge de traiter les archives, telles qu'elles sont proposées sur le site, toute seule.

<a id="5"></a>
## Documentation technique

Le dépôt contient un fichier de configuration `doxyfile` à sa racine, utilisable par [Doxygen](http://doxygen.org). Il sera nécessaire de télécharger Doxygen puis d'exécuter le programme dans le dossier racine du dépôt, celui qui contient README.md ou INSTALL.md.

```
~/TchouTchouGo$ doxygen doxyfile
```

Le fichier de configuration a été réglé pour permettre la génération de diagrammes de classes lorsqu'il y a des héritages ou des relations avec d'autres classes. Pour cela, Doxygen utilise [Graphviz](http://www.graphviz.org/), aussi connu sous le nom de `dot`. Il sera donc nécessaire d'installer Graphviz pour générer la documentation.

```
sudo apt install graphviz
```

Si cela n'est pas possible, définissez le paramètre `HAVE_DOT` à `NO` dans le fichier `doxyfile` avant de créer la documentation technique.
