import os
import googleapiclient.discovery
from dotenv import load_dotenv


def ytb_api_connexion():
    """_summary_

    Raises:
        ValueError: _description_

    Returns:
        _type_: _description_
    """

    # Remplace par ta clé API
    load_dotenv()
    API_KEY = os.getenv('YOUTUBE_API_KEY')
    if not API_KEY:
        raise ValueError("Clé API YouTube non trouvée. Vérifier le fichier .env.")

    # Création du client YouTube API
    youtube = googleapiclient.discovery.build("youtube", "v3", developerKey=API_KEY)

    return youtube


def get_channel_info(channel_ids, youtube):
    """_summary_

    Args:
        channel_ids (list): list of channel IDs
        youtube (object): the build object from googleapiclient.discovery

    Returns:
        _type_: _description_
    """

    # Appel à l'API pour récupérer les informations des chaînes
    request = youtube.channels().list(
        part="snippet,contentDetails,statistics,brandingSettings",  # On veut le snippet, le contenu et les stats
        id=",".join(channel_ids)  # On joint les IDs des chaînes
    )
    response = request.execute()  # Exécution de la requête

    # Traitement des données récupérées
    channel_data = []
    # A noter : la liste des abonnés/abonnements non dispo via l'API
    for item in response["items"]:
        # Vérification avant d'accéder à brandingSettings
        branding_settings = item.get("brandingSettings", {}).get("channel", {})
        channel_info = {
            "channel_id": item["id"],
            "channel_name": item["snippet"]["title"],
            "description": item["snippet"]["description"],
            "subscriber_count": item["statistics"]["subscriberCount"],
            "video_count": item["statistics"]["videoCount"],
            "views": item['statistics']['viewCount'],
            "playlistId": item['contentDetails']['relatedPlaylists']['uploads'],
            "featured_channels": branding_settings.get("featuredChannelsUrls", [])
        }
        channel_data.append(channel_info)

    return channel_data

