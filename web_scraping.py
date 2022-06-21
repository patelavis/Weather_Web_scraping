# Import libraries
import pandas as pd
from bs4 import BeautifulSoup
import requests
import os
# Save all website as .html file formate in local folder 
def retrive_html(from_year, to_year):
    for year in range(from_year, to_year+1):
        for month in range(1, 13):
            if month<10:
                url = f'https://en.tutiempo.net/climate/0{month}-{year}/ws-421820.html'
            else:
                url = f'https://en.tutiempo.net/climate/{month}-{year}/ws-421820.html'
            texts = requests.get(url).text
            if not os.path.exists(f'Data/html_data/{year}'):
                os.makedirs(f'Data/html_data/{year}')
                
            with open(f'Data/html_data/{year}/{month}.html', 'w') as f:
                f.write(texts)
# Run above fuction
retrive_html(2013, 2019)
# to get tabular data from website
temp_data = []
for year in range(2013, 2020):
    for month in range(1, 13):
        with open(f'Data/html_data/{year}/{month}.html', 'r') as f:
            data = f.read()
        soup = BeautifulSoup(data)
        table_data = soup.find('table', {'class':'medias mensuales numspan'})
        
        for row in table_data.find_all('tr')[1:]:
            temp_data.append([x.text for x in row.find_all('td')])
# save in dataframe formate and output as a .csv file
df = pd.DataFrame(temp_data)
df.to_csv('weather_data_2013-2019.csv', index=False)
