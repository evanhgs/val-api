# Valenstagram API v2

API FastAPI pour le projet Valenstagram.

## Installation rapide (Développement)

### 1. Cloner le projet et préparer l'environnement
```bash
cp .env.example .env
# editer le .env si nécessaire
```

### 2. Démarrer l'infrastructure (Base de données & MQTT)
```bash
make infra-up
```

### 3. Lancer l'API localement
```bash
python3 -m venv .venv
source .venv/bin/activate
# venv\Scripts\activate   # Sur Windows

pip install -r requirements.txt

# mettre a jour les tables bdd
make migrate

make run
```
L'API est alors accessible sur : [http://localhost:5000/api/docs](http://localhost:5000/api/docs)

## Commandes utiles (Makefile)

- `make infra-up` : Démarre PostgreSQL et Mosquitto en Docker.
- `make infra-down` : Arrête l'infrastructure Docker.
- `make migrate` : Applique les dernières migrations de base de données.
- `make run` : Lance l'API FastAPI avec rechargement automatique.
- `make test` : Lance tous les tests.
- `make clean` : Nettoie les conteneurs et les fichiers temporaires.

## Tests
Assurez-vous que l'infrastructure est lancée (`make infra-up`) puis :
```bash
make test
```
