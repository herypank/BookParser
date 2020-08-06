import os
import requests
from pathlib import Path
from bs4 import BeautifulSoup
from pathvalidate import sanitize_filename
from urllib.parse import urljoin
import json

def parsing_text(id,url_book):

def parsing_text(id):
    """Функция для парсинга названия книг с сайта http://tululu.org.

    Args:
        url_book (str): Cсылка на книгу которую парсим.
        parse_book (list): (0)Название книги, (1)Автор.

    Returns:
        str: Путь до файла, куда сохранён текст.
    """
    url_book = f'http://tululu.org/b{id}/'
    response = requests.get(url_book)
    soup = BeautifulSoup(response.text, 'lxml')
    header = soup.select_one("#content")
    title_tag = header.h1
    parse_book = (title_tag).text.split(' \xa0 :: \xa0 ')
    author,title = parse_book

    return author + ' -- ' +  title

def parsing_comments(id):
    """Функция для парсинга комментариев книг с сайта http://tululu.org.

    Args:
        url_book (str): Cсылка на книгу которую парсим.
        parse_book (list): (0)Название книги, (1)Автор.

    Returns:
        str: Путь до файла, куда сохранён текст.
    """
    url_book = f'http://tululu.org/b{id}/'
    response = requests.get(url_book)
    soup = BeautifulSoup(response.text, 'lxml')
    title_tag = soup.select(".texts[style='margin:0;padding:0 10px;'] > .black")
    comments = []
    for comment in title_tag:
        comments.append(comment.text)
    return comments

def parsing_genres(id):
    """Функция для парсинга комментариев книг с сайта http://tululu.org.

    Args:
        url_book (str): Cсылка на книгу которую парсим.
        parse_book (list): (0)Название книги, (1)Автор.

    Returns:
        str: Путь до файла, куда сохранён текст.
    """
    url_book = f'http://tululu.org/b{id}/'
    response = requests.get(url_book)
    soup = BeautifulSoup(response.text, 'lxml')
    genres_p = soup.find('span', class_ = 'd_book').find_all('a')
    genres = []
    for genre in genres_p:
        genres.append(genre.text)
    return genres



def parsing_image(id):
    """Функция для парсинга картинок книг с сайта http://tululu.org.

    Args:
        url_book (str): Cсылка на книгу которую парсим.
        parse_book (list): (0)Название книги, (1)Автор.

    Returns:
        str: Путь до файла, куда сохранён текст.
    """
    url_book = f'http://tululu.org/b{id}/'
    response = requests.get(url_book)
    soup = BeautifulSoup(response.text, 'lxml')
    img_src = soup.find('div', class_ = 'bookimage').find('img')['src']
    return urljoin('http://tululu.org', img_src)

def download_img(PATCH_IMG,url_img):

    response = requests.get(url_img, allow_redirects=False)
    filename = f"{url_img.split('/')[-1]}"
    folder = os.path.join(PATCH_IMG, filename)
    with open(folder, "wb") as file:
        return file.write(response.content)

def download_book(url_book,id):    
    id_download = url_book[url_book.find('/b')+2:-1] #так как для закачки книги ссылка совсем другая нужен id
    url_download = f'http://tululu.org/txt.php?id={id_download}'
    response = requests.get(url_download, allow_redirects=False)
    filename = f"{id+1}-я книга. {parsing_text(id_download,url_book)}.txt"
    folder = os.path.join(PATCH_BOOKS, filename)
    with open(folder, "w", encoding='utf-8') as file:
        return file.write(response.text)

if __name__ == '__main__':
    PATCH_BOOKS = r"C:\Users\lysak.m\Documents\py\study_prog\Many_projects\BookParser\books"
    Path(PATCH_BOOKS).mkdir(parents=True, exist_ok=True)
    PATCH_IMG = r"C:\Users\lysak.m\Documents\py\study_prog\Many_projects\BookParser\images"
    Path(PATCH_IMG).mkdir(parents=True, exist_ok=True)
    urls = parsing_url()
    list = []
    for id in range(10):
        url_book = urls[id]
        url_img = parsing_image(id,url_book)
        book_info = parsing_text(id,url_book).split(' -- ')
        comments = parsing_comments(id,url_book)
        genres = parsing_genres(id,url_book)
        url_src = os.path.join('images',url_img.split('/')[-1])
        book_path = os.path.join('books',book_info[0] + '.txt')
        fantosy_book = {
            'title':book_info[0],
            "author": book_info[1],
            'img_src':url_src,
            'book_path':book_path,
            'comments':comments,
            "genres": genres
        }
        list.append(fantosy_book)
        download_img(PATCH_IMG,url_img)
        download_book(url_book,id)
    with open("capitals.json", "a", encoding='utf-8') as my_file:
        json.dump(list,my_file, indent=4 ,ensure_ascii=False)

