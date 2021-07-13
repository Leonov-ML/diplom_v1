from user import User, albums_dict
from settings import vk_token, yandex_token

if __name__ == '__main__':
    user_id_or_nickname = input("Введите id/nickname: ")
    photos_count = 100
    user = User(user_id_or_nickname, vk_token, yandex_token)
    user.get_profile_albums(user_id_or_nickname)
    album = int(input('Какой выберем?   '))
    print(f' Вы выбрали {album}')
    album_id = albums_dict[album][1]
    folober = (input('Сохраняем в папку с таким же именем? Y или N   '))
    if folober == 'y':
        backup_folder = albums_dict[album][0]
    else:
        backup_folder = input("Введите название папки для резервного копирования на диске: ")
    count = (input('Скачиваем все фотографии? Y или N   '))
    if count == 'y':
        photos_count = albums_dict[album][2]
    else:
        photos_count = int(input("Введите количество фотографии для резервного копирования: "))
    user.backup_profile_photos(photos_count, backup_folder, album_id)
