import sys
import io
import collecting_data


def main():
    print("Starting program")

    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

    # Étape 1 : Collecte des données via l'API YouTube
    youtube = collecting_data.ytb_api_connexion()  # Connection to the YouTube Data API

    channel_ids = ["UCWedHS9qKebauVIK2J7383g"]  # Channels we are working with

    channel_info = collecting_data.get_channel_info(channel_ids, youtube)  # getting channel info
    playlist_id = channel_info[0]["playlistId"]  # playlistID for the first channel

    videos_id = collecting_data.get_video_ids(playlist_id, youtube)  # getting all videos id for the first ytb channel in a list
    videos_list = collecting_data.get_video_details(videos_id, youtube)  # getting info for all videos of one ytb channel

    # print(repr(channel_info))
    # print(type(channel_info))
    print(len(videos_list))

    # Étape 2 : Envoi des données dans Kafka (ingestion des données)

    # Étape 3 : Sauvegarde des données dans HDFS

    # Étape 4 : Transformation et traitement des données avec PySpark

    # Étape 5 : Construction du graphe avec PySpark GraphX ou NetworkX

    # Étape 6 : Génération de la visualisation


if __name__ == "__main__":
    main()
