from pathlib import Path
import requests
from multiprocessing.pool import ThreadPool
from bs4 import BeautifulSoup


class NhentaiDownloader():
    def __init__(self, manga_id: int, process_count=30, path="/") -> None:
        Path(path).mkdir(parents=True, exist_ok=True)
        self.getinfo = self.GetInfo(manga_id)
        self.isrecaptcha = self.getinfo.isrecaptcha
        self.images_urls = self.getinfo.get_all_urls()
        self.pages = self.getinfo.pages
        self.paths = [path for _ in range(self.pages)]
        self.DownloadProcess(process_count, self.images_urls, self.paths)

    class DownloadProcess():
        def __init__(self, process_count: int, images_urls: list, paths: list):
            results = ThreadPool(process_count).imap(
                self.image_downloader, zip(images_urls, paths))
            for r in results:
                print(r,end='')

        def image_downloader(self, download_info: tuple):
            image_url = download_info[0]
            path = download_info[1]
            # print(image_url,path)
            print(f"Downloading: {image_url}\n", end="")
            res = requests.get(image_url, stream=True)
            count = 1
            while res.status_code != 200 and count <= 5:
                res = requests.get(image_url, stream=True)
                print(f"Retry: {count} {image_url}\n", end="")
                count += 1
            if "image" not in res.headers.get("content-type", ""):
                print("ERROR: URL doesnot appear to be an image\n", end="\n")
                return False
            try:
                image_name = str(image_url[(image_url.rfind("/")) + 1:])
                if "?" in image_name:
                    image_name = image_name[:image_name.find("?")]
            except:
                image_name = "0.jpg"
            with open(Path(path, image_name), "wb") as f:
                for chunk in res.iter_content(chunk_size=8192):
                    f.write(chunk)
            return f"Download complete: {image_url}\n"

    class GetInfo():
        def __init__(self, manga_id: int) -> None:
            self.web_content = self.get_content(manga_id)
            self.isrecaptcha = self.check_isrecaptcha(self.web_content)
            self.media_id = self.get_media_id(self.web_content)
            self.pages = self.get_pages(self.web_content)
            self.data_type = self.get_data_type(self.web_content)

        def check_isrecaptcha(self, web_content: BeautifulSoup):
            if "recaptcha" in str(web_content):
                print("Fetch failed")
                exit()

        def get_media_id(self, web_content: BeautifulSoup):
            media_id = int(str(web_content.find_all("meta")[3]).split("/")[4])
            print(f"Media_id : {media_id}")
            return media_id

        def get_pages(self, web_content: BeautifulSoup):
            pages = int(web_content.find_all("section")[
                        1].find_all("div")[-2].find_all("span")[1].text)
            print(f"Pages : {pages}")
            return pages

        def get_content(self, manga_id: int):
            res = requests.get(
                f"https://translate.google.com/translate?sl=zh-TW&tl=en&hl=zh-TW&u=nhentai.net/g/{manga_id}")
            return BeautifulSoup(res.text, "html.parser")

        def get_data_type(self, web_content: BeautifulSoup):
            data_type = str(web_content.find_all("meta")[
                            3]).split("/")[5].split(".")[1].split("\"")[0]
            return data_type

        def get_all_urls(self):
            return [f"https://translate.google.com/translate?sl=zh-TW&tl=en&hl=zh-TW&u=i3.nhentai.net/galleries/{self.media_id}/{i+1}.{self.data_type}" for i in range(self.pages)]
