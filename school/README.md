# PreSkool - Système de Gestion Scolaire (Django)

## 📌 Présentation du Projet
Ce projet est une application web complète de gestion scolaire développée avec le framework **Django**. Il a été réalisé dans le cadre du projet de fin de module.

L'application couvre l'ensemble des modules requis :
- **Authentification & Rôles** (Admin, Enseignant, Étudiant)
- **Étudiants** (Gestion des étudiants et des parents)
- **Enseignants** (Gestion du personnel enseignant)
- **Départements & Matières**
- **Jours Fériés & Emploi du Temps**
- **Examens & Résultats**

---

## 🚀 Installation & Lancement

### 1. Cloner ou extraire le projet
Ouvrez votre terminal et naviguez vers le dossier du projet :
```bash
cd school
```

### 2. Créer et activer l'environnement virtuel
```bash
python -m venv monenv
# Sur Windows :
monenv\Scripts\activate
# Sur MacOS / Linux :
source monenv/bin/activate
```

### 3. Installer les dépendances
```bash
pip install -r requirements.txt
```

### 4. Appliquer les migrations
(Optionnel si la base SQLite `db.sqlite3` est déjà fournie, sinon exécuter ces commandes)
```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Lancer le serveur de développement
```bash
python manage.py runserver
```
L'application sera accessible sur : **http://127.0.0.0:8000/**

---

## 🔐 Identifiants de Test (Données Initiales)

Les identifiants suivants ont été générés avec le script `seed.py` afin de vous permettre de tester les différents rôles.

| Rôle | Email / Nom d'utilisateur | Mot de passe |
| :--- | :--- | :--- |
| **Administrateur** | `admin@preskool.com` | `adminpassword` |
| **Enseignant** | `teacher@preskool.com` | `teacherpassword` |
| **Étudiant** | `student@preskool.com` | `studentpassword` |

Pour regénérer les données de test en cas de besoin, vous pouvez exécuter :
```bash
python seed.py
```

---

## 🛠 Architecture MVT & Choix Techniques

- **Modèles avec relations avancées :** Utilisation de `OneToOneField` (Étudiant/Parent), `ForeignKey` (Département/Enseignant, Matière/Enseignant).
- **Modèle Utilisateur Personnalisé :** `CustomUser` héritant de `AbstractUser` pour implémenter les rôles Booléens (`is_admin`, `is_teacher`, `is_student`).
- **Templating complet :** Utilisation des Templates Bootstrap `PreSkool` intégrés avec les tags de template de Django.
- **Base de données :** SQLite (par défaut) facilitant le déploiement et les tests initiaux.

---

**Développé dans le cadre du module "Développement web avancé Back-end (Python)".**
