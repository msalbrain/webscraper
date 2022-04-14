import requests
from bs4 import BeautifulSoup
from typing import List

from datetime import datetime
import ast
import time

schema = {"data": [],
          "updated_last": {
              "last_query": 0.0,

          }}

month_to_num = {
    "january": '1',
    "february": '2',
    "march": '3',
    "april": '4',
    "may": '5',
    "june": '6',
    "july": '7',
    "august": '8',
    "september": '9',
    "october": '10',
    "november": '11',
    "december": '12'
}


def convd(t):
    return datetime(t[0], t[1], t[2], t[3], t[4]).timestamp()


def read_db():
    # Opening JSON file
    json_file = open('data.db', "r")
    db_data = json_file.read()
    json_file.close()
    if db_data.strip() == '':
        print("hello with the strip")
        return schema

    data = ast.literal_eval(db_data)
    return data


def write_db(d):
    with open('data.db', "w") as json_file:
        data = json_file.write(str(d))

def unix_time():
    dtime = datetime.now()
    unix_time = time.mktime(dtime.timetuple())
    return float(unix_time)


def convert_date_str_tuple(date_str: str):
    date_list = date_str.split()
    month_ = date_list[0]
    day_ = date_list[1][0:-1]
    year_ = date_list[2]

    return convd((int(year_), int(month_to_num.get(month_.casefold())), int(day_), 0 , 0))


def run():
    _class = "col-sm-6 col-xxl-4 post-col"
    read = read_db()
    read_data = read.get("data")
    url = "https://animesenpai.net"
    with requests.get(url) as f:
        soup = BeautifulSoup(f.content, 'html.parser')

        list_of_cards = soup.find_all(class_=_class)
        first_date = convert_date_str_tuple(list_of_cards[0].find(class_="date").get_text())
        lala = []
        for i in list_of_cards:

            print("\n")

            url_date = i.find(class_="date").get_text()
            print(url_date)
            if first_date == convert_date_str_tuple(url_date):

                title = i.a["title"]
                print(title)

                url_image = i.a["style"].split()[1].replace("url('", "").replace("');", "")
                print(url_image)

                sht = {
                    "title": title,
                    "date": url_date,
                    "img": url_image
                }
                print(sht)
                lala.append(sht)
            elif first_date > convert_date_str_tuple(url_date):
                read.update({"data": lala,"updated_last": {
                    "last_query": unix_time()
                    }})
                print(read)
                write_db(read)
                break




def entry() -> List[dict]:
    content = []
    most_recent = read_db().get("updated_last")["last_query"]

    diff = unix_time() - most_recent
    if diff < 3600:
        for i in read_db().get("data"):

            content.append(i)

        return content

    else:
        print("i broke out")
        run()
        return entry()

if __name__ == '__main__':
    print(entry())
