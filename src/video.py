from src.channel import api_key
from googleapiclient.discovery import build
from pprint import pprint


class Video:
    youtube = build('youtube', 'v3', developerKey=api_key)

    def __init__(self, video_id: str) -> None:
        """
        Экземпляр инициализируется id видео. Дальше все данные будут подтягиваться по API
        """
        self.video_id = video_id
        self.video_response = Video.youtube.videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                                              id=self.video_id).execute()
        #pprint(self.video_response)

        try:
            self.title: str = self.video_response['items'][0]['snippet']['title']

        except IndexError:
            print('Incorrect_video_id')
            self.title = None
            self.view_count = None
            self.like_count = None
            self.comment_count = None
        else:
            self.title: str = self.video_response['items'][0]['snippet']['title']
            self.url = "https://www.youtube.com/" + self.video_response.get('items')[0].get('etag')
            self.view_count: int = self.video_response['items'][0]['statistics']['viewCount']
            self.like_count: int = self.video_response['items'][0]['statistics']['likeCount']
            self.comment_count: int = self.video_response['items'][0]['statistics']['commentCount']

    def __str__(self):
        return self.title


class PLVideo(Video):
    def __init__(self, video_id: str, playlist_id: str) -> None:
        """
        Экземпляр инициализируется id видео и id плейлиста. Дальше все данные будут подтягиваться по API
        """
        super().__init__(video_id)
        self.playlist_id = playlist_id
        self.playlist_videos = Video.youtube.playlistItems().list(playlistId=playlist_id,
                                                                    part='contentDetails',
                                                                    maxResults=50,
                                                                    ).execute()

