# Quiz app par Zackary SAADA et Jovan RAHME

# 🔌 Partie API

L'API, développée avec Flask, constitue le backend de notre application de quiz. Elle gère la création de questions, le réordonnancement, la participation des joueurs et l'affichage des scores. L'administration de l'API est protégée par une authentification par token JWT.

## ✅ Prérequis

Avant de commencer, assurez-vous d'avoir installé :

* **Python 3** minimum
* **pip** (le gestionnaire de paquets de Python)
* **Postman** (pour tester l'API et générer les données)

## 🛠️ Installation

1.  **Clonez le projet** : Clonez ou téléchargez ce projet sur votre machine locale.

2.  **Accédez au répertoire de l'API** : Ouvrez un terminal à la racine du projet et déplacez-vous dans le dossier `quiz_api`.
    ```bash
    cd quiz_api
    ```

3.  **Créez un environnement virtuel (recommandé)** : Ouvrez un terminal à la racine du projet et exécutez :
    ```bash
    python -m venv venv
    source venv/bin/activate  # Sur Windows: venv\Scripts\activate
    ```

4.  **Installez les dépendances** : Le projet inclut un fichier `requirements.txt`. Exécutez la commande suivante pour installer les bibliothèques nécessaires :
    ```bash
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
```bash
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
+----------------+      +--------------------+      +------------------+
|   questions    |      |  possible_answers  |      |  participations  |
|----------------|      |--------------------|      |------------------|
| PK id INTEGER  |-----<| FK question_id INT |      | PK id INTEGER    |
| position INT   |      | id INTEGER         |      | player_name TEXT |
| title TEXT     |      | text TEXT          |      | score INTEGER    |
| text TEXT      |      | is_correct INT     |      | date TEXT        |
| image TEXT     |      +--------------------+      | answers TEXT     |
+----------------+                                  +------------------+
```

- Une question peut avoir plusieurs réponses possibles (relation un-à-plusieurs).
- Chaque participation est enregistrée indépendamment avec le nom du joueur, son score, et la date.

#  🎨 Partie UI

L'interface utilisateur (UI), développée avec **Vue.js 3** (utilisant la Composition API), **Vite.js** et **Vue Router**, offre une expérience interactive pour les joueurs et un panneau d'administration complet pour la gestion du quiz.

## ✅ Prérequis

Avant de commencer, assurez-vous d'avoir installé :

* **Node.js** (version 18 ou supérieure recommandée)
* **npm** (généralement inclus avec Node.js)

## 🛠️ Installation

1.  **Accédez au répertoire de l'UI** : Ouvrez un terminal à la racine du projet et déplacez-vous dans le dossier `quiz-ui`.
    ```bash
    cd quiz-ui
    ```

2.  **Installez les dépendances** : Exécutez la commande suivante pour installer les bibliothèques nécessaires définies dans `package.json`:
    ```bash
    npm install
    ```

## ⚙️ Configuration

L'interface utilisateur doit pouvoir communiquer avec l'API. L'URL de l'API est configurée dans le fichier `src/services/QuizApiService.js`.

Par défaut, l'URL est `http://localhost:5000`. Si votre API fonctionne sur un port ou une adresse différente, assurez-vous de mettre à jour la constante `API_URL` dans ce fichier.

```javascript
// quiz-ui/src/services/QuizApiService.js

const API_URL = 'http://localhost:5000'; 
// ...
```

Assurez-vous que la [partie API](#-partie-api) est lancée et accessible à cette adresse avant de lancer l'UI.

Si vous n'avez pas lancé la collection Postman de génération de données,  
⚠️⚠️ **<ins>Pensez à initialiser</ins> la base de données avec le bouton** "*Réinitialiser la base de données*" **dans la <ins>page admin</ins>** ! ⚠️⚠️  
Les échanges entre l'UI et l'API ne fonctionneront pas sinon.

## 🚀 Lancement de l'UI

Une fois l'installation terminée, lancez le serveur de développement Vite avec la commande suivante depuis le dossier `quiz-ui`:
```bash
npm run dev
```
L'application sera alors accessible à l'adresse indiquée dans le terminal (généralement `http://localhost:3000`).

## ✨ Fonctionnalités

L'application se compose de trois grandes sections accessibles via la navigation :

### 1. Espace Joueur

* **Page d'accueil (`/`)** : Point d'entrée de l'application, elle propose de démarrer une nouvelle partie ou de consulter le tableau des scores.
* **Démarrer un quiz (`/quiz`)** :
    * Le joueur doit d'abord entrer un pseudonyme pour commencer.
    * Le quiz se déroule question par question, avec un affichage clair du titre, de l'énoncé, de l'image (si disponible) et des quatre propositions de réponse.
    * Après avoir répondu à la dernière question, le joueur est redirigé vers la page des scores.
* **Tableau des scores (`/scores`)** : Affiche le classement des 10 meilleures participations, avec le nom du joueur, son score et la date de sa participation.

### 2. Panneau d'Administration

Accessible via le bouton "Admin" sur la page d'accueil.

* **Page de connexion (`/admin`)** : L'accès au panneau d'administration est protégé par un mot de passe. Le mot de passe requis est `iloveflask`.

* **Gestionnaire de questions (`/admin/questions`)** : Une fois authentifié, l'administrateur accède à une interface complète pour gérer le contenu du quiz :
    * **Liste des questions** : Affiche toutes les questions existantes avec leur titre.
    * **Réordonnancement** : Les questions peuvent être réorganisées en changeant leur position. La nouvelle position et celle des autres sont sauvegardées automatiquement via un appel à l'API.
    * **Création et Édition** : Un formulaire permet d'ajouter une nouvelle question ou de modifier une question existante. Le formulaire inclut des champs pour :
        * Le titre de la question.
        * Le texte (énoncé) de la question.
        * Le téléchargement d'une image associée.
        * Plusieurs réponses possibles (de 2 à n).
        * La sélection de la bonne réponse via un bouton radio.
    * **Suppression** : Chaque question peut être supprimée individuellement (2 minimum).
