import time
from downloader import NhentaiDownloader

if __name__ == "__main__":
    manga_id = input("Input ID : ")
    process_count = int(input("Input process count : "))
    path = str(manga_id)
    start = time.time()
    NhentaiDownloader(manga_id, process_count, path=path)
    end = time.time()
    print("Total download time : " + str(end-start) + " s")
    input("press ENTER to exit")