# Quiz app

# 🎨 Partie UI

***TODO***

# 🔌 Partie API

L'API, développée avec Flask, constitue le backend de notre application de quiz. Elle gère la création de questions, le réordonnancement, la participation des joueurs et l'affichage des scores. L'administration de l'API est protégée par une authentification par token JWT.

## ✅ Prérequis

Avant de commencer, assurez-vous d'avoir installé :

* **Python 3** minimum
* **pip** (le gestionnaire de paquets de Python)
* **Postman** (pour tester l'API et générer les données)

## 🛠️ Installation

1.  **Clonez le projet** : Clonez ou téléchargez ce projet sur votre machine locale.

2.  **Créez un environnement virtuel (recommandé)** : Ouvrez un terminal à la racine du projet et exécutez :
    ```
    python -m venv venv
    source venv/bin/activate  # Sur Windows: venv\Scripts\activate
    ```

3.  **Installez les dépendances** : Le projet inclut un fichier `requirements.txt`. Exécutez la commande suivante pour installer les bibliothèques nécessaires :
    ```
    pip install -r requirements.txt
    ```

## ⚙️ Configuration de Postman

Pour utiliser les collections Postman (tests et génération de données), vous devez configurer un environnement :

1.  Dans Postman, créez un nouvel environnement.
2.  Ajoutez les deux variables suivantes :
    * **`baseUrl`** : L'URL de base de votre API (par défaut : `http://127.0.0.1:5000`).
    * **`pwd`** : Le mot de passe administrateur pour accéder aux fonctions admin est `iloveflask`.

## 🚀 Lancement de l'API

Une fois l'installation terminée, lancez le serveur Flask avec la commande suivante à la racine du projet :
```
python app.py
```
L'API sera alors accessible à l'adresse `http://127.0.0.1:5000`.

## ✨ Génération de la Base de Données et du Quiz
Pour initialiser ou réinitialiser le quiz avec un jeu de questions prédéfini, utilisez la collection Postman **"Quiz - Data Generation"**.

### Étapes à suivre dans l'ordre :

1. **S'authentifier :** Lancez la requête `1 - Login as Admin`. Cela récupérera un token d'authentification nécessaire pour les étapes suivantes.

2. **Reconstruire la base :** Lancez la requête `2 - Rebuild Database`. Cela va supprimer toutes les données existantes et recréer les tables vides.

3. **Ajouter les questions :** Lancez, une par une, les requêtes `3 - Add Question ...`, `4 - Add Question ...`, etc. Cela peuplera la base de données avec votre quiz personnalisé.

Votre quiz est maintenant prêt à être utilisé.

> Alternativement, il existe un jeu de test appelé `quiz_tests.postman_collection.json` que vous pouvez utiliser pour tester la solidité de l'API.

## 📊 Schéma de la Base de Données

Le schéma de la base de données SQLite est composé de trois tables liées entre elles.

```
+----------------+       +--------------------+       +------------------+
|   questions    |       |  possible_answers  |       |  participations  |
|----------------|       |--------------------|       |------------------|
| PK id INTEGER  |------<| FK question_id INT |       | PK id INTEGER    |
| position INT   |       | id INTEGER         |       | player_name TEXT |
| title TEXT     |       | text TEXT          |       | score INTEGER    |
| text TEXT      |       | is_correct INT     |       | date TEXT        |
| image TEXT     |       +--------------------+       | answers TEXT     |
+----------------+                                    +------------------+
```

- Une question peut avoir plusieurs réponses possibles (relation un-à-plusieurs).
- Chaque participation est enregistrée indépendamment avec le nom du joueur, son score, et la date.
