from user import User
from settings2 import vk_token, yandex_token

open('errlog.log','w').close()

if __name__ == '__main__':
    user_id_or_nickname = input("Введите id/nickname: ")
    photos_count = 100
    user = User(user_id_or_nickname, vk_token, yandex_token)
    albums = user.get_profile_albums(user_id_or_nickname)
    print(f'У пользователя {user_id_or_nickname} доступны альбомы: ')
    for album in albums:
        print(f'Для выбора альбома "{albums[album][0]}" жми "{album}" в нем "{albums[album][2]}" фото')
    album = int(input('Какой выберем?   '))
    print(f' Вы выбрали {album}')
    album_id = albums[album][1]
    folober = (input('Сохраняем в папку с таким же именем? Y или N   '))
    if folober == 'y':
        backup_folder = albums[album][0]
    else:
        backup_folder = input("Введите название папки для резервного копирования на диске: ")
    count = (input('Скачиваем все фотографии? Y или N   '))
    if count == 'y':
        photos_count = albums[album][2]
    else:
        photos_count = int(input("Введите количество фотографии для резервного копирования: "))
    user.backup_profile_photos(photos_count, backup_folder, album_id)
