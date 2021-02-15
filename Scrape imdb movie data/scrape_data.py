from bs4 import BeautifulSoup as BS
from urllib import request
import re
import pandas as pd
import json

def check_url(url):
    p = re.compile("https://www.imdb.com/")
    if p.match(url):
        return True
    return False

def get_html(url):
    try:
        page = request.urlopen(url)
        return page
    except:
        print("Error opening URL")
    
def get_parsed_data(html):
    try:
        soup = BS(html, 'html.parser')
        return soup
    except AttributeError:
        print("Error parsing html")

def scrape_data(soup):
    result_dict = {"Title": [], "Year": [], "Rating": [], "ImageLink": []}

    poster_column = soup.find_all('td', class_='posterColumn')
    title_column = soup.find_all('td', class_='titleColumn')
    rating = soup.find_all('td', class_='imdbRating')

    for i, j, k in zip(poster_column, title_column, rating):
        result_dict["ImageLink"].append(i.find("img")["src"])
        result_dict["Title"].append(j.find('a').string)
        result_dict["Year"].append(j.find('span', class_="secondaryInfo").string)
        rating = k.find('strong')
        if rating == None:
            result_dict["Rating"].append(None)
        else:
            result_dict["Rating"].append(rating.string)

    return result_dict

def input_file_name(result_dict):
    filename = input("Filename: ").split('.')
    if len(filename) > 2:
        print("Invalid filename. Include only single extension.\n")
        input_file_name(result_dict)
    elif len(filename) == 2:
        if filename[0] == "" or filename[1] == "":
            print("Invalid name. Enter again\n")
            input_file_name(result_dict)
        elif filename[1] != "json" and filename[1] != "csv":
            print("Invalid extension. Allowed only json and csv. Enter again.\n")
            input_file_name(result_dict)
        else:
            if filename == "json":
                filename = filename[0] + ".json"
                with open(filename, "w") as f:
                    json.dump(result_dict, f)
                    f.close()
            else:
                filename = filename[0] + ".csv"
                pd.DataFrame.from_dict(result_dict).to_csv(filename, index=False)
    else:
        filename = filename[0] + ".json"
        with open(filename, "w") as f:
            json.dump(result_dict, f)
            f.close()

def driver():
    url = input("Enter url: ")
    valid = check_url(url)
    if not valid:
        print("Enter valid url")
        exit()
    
    result_dict = scrape_data(get_parsed_data(get_html(url)))
    
    print("\n\nEnter the filename in which you want to save the file.\n(Default storage extension is json. Available storage types are JSON and CSV. To save as CSV write .csv as extension. To save as json write .json or don't write any . extension)\n")
    input_file_name(result_dict)



if __name__ == '__main__':
    driver()
    print("Done....Yup!!")