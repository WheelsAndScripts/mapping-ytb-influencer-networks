import sys
import io
import collecting_data


def main():
    print("Starting program")

    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

    # Étape 1 : Collecte des données via l'API YouTube
    youtube = collecting_data.ytb_api_connexion()

    channel_ids = ["UCWedHS9qKebauVIK2J7383g"]

    channel_info = collecting_data.get_channel_info(channel_ids, youtube)

    print(repr(channel_info))
    print(type(channel_info))

    # Étape 2 : Envoi des données dans Kafka (ingestion des données)

    # Étape 3 : Sauvegarde des données dans HDFS

    # Étape 4 : Transformation et traitement des données avec PySpark

    # Étape 5 : Construction du graphe avec PySpark GraphX ou NetworkX

    # Étape 6 : Génération de la visualisation


if __name__ == "__main__":
    main()
