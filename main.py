import requests
import time
from multiprocessing.pool import ThreadPool
from bs4 import BeautifulSoup


def image_downloader(img_url: str):
    print(f"Downloading: {img_url}")
    res = requests.get(img_url, stream=True, headers=headers)
    count = 1
    while res.status_code != 200 and count <= 5:
        res = requests.get(img_url, stream=True, headers=headers)
        print(f"Retry: {count} {img_url}")
        count += 1
    if "image" not in res.headers.get("content-type", ""):
        print("ERROR: URL doesnot appear to be an image")
        return False
    try:
        image_name = str(img_url[(img_url.rfind("/")) + 1:])
        if "?" in image_name:
            image_name = image_name[:image_name.find("?")]
    except:
        image_name = "0.jpg"

    f = open(image_name, "wb")
    for chunk in res.iter_content(chunk_size=512*1024):
        if chunk:
            f.write(chunk)
    f.close()
    return f"Download complete: {img_url}"


def run_downloader(process: int, images_url: list):
    print(f"MESSAGE: Running {process} process")
    results = ThreadPool(process).imap(
        image_downloader, images_url)
    for r in results:
        print(r)


def get_media_id(web_content: BeautifulSoup):
    media_id = int(str(web_content.find_all("meta")[3]).split("/")[4])
    print(f"Media_id : {media_id}")
    return media_id


def get_pages(web_content: BeautifulSoup):
    pages = int(web_content.find_all("section")[
                1].find_all("div")[-2].find_all("span")[1].text)
    print(f"Pages : {pages}")
    return pages


def get_content(manga_id: int):
    res = requests.get(
        f"https://translate.google.com/translate?sl=zh-TW&tl=en&hl=zh-TW&u=nhentai.net/g/{manga_id}", headers=headers)
    return BeautifulSoup(res.text, "html.parser")


def get_data_type(manga_id: int):
    data_type = str(web_content.find_all("meta")[
                    3]).split("/")[5].split(".")[1].split("\"")[0]
    return data_type


def get_all_urls(media_id: int, pages: int, data_type: str):
    return [f"https://translate.google.com/translate?sl=zh-TW&tl=en&hl=zh-TW&u=i3.nhentai.net/galleries/{media_id}/{i+1}.{data_type}" for i in range(pages)]


if __name__ == "__main__":
    manga_id = input("Input ID : ")
    process_count = int(input("Input process count : "))

    start = time.time()
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36"}
    web_content = get_content(manga_id)
    if "recaptcha" in str(web_content):
        print("Fetch failed")
        exit()
    media_id = get_media_id(web_content)
    pages = get_pages(web_content)
    data_type = get_data_type(web_content)
    urls = get_all_urls(media_id, pages, data_type)
    run_downloader(process_count, urls)
    end = time.time()
    print("Total download time : " + str(end-start) + " s")
# update comment 2
# add comment 1
