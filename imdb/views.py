from django.shortcuts import render
from requests import get
from bs4 import BeautifulSoup


def imdb_parser(request):
    # url of current Week premiere
    url = 'http://www.imdb.com/movies-in-theaters/'

    response = get(url)

    html_soup = BeautifulSoup(response.text, 'html.parser')
    # Get HTML block with film list and parse it
    movie_containers = html_soup.find_all('div', class_='list_item')
    # Create list of all movies for fill it later
    movie_list = []
    # ===========Test part============
    # first_movie = movie_containers[0]
    # stars_li = '|'.join(map(str, [stars.text for stars in first_movie.select('span[itemprop="name"]')]))
    # print(stars_li)
    # Get list of all films on parsed page
    # f = first_movie.find('span', class_='metascore favorable')
    # print(f)
    # ========== End test ===========
    for movie in movie_containers:
        # Check rating. Because Without check get an error NoneType object have not text attr
        rating = movie.find('span', class_='metascore')
        # rating = movie.find_next('div', class_='rating_txt')

        h5_stars = movie.find_all('h5')
        print([i.text for i in h5_stars[1].find_next_siblings('a')])

        if rating is not None:
            rating = rating.text
        else:
            rating = 'Does not rated yet'
        movie_list.append({
            'title': movie.h4.a['title'],
            'description': movie.find('div', class_='outline').string,
            'image': movie.img['src'],
            'director': movie.h5.find_next('a').text,
            # Get stars list and clear from tags and \n, convert list to string
            # ','.join(map(str, [stars.text.strip('\n') for stars in movie.h5.find_next('a').text])),
            'stars': ', '.join([i.text for i in h5_stars[1].find_next_siblings('a')]),
            # get rating
            'rating': rating,
            # Get rating list, clear from tags and \n, convert list to string
            'genre': '| '.join(map(str, [genre.text.strip('\n') for genre in movie.select('span[itemprop="genre"]')])),
            'trailer': movie.find('a', {'itemprop': "trailer"})['href']

          }
        )
    print(movie_list[0]['trailer'])
    return render(request, 'imdb/index.html', {'movie_list': movie_list})
