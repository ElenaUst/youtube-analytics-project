from src.channel import api_key
from googleapiclient.discovery import build
import datetime
from src.video import Video
import isodate


class PlayList:
    """
    инициализируется _id_ плейлиста и имеет следующие публичные атрибуты:
  - название плейлиста
  - ссылку на плейлист
    """
    youtube = build('youtube', 'v3', developerKey=api_key)

    def __init__(self, playlist_id: str) -> None:
        self.playlist_id = playlist_id
        self.playlist_videos = PlayList.youtube.playlistItems().list(playlistId=self.playlist_id,
                                                                     part='contentDetails, snippet',
                                                                     maxResults=50,
                                                                     ).execute()
        self.title: str = self.playlist_videos['items'][0]['snippet']['title'].split('.')[0].strip()
        self.url = "https://www.youtube.com/playlist?list=" + self.playlist_videos.get('items')[0].get('snippet').get(
            'playlistId')

    @property
    def total_duration(self):
        """
        Возвращает объект класса `datetime.timedelta` с суммарной длительностью плейлиста (обращение как к свойству,
        использовать `@property`)
        """
        dur = datetime.timedelta()
        for video in self.playlist_videos['items']:
            video_id = video['contentDetails']['videoId']
            tmp_video = Video(video_id)
            iso_8601_duration = tmp_video.video_response['items'][0]['contentDetails']['duration']
            duration = isodate.parse_duration(iso_8601_duration)
            dur += duration
        return dur

    def show_best_video(self):
        """
        Возвращает ссылку на самое популярное видео из плейлиста (по количеству лайков)
        """
        max_likes = 0
        best_video = ''
        for video in self.playlist_videos['items']:
            video_id = video['contentDetails']['videoId']
            tmp_video = Video(video_id)
            if int(tmp_video.like_count) > max_likes:
                max_likes = int(tmp_video.like_count)
                best_video = "https://youtu.be/" + tmp_video.video_id
        return best_video
