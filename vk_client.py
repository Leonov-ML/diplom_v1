import requests
import time

class VkApi:
    def __init__(self, token, api_url, api_version):
        self.token = token
        self.api_url = api_url
        self.api_version = api_version
        self.params = {
            "access_token": self.token,
            "v": self.api_version
        }

    def get_user_id(self, user_id_or_nickname):
        id_url = self.api_url + "users.get"
        id_params = {"user_ids": user_id_or_nickname}
        repeat = True
        while repeat:
            res = requests.get(id_url, params={**self.params, **id_params})
            res.raise_for_status()
            data = res.json()
            if 'error' in data and 'error_code' in data['error'] and data['error']['error_code'] == 6:
                time.sleep(1)
            else:
                repeat = False
        return res.json()

    def get_albums(self, owner_id):
        album_url = self.api_url + "photos.getAlbums"
        album_params = {
            'owner_id': owner_id,
            'need_system': '1',
            'rev': '1'
        }
        res = requests.get(album_url, params={**self.params, **album_params})
        res.raise_for_status()
        return res.json()

    def get_photos(self, owner_id, album_id, count):
        photos_url = self.api_url + "photos.get"
        photos_params = {
            'owner_id': owner_id,
            'album_id': album_id,
            'extended': '1',
            'photo_sizes': '1',
            'count': count,
            'rev': '1'
        }
        repeat = True
        while repeat:
            res = requests.get(photos_url, params={**self.params, **photos_params})
            res.raise_for_status()
            data = res.json()
            if 'error' in data and 'error_code' in data['error'] and data['error']['error_code'] == 6:
                time.sleep(1)
            elif 'error' in data and 'error_code' in data['error'] and data['error']['error_code'] == 30:
                print('Это закрытый акаунт, ни чего не получится ¯\_(ツ)_/¯ ...!')
                exit()
            else:
                repeat = False

        return res.json()

    def get_likes(self, owner_id, item_id):
        likes_url = self.api_url + "likes.getList"
        likes_params = {
            "type": "photo",
            "owner_id": owner_id,
            "item_id": item_id,
            "album_id": 'profile',
        }
        repeat = True
        while repeat:
            res = requests.get(likes_url, params={**self.params, **likes_params})
            res.raise_for_status()
            data = res.json()
            if 'error' in data and 'error_code' in data['error'] and data['error']['error_code'] == 6:
                time.sleep(1)
            else:
                repeat = False

        return res.json()