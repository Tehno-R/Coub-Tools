import json
from bs4 import BeautifulSoup
import requests
from random_header_generator import HeaderGenerator


def get_page(url, header=None ,safe_in_file=None, source=False):
    if header is None:
        header_generator = HeaderGenerator()
        header = header_generator()
        # print(header)

    try:
        res = requests.get(url=url, headers=header)
    except requests.RequestException:
        print("Connection Error")
        return None
    if res.status_code == 200:
        if safe_in_file:
            try:
                with open(f"{safe_in_file}", 'w') as f:
                    f.write(res.text)
            except Exception as e:
                print("Error write in file")
        if source:
            return res.text
        else:
            soup = BeautifulSoup(res.text, "html.parser")
            return soup
    else:
        print(f"Status code: {res.status_code}")
        return None


def get_all_coub_info(permalink):
    LINK = f"https://coub.com/api/v2/timeline/channel/{permalink}?order_by=newest&permalink={permalink}&type=simples&page=1"
    coubs_info = get_page(LINK, source=True)
    if coubs_info is None:
        print("Error getting coubs info")
        return None
    pages = []
    coubs_info_dict = json.loads(coubs_info)
    if coubs_info_dict["total_pages"] != 0:
        pages.append(coubs_info_dict)
        for page in range(1, coubs_info_dict["total_pages"] + 1):
            pages.append(get_page(LINK[:-1] + str(page)))

    if pages:
        return pages
    return coubs_info_dict


def format_coubs_info(coubs_info):
    # idea: make class Coub
    # to do: to sort keys and each writes
    keys = ["id", "permalink", "title", "channel_id", "published_at", "featured", "views_count", "picture", "tags",
            "categories", "music", "recoubs_count", "likes_count", "comments_count", "duration", "file_versions/html5/video/high"]
    if coubs_info is list:
        for coub in coubs_info:
            pass


if __name__ == "__main__":
    # t10enshi
    # .t10nshi
    page = get_all_coub_info("t10enshi")
    if page is None:
        exit("Get page error")
    # json.dump(page[0], open("example.json", "w"))