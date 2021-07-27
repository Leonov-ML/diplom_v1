import json
from vk_client import VkApi
from yandex_client import YandexApi
from photo import Photo
from tqdm import tqdm

YANDEX_API_URL = "https://cloud-api.yandex.net/"
YANDEX_API_VERSION = "v1"

VK_API_URL = "https://api.vk.com/method/"
VK_API_VERSION = "5.131"

albums_dict = {}


class User:
    def __init__(self, user_id_or_nickname, vk_token, yandex_token):
        self.vk_client = VkApi(vk_token, VK_API_URL, VK_API_VERSION)
        self.yandex_client = YandexApi(yandex_token, YANDEX_API_URL, YANDEX_API_VERSION)
        self.user_id = self.get_user_id(user_id_or_nickname)

    def get_user_id(self, user_id_or_nickname):
        response = self.vk_client.get_user_id(user_id_or_nickname)["response"]
        return int(response[0]["id"])

    def get_profile_albums(self, user_id_or_nickname):
        response = self.vk_client.get_albums(self.user_id)["response"]
        items = response["items"]

        for i in range(len(items)):
            albums_dict[i] = [items[i]['title'], items[i]['id'], items[i]['size']]

        return albums_dict

    def backup_profile_photos(self, count=5, backup_folder="user_photos", album_id="album_id"):
        photos = self.get_profile_photos(count, album_id)
        self.upload_photos_yandex(photos, backup_folder)
        self.save_photos_to_json("output.json", photos)


    def get_profile_photos(self, count, album_id):
        response = self.vk_client.get_photos(self.user_id, album_id, count, )["response"]
        items = response["items"]
        photos = []
        likes_dict = {}
        for item in tqdm(items, desc='Идет скачивание файлов', leave=False):
            photo_id = item["id"]
            likes = self.get_photo_likes(photo_id)
            url = item["sizes"][-1]["url"]
            photo_type = item["sizes"][-1]["type"]
            date = item["date"]
            photo = Photo(photo_id, url, likes, photo_type, date)
            photos.append(photo)
            if likes not in likes_dict:
                likes_dict[likes] = []
            likes_dict[likes].append(photo)
        for likes, like_photos in likes_dict.items():
            if len(like_photos) > 1:
                for like_photo in like_photos:
                    like_photo.use_date_in_file_name = True

        return photos

    def get_photo_likes(self, item_id):
        response = self.vk_client.get_likes(self.user_id, item_id)["response"]

        return response["count"]

    def upload_photos_yandex(self, photos, backup_folder):
        list_upload = []
        status = []
        print("Создаю папку {} в Yandex Disk".format(backup_folder))
        self.yandex_client.create_folder(backup_folder)
        for photo in tqdm(photos, desc='Идет загрузка файлов', leave=False):
            path = backup_folder + "/" + photo.get_file_name()
            url = photo.url
            data = self.yandex_client.upload(path, url)
            list_upload.append(data["href"])
        for url in tqdm(list_upload, desc='Идет проверка загрузки', leave=False):
            err = self.yandex_client.check_upload(url)
            status.append(err["status"])
        if 'failed' in status:
            print('Возможно что то пошло не так, проверьте введенные данные.')
        elif 'in-progress' in status:
            print('Есть небольшие предупреждения, стоит убедитьсячто все хорошо.')
        else:
            print(f'Все фотографии успешно загружены! =)')

    def save_photos_to_json(self, file_name, photos):
        print("Сохраняю отчет в {}".format(file_name))
        output = []
        for photo in photos:
            output.append(photo.to_dict())
        with open(file_name, "w") as f:
            json.dump(output, f)

