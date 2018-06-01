import requests
from bs4 import BeautifulSoup
import codecs
URL = 'https://movie.douban.com/top250'

def download_page(url):
    data = requests.get(url)
    data.encoding = 'uft-8'
    return data.text

def parse_html(html):
    soup = BeautifulSoup(html, 'html.parser')
    movie_list_soup = soup.find('ol', attrs={'class': 'grid_view'})
    movie_name_list = []
    movie_html_list = []
    count = 0
    for movie_li in movie_list_soup.find_all('li'):
        detail = movie_li.find('div', attrs={'class': 'hd'})
        movie_name = detail.find('span', attrs={'class': 'title'}).getText()
        movie_html = detail.find('a')['href']
        movie_name_list.append(movie_name)
        movie_html_list.append(movie_html)
        # print(movie_name)
        # print(movie_html)
    next_page = soup.find('span', attrs={'class': 'next'}).find('a')
    if next_page:
        return movie_name_list, movie_html_list, URL+next_page['href']
    return movie_name_list, movie_html_list, None

def main():
    url = URL
    with codecs.open('movies.txt', 'wb', encoding='utf-8') as fp:
        while url:
            html = download_page(url)
            movies, movies_html, url = parse_html(html)
            for i in zip(movies, movies_html):
                fp.write(u'{movies}\n'.format(movies='\n'.join(i)))


if __name__ == '__main__':
    main()

