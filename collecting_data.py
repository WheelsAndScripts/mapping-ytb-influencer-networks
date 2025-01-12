import os
import googleapiclient.discovery
from dotenv import load_dotenv


def ytb_api_connexion():
    """
    Initializes a connection to the YouTube Data API v3 using an API key stored in a .env file

    Raises:
        ValueError: If the YouTube API key is not found in the .env file or is invalid

    Returns:
        googleapiclient.discovery.Resource: A YouTube API client instance ready to make requests
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
    Retrieves detailed information about a list of YouTube channels using the YouTube Data API v3

    Args:
        - channel_ids (list): A list of YouTube channel IDs to fetch information for
        - youtube (googleapiclient.discovery.Resource): An instance of the YouTube API client

    Returns:
        list: A list of dictionaries, each containing the following details about a channel:
            - channel_id (str): The unique ID of the channel
            - channel_name (str): The name of the channel
            - description (str): The description of the channel
            - subscriber_count (str): The number of subscribers to the channel
            - video_count (str): The total number of videos uploaded by the channel
            - views (str): The total number of views on the channel
            - playlistId (str): The ID of the playlist containing the channel's uploads
            - featured_channels (list): A list of featured channel URLs (if available)

    Notes:
        The list of subscribers or subscriptions for a channel is not available via the YouTube Data API

    Raises:
        KeyError: If any expected fields are missing in the API response

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


def get_video_ids(playlist_id, youtube):
    """
    Get list of video IDs of all videos in the given playlist (= one ytb channel)

    Args:
        - youtube (googleapiclient.discovery.Resource): the build object from googleapiclient.discovery
        - playlist_id (str): playlist ID of the channel
    
    Returns:
        List of video IDs of all videos in the playlist
  
    """
 
    request = youtube.playlistItems().list(
                part='contentDetails',
                playlistId=playlist_id,
                maxResults=50)
    response = request.execute()
    
    video_ids = []

    for i in range(len(response['items'])):
        video_ids.append(response['items'][i]['contentDetails']['videoId'])
 
    next_page_token = response.get('nextPageToken')
    more_pages = True

    while more_pages:
        if next_page_token is None:
            more_pages = False
        else:
            request = youtube.playlistItems().list(
                        part='contentDetails',
                        playlistId=playlist_id,
                        maxResults=50,
                        pageToken=next_page_token)
            response = request.execute()

            for i in range(len(response['items'])):
                video_ids.append(response['items'][i]['contentDetails']['videoId'])
       
            next_page_token = response.get('nextPageToken')
  
    return video_ids


def get_video_details(video_ids, youtube):
    """
    Get video statistics of all videos with given IDs

    Args:
        - video_ids (list): list of video IDs for one ytb channel
        - youtube (googleapiclient.discovery.Resource): the build object from googleapiclient.discovery

    Returns:
        list: A list of dictionaries, each containing detailed statistics and metadata for a video:
            - video_id (str): The unique ID of the video
            - channelTitle (str): The name of the channel that uploaded the video
            - title (str): The title of the video
            - description (str): The description of the video
            - tags (list): A list of tags associated with the video
            - publishedAt (str): The upload date and time of the video in ISO 8601 format
            - viewCount (str): The total number of views for the video
            - likeCount (str): The total number of likes for the video
            - commentCount (str): The total number of comments on the video
            - duration (str): The duration of the video in ISO 8601 format (e.g., PT2M30S)
    """
        
    all_video_info = []

    for i in range(0, len(video_ids), 50):
        request = youtube.videos().list(
            part="snippet,contentDetails,statistics",
            id=','.join(video_ids[i:i+50])
        )
        response = request.execute()

        for video in response['items']:
            stats_to_keep = {'snippet': ['channelTitle', 'title', 'description', 'tags', 'publishedAt'],
                             'statistics': ['viewCount', 'likeCount', 'commentCount'],
                             'contentDetails': ['duration']
                            }
            video_info = {}
            video_info['video_id'] = video['id']

            for k in stats_to_keep.keys():
                for v in stats_to_keep[k]:
                    try:
                        video_info[v] = video[k][v]
                    except:
                        video_info[v] = None

            all_video_info.append(video_info)
            
    return all_video_info