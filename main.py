import time
from downloader import NhentaiDownloader

if __name__ == "__main__":
    while True:
        try:
            manga_id = int(input("Input ID : "))
            break
        except:
            print("That's not a valid ID. Try again.")
            continue
    try:
        process_count = int(input("Input process count (default is 30) : "))
    except:
        process_count = 30
    path = str(manga_id)
    start = time.time()
    NhentaiDownloader(manga_id, process_count, path=path)
    end = time.time()
    print("Total download time : " + str(end-start) + " s")
    input("press ENTER to exit")
