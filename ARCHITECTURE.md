# Architecture de la Data Platform

## 🏗️ Vue d'ensemble de l'architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                     Data Platform Architecture                   │
└─────────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────────┐
│                      INGESTION LAYER                              │
├──────────────────────────────────────────────────────────────────┤
│  • APIs externes                                                  │
│  • Fichiers (CSV, JSON, Parquet)                                 │
│  • Bases de données externes                                     │
│  • Streaming (Kafka, Pub/Sub)                                    │
└──────────────────────────────────────────────────────────────────┘
                              ↓
┌──────────────────────────────────────────────────────────────────┐
│                    STORAGE LAYER (MinIO)                          │
├──────────────────────────────────────────────────────────────────┤
│  • Stockage d'objets distribué                                   │
│  • Données brutes et traitées                                    │
│  • Backups et archives                                           │
└──────────────────────────────────────────────────────────────────┘
                              ↓
┌──────────────────────────────────────────────────────────────────┐
│                  ORCHESTRATION LAYER (Airflow)                    │
├──────────────────────────────────────────────────────────────────┤
│  • Planification des pipelines                                   │
│  • Gestion des dépendances                                       │
│  • Monitoring et alertes                                         │
│  • Retry et error handling                                       │
└──────────────────────────────────────────────────────────────────┘
                              ↓
┌──────────────────────────────────────────────────────────────────┐
│                  PROCESSING LAYER (PostgreSQL)                    │
├────────���─────────────────────────────────────────────────────────┤
│  ┌─────────────────────────────────────────────────────────────┐ │
│  │ RAW DATA LAYER                                              │ │
│  │ • customers, orders, products, order_items                 │ │
│  │ • Données originales sans transformation                   │ │
│  └─────────────────────────────────────────────────────────────┘ │
│                              ↓                                    │
│  ┌─────────────────────────────────────────────────────────────┐ │
│  │ STAGING LAYER                                               │ │
│  │ • customers_staging, orders_staging                        │ │
│  │ • Données nettoyées et validées                            │ │
│  └─────────────────────────────────────────────────────────────┘ │
│                              ↓                                    │
│  ┌─────────────────────────────────────────────────────────────┐ │
│  │ ANALYTICS LAYER                                             │ │
│  │ • customer_metrics, daily_sales                            │ │
│  │ • Données agrégées et prêtes pour l'analyse               │ │
│  └─────────────────────────────────────────────────────────────┘ │
└──────────────────────────────────────────────────────────────────┘
                              ↓
┌──────────────────────────────────────────────────────────────────┐
│                    CACHING LAYER (Redis)                          │
├──────────────────────────────────────────────────────────────────┤
│  • Cache des requêtes fréquentes                                 │
│  • Sessions utilisateur                                          │
│  • Données temporaires                                           │
└──────────────────────────────────────────────────────────────────┘
                              ↓
┌──────────────────────────────────────────────────────────────────┐
│                  PRESENTATION LAYER                               │
├──────────────────────────────────────────────────────────────────┤
│  • Grafana (Dashboards)                                          │
│  • Jupyter (Notebooks)                                           │
│  • Adminer (Database UI)                                         │
│  • APIs personnalisées                                           │
└──────────────────────────────────────────────────────────────────┘
```

## 🔄 Flux de données ETL

### Pipeline ETL Principal

```
EXTRACT
   ↓
   └─→ Lecture des données brutes
       └─→ Validation des sources
           └─→ Logging des extractions

TRANSFORM
   ↓
   └─→ Nettoyage des données
       └─→ Déduplication
           └─→ Validation des règles métier
               └─→ Enrichissement

LOAD
   ↓
   └─→ Chargement en staging
       └─→ Validation post-load
           └─→ Chargement en analytics
               └─→ Mise à jour des métriques
```

## 📊 Modèle de données

### Schéma Raw Data

```sql
raw_data.customers
├── customer_id (PK)
├── first_name
├── last_name
├── email (UNIQUE)
├── phone
├── country
├── created_at
└── updated_at

raw_data.orders
├── order_id (PK)
├── customer_id (FK → customers)
├── order_date
├── total_amount
├── status
└── created_at

raw_data.products
├── product_id (PK)
├── product_name
├── category
├── price
├── stock_quantity
└── created_at

