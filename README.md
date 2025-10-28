# Data Platform - Démonstrateur Open Source avec Docker

Un démonstrateur complet d'une plateforme de données moderne utilisant des outils open source et Docker.

## 🎯 Vue d'ensemble

Cette plateforme démontre une architecture complète de data platform incluant :

- **Ingestion de données** : PostgreSQL comme data warehouse
- **Orchestration** : Apache Airflow pour les pipelines ETL
- **Stockage d'objets** : MinIO pour le stockage distribué
- **Mise en cache** : Redis pour la performance
- **Visualisation** : Grafana pour les dashboards + React Dashboard moderne
- **Analyse** : Jupyter pour l'exploration de données
- **Gestion** : Adminer pour l'administration de base de données
- **API Backend** : Flask API pour les données du dashboard

## 📋 Prérequis

- Docker Desktop (version 20.10+)
- Docker Compose (version 1.29+)
- Au minimum 8 GB de RAM disponible
- 20 GB d'espace disque libre

### Installation de Docker

**Windows/Mac:**
- Télécharger [Docker Desktop](https://www.docker.com/products/docker-desktop)
- Installer et redémarrer

**Linux:**
```bash
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER
```

## 🚀 Démarrage rapide

### 1. Cloner ou télécharger le projet

```bash
cd c:\Users\TUF\Desktop\docker
```

### 2. Démarrer les services

**Windows:**
```bash
start.bat
```

**Linux/Mac:**
```bash
chmod +x start.sh
./start.sh
```

**Ou directement avec Docker Compose:**
```bash
docker-compose up -d
```

### 3. Vérifier le statut

```bash
docker-compose ps
```

### 4. Accéder aux services

Une fois les services démarrés, accédez à :

| Service | URL | Identifiants |
|---------|-----|--------------|
| **React Dashboard** | http://localhost:3000 | - |
| **API Backend** | http://localhost:8000 | - |
| **Airflow** | http://localhost:8080 | admin / admin |
| **Grafana** | http://localhost:3001 | admin / admin |
| **Jupyter** | http://localhost:8888 | Pas de mot de passe |
| **Adminer** | http://localhost:8081 | datauser / datapass123 |
| **MinIO** | http://localhost:9001 | minioadmin / minioadmin123 |
| **PostgreSQL** | localhost:5432 | datauser / datapass123 |
| **Redis** | localhost:6379 | Pas de mot de passe |

## 📊 Architecture de la base de données

### Schémas

La base de données est organisée en trois couches :

#### 1. **raw_data** - Couche brute
Contient les données originales sans transformation :
- `customers` - Informations clients
- `orders` - Commandes
- `products` - Produits
- `order_items` - Détails des commandes

#### 2. **staging** - Couche intermédiaire
Données transformées et nettoyées :
- `customers_staging` - Clients nettoyés
- `orders_staging` - Commandes nettoyées

#### 3. **analytics** - Couche analytique
Données agrégées pour l'analyse :
- `customer_metrics` - Métriques clients
- `daily_sales` - Ventes quotidiennes

## 🔄 Pipelines ETL

### Pipeline ETL Principal (`etl_pipeline.py`)

Exécution quotidienne à 2h du matin :

1. **Extract** - Extraction des données brutes
2. **Transform** - Nettoyage et transformation
3. **Load** - Chargement en couche analytique

### Pipeline de Maintenance (`maintenance_pipeline.py`)

Exécution hebdomadaire le dimanche à 3h du matin :

1. **Vacuum** - Optimisation de la base de données
2. **Quality Check** - Vérification de la qualité des données
3. **Report** - Génération de rapports

## 📈 Utilisation

### Charger des données de test

```bash
docker-compose exec postgres python /scripts/load_sample_data.py
```

### Consulter les logs

```bash
# Tous les services
docker-compose logs -f

# Service spécifique
docker-compose logs -f airflow-webserver
docker-compose logs -f postgres
docker-compose logs -f grafana
```

### Accéder à la base de données

**Via Adminer (interface web):**
- URL: http://localhost:8081
- Serveur: postgres
- Utilisateur: datauser
- Mot de passe: datapass123
- Base de données: datawarehouse

**Via psql (ligne de commande):**
```bash
docker-compose exec postgres psql -U datauser -d datawarehouse
```

### Exécuter des requêtes SQL

```bash
docker-compose exec postgres psql -U datauser -d datawarehouse -c "SELECT * FROM raw_data.customers LIMIT 5;"
```

### Analyser les données avec Jupyter

1. Accédez à http://localhost:8888
2. Ouvrez `notebooks/data_analysis.ipynb`
3. Exécutez les cellules pour explorer les données

## 🛠️ Gestion des services

### Arrêter les services

```bash
docker-compose down
```

### Arrêter et supprimer les volumes (réinitialiser)

```bash
docker-compose down -v
```

### Redémarrer un service

```bash
docker-compose restart [service_name]
```

### Voir les ressources utilisées

```bash
docker stats
```

## 📝 Configuration

### Variables d'environnement

Modifiez le fichier `.env` pour personnaliser :

```env
POSTGRES_USER=datauser
POSTGRES_PASSWORD=datapass123
POSTGRES_DB=datawarehouse
GF_SECURITY_ADMIN_PASSWORD=admin
MINIO_ROOT_USER=minioadmin
MINIO_ROOT_PASSWORD=minioadmin123
```

### Modifier les ports

Éditez `docker-compose.yml` et changez les mappings de ports :

```yaml
ports:
  - "5432:5432"  # Changer le premier nombre pour un autre port
```

## 🔍 Dépannage

### Les services ne démarrent pas

```bash
# Vérifier les logs
docker-compose logs

# Vérifier les ports disponibles
netstat -ano | findstr :8080  # Windows
lsof -i :8080  # Linux/Mac
```

### Erreur de connexion à PostgreSQL

```bash
# Vérifier que PostgreSQL est prêt
docker-compose exec postgres pg_isready -U datauser

# Attendre quelques secondes et réessayer
```

### Airflow ne démarre pas

```bash
# Réinitialiser la base de données Airflow
docker-compose exec airflow-webserver airflow db reset

# Recréer l'utilisateur admin
docker-compose exec airflow-webserver airflow users create \
  --username admin \
  --password admin \
  --firstname Admin \
  --lastname User \
  --role Admin \
  --email admin@example.com
```

### Problèmes de mémoire

Augmentez les ressources Docker :
- Docker Desktop → Preferences → Resources
- Augmentez CPU et Memory

## 📚 Ressources supplémentaires

- [Documentation PostgreSQL](https://www.postgresql.org/docs/)
- [Documentation Apache Airflow](https://airflow.apache.org/docs/)
- [Documentation Grafana](https://grafana.com/docs/)
- [Documentation Jupyter](https://jupyter.org/documentation)
- [Documentation MinIO](https://docs.min.io/)
- [Documentation Redis](https://redis.io/documentation)

## 🤝 Contribution

Pour améliorer ce démonstrateur :

1. Créer une branche feature
2. Faire vos modifications
3. Tester les changements
4. Soumettre une pull request

## 📄 Licence

Ce projet est fourni à titre d'exemple éducatif.

## 📞 Support

Pour les problèmes ou questions :

1. Vérifier les logs : `docker-compose logs`
2. Consulter la section Dépannage
3. Vérifier les ressources système disponibles

---

**Dernière mise à jour:** 2024
**Version:** 1.0.0
