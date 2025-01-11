#!/bin/bash
# Active l'environnement virtuel
echo "Activating Python virtual environment..."
source ~/Documents/Perso/Environnments/influencer_networks/Scripts/activate

# Navigue dans le dossier du projet
cd ~/Documents/Perso/Portfolios/mapping-ytb-influencer-networks

# Exécute le script Python (test du shell)
echo "Excuting the script"
python script1.py

# Étape 1 : Collecte des données via l'API YouTube

# Étape 2 : Envoi des données dans Kafka (ingestion des données)

# Étape 3 : Sauvegarde des données dans HDFS

# Étape 4 : Transformation et traitement des données avec PySpark

# Étape 5 : Construction du graphe avec PySpark GraphX ou NetworkX

# Étape 6 : Génération de la visualisation
