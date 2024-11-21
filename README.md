# UE-AD-A1-REST

## Description

Ce projet est une application de réservation de films utilisant plusieurs microservices. Chaque microservice est responsable d'une partie spécifique de l'application : gestion des utilisateurs, gestion des films, gestion des horaires de projection et gestion des réservations.

Ce projet a été réalisé dans le cadre du cours d'architecture distribuée de Mme Hélène Coullon à l'IMT Atlantique. Pour plus d'informations sur le cours, vous pouvez consulter [le site de Mme Hélène Coullon](https://helene-coullon.fr/pages/ue-ad-24-25/).

## Prérequis

- Python 3.x
- pip (Python package installer)

## Installation

1. Clonez le dépôt :
    ```sh
    git clone https://github.com/Nathekip/UE-AD-A1-REST
    cd UE-AD-A1-REST
    ```

2. Installez les dépendances pour chaque microservice :
    ```sh
    pip install -r user/requirements.txt
    pip install -r movie/requirements.txt
    pip install -r showtime/requirements.txt
    pip install -r booking/requirements.txt
    ```

## Lancer le projet

Pour lancer tous les microservices en utilisant le script `runServer.py`, suivez les étapes ci-dessous :

1. Assurez-vous que vous êtes dans le répertoire racine du projet.
2. Exécutez le script `runServer.py` :
    ```sh
    python runServer.py
    ```

Ce script lancera les quatre microservices suivants :
- `user` sur le port 3203
- `movie` sur le port 3200
- `showtime` sur le port 3202
- `booking` sur le port 3201

## Utilisation

Vous pouvez maintenant accéder aux différents microservices via les URL suivantes :
- Utilisateurs : `http://127.0.0.1:3203`
- Films : `http://127.0.0.1:3200`
- Horaires de projection : `http://127.0.0.1:3202`
- Réservations : `http://127.0.0.1:3201`

## API Endpoints

### Utilisateurs
- `GET /users`: Récupérer tous les utilisateurs
- `POST /users`: Ajouter un nouvel utilisateur
- `DELETE /users/<user_id>`: Supprimer un utilisateur
- `POST /users/<user_id>/bookings`: Ajouter une réservation pour un utilisateur
- `GET /users/bookings/<user>`: Récupérer les réservations d'un utilisateur
- `GET /users/movies/<user>`: Récupérer les films réservés par un utilisateur

### Films
- `GET /movies`: Récupérer tous les films
- `POST /movies/<movieid>`: Ajouter un film
- `DELETE /movies/<movieid>`: Supprimer un film
- `PUT /movies/<movieid>/<rate>`: Mettre à jour la note d'un film
- `GET /movies/<movieid>`: Récupérer un film par son ID
- `GET /moviesbytitle`: Récupérer un film par son titre

### Horaires de projection
- `GET /showtimes`: Récupérer tous les horaires de projection
- `POST /showtimes`: Ajouter un nouvel horaire de projection
- `DELETE /showtimes/<showtimeid>`: Supprimer un horaire de projection

### Réservations
- `GET /bookings`: Récupérer toutes les réservations
- `POST /bookings/<userid>`: Ajouter une réservation pour un utilisateur
- `GET /bookings/<userid>`: Récupérer les réservations d'un utilisateur

## Licence

Ce projet est sous licence GNU.