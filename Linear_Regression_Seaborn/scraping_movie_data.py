# we want to scrape the data from the-numbers; getting the budget, rank, name and gross of every movie in their db

from bs4 import BeautifulSoup
import requests
import pandas as pd


# problem: difficult to distinguish between Rank, Release date, etc, since all have the class 'data'
# solution: loop through the the extracted list in steps of 6 since the data is always in the same order
def extract_data():
    # function useful because multiple pages exist on website
    for elements in range(0, len(data), 6):
        movie_data.append({'Rank': data[0 + elements].text,
                           'Release Date': data[1 + elements].text,
                           'Movie': data[2 + elements].text.replace(u'â\x80\x99', u"'").replace(u'â\x80\x94', u' - '), # not beautiful but ok
                           'Production Budget': data[3 + elements].text.replace(u'\xa0$', u''),
                           'Domestic Gross': data[4 + elements].text.replace(u'\xa0$', u''),
                           'Worldwide Gross': data[5 + elements].text.replace(u'\xa0$', u'')
                           })
    return movie_data


movie_data = []

# first page as tryout + different URL layout
response = requests.get('http://www.the-numbers.com/movie/budgets/all').text
soup = BeautifulSoup(response, 'html.parser')

# all entries have 'td'
data = soup.find_all(name='td')

extract_data()
print(movie_data)

# now we loop through all pages; the url starts with 101 and goes until 6101
for pages in range(1, 62):
    response = requests.get(f'http://www.the-numbers.com/movie/budgets/all/{pages}01').text
    soup = BeautifulSoup(response, 'html.parser')
    data = soup.find_all(name='td')
    extract_data()

print(movie_data)

# now we convert our list of dicts into a pandas dataframe and export the data as a csv
df_movies = pd.DataFrame(movie_data)
df_movies.to_csv('movie_data.csv', index=False)