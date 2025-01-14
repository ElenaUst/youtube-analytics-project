from googleapiclient.discovery import build
import os
from pprint import pprint
import json

api_key: str = os.getenv('YT_API_KEY')


class Channel:
    """Класс для ютуб-канала"""
    youtube = build('youtube', 'v3', developerKey=api_key)

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.__channel_id = channel_id
        self.channel = Channel.youtube.channels().list(id=self.__channel_id, part='snippet,statistics').execute()
        self.title = self.channel.get('items')[0].get('snippet').get('title')
        self.description = self.channel.get('items')[0].get('snippet').get('description')
        self.url = "https://www.youtube.com/" + self.channel.get('items')[0].get('snippet').get('customUrl')
        self.subscriberCount = self.channel.get('items')[0].get('statistics').get('subscriberCount')
        self.video_count = self.channel.get('items')[0].get('statistics').get('videoCount')
        self.viewCount = self.channel.get('items')[0].get('statistics').get('viewCount')

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        channel = self.youtube.channels().list(id=self.__channel_id, part='snippet,statistics').execute()
        pprint(channel)

    @classmethod
    def get_service(cls):
        """
        Возвращает объект для работы с YouTube API
        """
        return cls.youtube

    def to_json(self, filename):
        """
        Сохраняет в файл значения атрибутов экземпляра `Channel`
        """
        data = self.__dict__
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    def __str__(self):
        """
        Возвращает название и ссылку на канал по шаблону `<название_канала> (<ссылка_на_канал>)`
        """
        return f'{self.title} ({self.url})'

    def __add__(self, other):
        if isinstance(other, Channel):
            return int(self.subscriberCount) + int(other.subscriberCount)
        else:
            raise TypeError

    def __sub__(self, other):
        if isinstance(other, Channel):
            return int(self.subscriberCount) - int(other.subscriberCount)
        else:
            raise TypeError

    def __gt__(self, other):
        if self.subscriberCount > other.subscriberCount:
            return True
        return False


    def __ge__(self, other):
        if self.subscriberCount >= other.subscriberCount:
            return True
        return False

    def __lt__(self, other):
        if self.subscriberCount < other.subscriberCount:
            return True
        return False

    def __le__(self, other):
        if self.subscriberCount <= other.subscriberCount:
            return True
        return False

    def __eq__(self, other):
        if self.subscriberCount == other.subscriberCount:
            return True
        return False
