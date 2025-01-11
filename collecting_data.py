import os
import googleapiclient.discovery
from dotenv import load_dotenv


def ytb_api_connexion():
    """
    Initializes a connection to the YouTube Data API v3 using an API key stored in a .env file.

    Raises:
        ValueError: If the YouTube API key is not found in the .env file or is invalid.

    Returns:
        googleapiclient.discovery.Resource: A YouTube API client instance ready to make requests.
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
    """
    Retrieves detailed information about a list of YouTube channels using the YouTube Data API v3.

    Args:
        channel_ids (list): A list of YouTube channel IDs to fetch information for.
        youtube (googleapiclient.discovery.Resource): An instance of the YouTube API client.

    Returns:
        list: A list of dictionaries, each containing the following details about a channel:
            - channel_id (str): The unique ID of the channel.
            - channel_name (str): The name of the channel.
            - description (str): The description of the channel.
            - subscriber_count (str): The number of subscribers to the channel.
            - video_count (str): The total number of videos uploaded by the channel.
            - views (str): The total number of views on the channel.
            - playlistId (str): The ID of the playlist containing the channel's uploads.
            - featured_channels (list): A list of featured channel URLs (if available).

    Notes:
        The list of subscribers or subscriptions for a channel is not available via the YouTube Data API.

    Raises:
        KeyError: If any expected fields are missing in the API response.

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

