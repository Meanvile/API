import sys
import csv
import requests

token = 'fd0a0c21fd0a0c21fd0a0c21c4fd7841cdffd0afd0a0c21a3d87c7425055109b33d4954'
ref = "https://api.vk.com/method/friends.get"
type_id = 'user_id'
version = 5.107
coding = 'utf-8'
id = 0
action = ""


def get_all_info(id, ref, type_id):
    response = requests.get(ref, params={'access_token': token, 'v': version,
                                         type_id: id,
                                         'fields': 'domain'})
    data = response.json()
    return data


def data2list(data, coding='utf-8'):
    if action == "albums":
        albums_list = [f"{album['title']}" for album in
                       data['response']['items']]
        with open(f'albums_of_{id}.csv', 'w', encoding=coding) as file:
            a_pen = csv.writer(file)
            a_pen.writerow(f'Альбомы id {id}')
            for i in albums_list:
                a_pen.writerow(i)
        print(f'Записан файл с альбомами: albums_{id}.csv!')
    elif action == "friends":
        friend_list = [f"{friend['first_name']} {friend['last_name']}" for
                       friend in data['response']['items']]
        with open(f'friends_of_{id}.csv', 'w', encoding=coding) as file:
            a_pen = csv.writer(file)
            a_pen.writerow(('First name', 'Last name'))
            count_of_deleted = 0
            for friend in friend_list:
                fr = friend.split()
                if fr[0] != 'DELETED':
                    a_pen.writerow((fr[0], fr[1]))
                else:
                    count_of_deleted += 1
            a_pen.writerow((f'Всего друзей: {len(friend_list)}',
                            f'Друзей, удаливших страницу: {count_of_deleted}'))
        print(f'Записан файл с друзьями: friends_{id}.csv!')


if __name__ == '__main__':
    if len(sys.argv) == 2:
        if isinstance(sys.argv[-1], int):
            action = sys.argv[-1]
        else:
            id = sys.argv[-1]
    if len(sys.argv) == 3:
        action = sys.argv[-2]
        id = sys.argv[-1]
    if not action:
        action = input("Введите то, список чего желаете получить(albums или "
                       "friends): ")
    if not id:
        id = int(input("Введите id пользователя (число): "))
    if action == "albums":
        ref = "https://api.vk.com/method/photos.getAlbums"
        type_id = 'owner_id'

    data = get_all_info(id, ref, type_id)
    data2list(data)
