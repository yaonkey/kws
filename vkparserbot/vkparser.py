#!usr/bin/env python3
import json
import sqlite3 as sql3

JSON_FILENAME = "../wall2.json"


class Image:
    src: str

    def __init__(self, src: str):
        self.src = src


class Post:
    text: str
    images: [Image]

    def __init__(self, text: str, images: [Image]):
        self.text = text
        self.images = images

    def get_images(self) -> [Image]:
        return self.images


def read_data(filename: str) -> str:
    data: str
    with open(filename) as json_file:
        data = json.load(json_file)
        return data['response']['items']


def get_count(filename: str) -> int:
    data: str
    with open(filename) as json_file:
        data = json.load(json_file)
        return int(data['response']['count'])


def parse_data(data: str) -> Post:
    images: [Image] = []

    text = data['text']
    imgs = data['attachments']
    for image in imgs:
        img_src = ''
        _image = ''
        if 'market_album' in image.keys():
            _image = image['market_album']['photo']['sizes'][-1]['url']
        elif 'photo' in image.keys():
            _image = image['photo']['sizes'][-1]['url']
        else:
            continue
        if '/impg' in _image:
            img_src = ''.join(_image.split('/impg'))
        if '/impf' in _image:
            img_src = ''.join(_image.split('/impf'))
        if '?' in img_src:
            img_src = Image(img_src.split('?')[0])
        else:
            img_src = Image(img_src)
        images.append(img_src)

    return Post(text, images)


def main():
    conn = sql3.connect("../kws.db")
    cursor = conn.cursor()
    for i in range(0, get_count(JSON_FILENAME)):
        post = parse_data(read_data(JSON_FILENAME)[i])
        print(f"{post.text} - {[image.src for image in post.images]}")
        _images = []
        for image in post.images:
            cursor.execute(f'INSERT INTO images (img_src) VALUES ("{image.src}");')
            conn.commit()
            res = cursor.execute(f'SELECT id FROM images WHERE img_src="{image.src}";')
            _images.append(str(int(res.fetchone()[0])))
        image_ids = ','.join(_images)
        post.text = post.text.replace('"', "'")
        cursor.execute(f'INSERT INTO posts (content, image_ids) VALUES ("{post.text}", "{image_ids}");')
        conn.commit()
    cursor.close()


def fix_db():
    conn = sql3.connect("../kws.db")
    cursor = conn.cursor()
    counter = 259
    while counter != 0:
        try:
            query = f"SELECT content, image_ids FROM posts WHERE id={counter}"
            res = cursor.execute(query).fetchone()
            query1 = f'INSERT INTO vk_posts (content, image_ids) VALUES ("{res[0]}", "{res[1]}")'
            cursor.execute(query1)
            conn.commit()
        except Exception as e:
            print(e)
            continue
        finally:
            counter -= 1
    conn.close()


if __name__ == '__main__':
    main()