raw_data.order_items
├── order_item_id (PK)
├── order_id (FK → orders)
├── product_id (FK → products)
├── quantity
├── unit_price
└── created_at
```

### Schéma Analytics

```sql
analytics.customer_metrics
├── customer_id (PK)
├── total_orders
├── total_spent
├── average_order_value
├── last_order_date
└── created_at

analytics.daily_sales
├── sale_date (PK)
├── total_sales
├── total_orders
├── unique_customers
└── created_at
```

## 🐳 Services Docker

### PostgreSQL (Port 5432)
- **Image**: postgres:15-alpine
- **Rôle**: Data Warehouse principal
- **Volumes**: postgres_data
- **Healthcheck**: pg_isready

### Apache Airflow (Port 8080)
- **Image**: apache/airflow:2.7.0
- **Rôle**: Orchestration des pipelines
- **Volumes**: dags, logs, plugins
- **Executor**: LocalExecutor

### Grafana (Port 3000)
- **Image**: grafana/grafana:10.0.0
- **Rôle**: Visualisation et dashboards
- **Volumes**: grafana_data
- **Datasource**: PostgreSQL

### Jupyter (Port 8888)
- **Image**: jupyter/datascience-notebook
- **Rôle**: Analyse exploratoire
- **Volumes**: notebooks, data

### MinIO (Ports 9000, 9001)
- **Image**: minio/minio
- **Rôle**: Stockage d'objets
- **Volumes**: minio_data
- **Console**: Port 9001

### Redis (Port 6379)
- **Image**: redis:7-alpine
- **Rôle**: Caching et sessions
- **Volumes**: redis_data

### Adminer (Port 8081)
- **Image**: adminer
- **Rôle**: Gestion de base de données
- **Connexion**: PostgreSQL

## 🔐 Sécurité

### Authentification
- PostgreSQL: Utilisateur/Mot de passe
- Airflow: Admin/Admin (à changer en production)
- Grafana: Admin/Admin (à changer en production)
- MinIO: minioadmin/minioadmin123 (à changer en production)

### Réseau
- Tous les services sur le réseau `data-platform`
- Communication interne via noms de service
- Ports exposés uniquement si nécessaire

### Recommandations de sécurité

1. **Changer les mots de passe par défaut** en production
2. **Utiliser des secrets** (Docker Secrets, Vault)
3. **Activer SSL/TLS** pour les connexions externes
4. **Implémenter RBAC** (Role-Based Access Control)
5. **Auditer les accès** et les modifications
6. **Sauvegarder régulièrement** les données

## 📈 Scalabilité

### Améliorations possibles

1. **Horizontal Scaling**
   - Utiliser Kubernetes au lieu de Docker Compose
   - Ajouter plusieurs workers Airflow
   - Réplication PostgreSQL

2. **Performance**
   - Partitionnement des tables
   - Indexation optimisée
   - Caching distribué avec Redis Cluster

3. **Stockage**
   - MinIO en cluster
   - Archivage des données anciennes
   - Compression des données

## 🔍 Monitoring et Logging

### Logs
- Airflow: `/opt/airflow/logs`
- PostgreSQL: Logs système
- Grafana: Logs d'application
- Tous les services: `docker-compose logs`

### Métriques
- Grafana: Dashboards personnalisés
- PostgreSQL: pg_stat_statements
- Airflow: Métriques intégrées

### Alertes
- Grafana: Règles d'alerte
- Airflow: Notifications par email
- Webhooks personnalisés

## 🚀 Déploiement en production

### Considérations

1. **Infrastructure**
   - Utiliser Kubernetes (EKS, GKE, AKS)
   - Managed services (RDS, Cloud SQL)
   - Load balancing

2. **Haute disponibilité**
   - Réplication des bases de données
   - Failover automatique
   - Backup réguliers

3. **Performance**
   - Optimisation des requêtes
   - Indexation appropriée
   - Partitionnement des données

4. **Sécurité**
   - Chiffrement des données
   - VPN/Bastion hosts
   - Audit et compliance

## 📚 Ressources

- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [Apache Airflow Documentation](https://airflow.apache.org/)
- [Grafana Documentation](https://grafana.com/docs/)
- [MinIO Documentation](https://docs.min.io/)
- [Redis Documentation](https://redis.io/documentation)
