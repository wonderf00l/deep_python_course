import sys
import getopt
from time import time
from collections import Counter
import asyncio
import aiohttp
from bs4 import BeautifulSoup


async def url_process(session, queue, sem, k_words, result):
    while True:
        url = await queue.get()
        print(f"{asyncio.current_task} got {url}")
        print("qsize: ", queue.qsize())
        async with sem:
            try:
                async with session.get(url) as resp:
                    data = await resp.text()
                    assert resp.status == 200
                    soup = BeautifulSoup(data, "html.parser")
                    lst_ = soup.text.replace('\n', '').split(' ')
                    lst_of_words = [word for word in lst_ if len(word) > 1]
                    words_rate = {url: dict(Counter(lst_of_words).most_common(k_words))}
                    result.append(words_rate)
            except ConnectionError as error:
                print(f"{url}: got {error}")
            except AssertionError:
                print(f"{url}: invalid response")
            except aiohttp.InvalidURL:
                print(f"{url}: got invalid URL")
            finally:
                queue.task_done()

async def main(urls=None, workers=5, k_words=5, queries=1, *, test=None):
    if test == "valid":
        urls = ["https://www.python.org/"]
    elif test == "invalid":
        urls = ["invalid test case"]
    result = []
    queue = asyncio.Queue()
    try:
        opts = getopt.getopt(sys.argv[1:], "c:")[0]
        for opt, arg in opts:
            if opt in ["-c"]:
                queries = int(arg)
    except (ValueError, IndexError, getopt.GetoptError) as error:
        print(error)
        while True:
            try:
                print("Input correct num of queries")
                queries = int(input("queries: "))
                break
            except ValueError:
                continue
    sem = asyncio.Semaphore(queries)
    for url in urls:
        await queue.put(url)
    print(f"initial qsize: {queue.qsize()}")
    async with aiohttp.ClientSession() as session:
        workers = [
            asyncio.create_task(url_process(session, queue, sem, k_words, result))
            for _ in range(workers)
        ]
        print("tasks have been created")
        await queue.join()
        for worker in workers:
            worker.cancel()
        print(result)
        return result
 

if __name__ == "__main__":
    URLs_lst = []
    with open("URL.txt", 'r', encoding="utf-8") as file:
        lst = file.readlines()
        URLs_lst.extend([lst[0]] * 5)
        for item in lst[1:]:
            URLs_lst.append(item[:-1])
    start = time()
    asyncio.run(main(URLs_lst, test="valid"))
    print(f"It took {time() - start} sec")
