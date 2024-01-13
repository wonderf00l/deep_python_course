import sys
import os
import getopt
from time import time
from collections import Counter
import asyncio
import aiohttp
from bs4 import BeautifulSoup


async def url_process(session, gen, sem, k_words, result):
    while True:
        try:
            url = next(gen)[:-1]
        except StopIteration:
            print(f"{asyncio.current_task} status: no urls to process anymore")
            return result
        print(f"{asyncio.current_task} got {url}")
        async with sem:
            try:
                async with session.get(url) as resp:
                    data = await resp.text()
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
                continue

def file_process(file_obj):
    for string in file_obj:
        yield string

async def main(filename=sys.argv[-1], *, workers=9, k_words=5, queries=1):
    while True:
        if isinstance(filename, str) and os.path.basename(__file__) not in filename:
            try:
                urls = open(filename, "r", encoding="utf-8")
            except FileNotFoundError:
                while True:
                    try:
                        urls = open(input("Input valid filename: "), "r", encoding="utf-8")
                        break
                    except FileNotFoundError:
                        continue
            break
        try:
            urls = open(input("Input filename: "), "r", encoding="utf-8")
            break
        except FileNotFoundError:
            continue
    if len(sys.argv) > 1:
        if isinstance(sys.argv[1], int):
            queries = sys.argv[1]
        else:
            try:
                opts = getopt.getopt(sys.argv[1:], "c:")[0]
                for opt, arg in opts:
                    if opt in ["-c"]:
                        queries = int(arg)
            except (ValueError, IndexError, getopt.GetoptError) as error:
                print(error)
                while True:
                    try:
                        queries = int(input("Input correct num of queries: "))
                        break
                    except ValueError:
                        continue
    else:
        while True:
            try:
                queries = int(input("Input correct num of queries: "))
                break
            except ValueError:
                continue
    result = []
    sem = asyncio.Semaphore(queries)
    gen = file_process(urls)
    async with aiohttp.ClientSession() as session:
        workers = [
            asyncio.create_task(url_process(session, gen, sem, k_words, result))
            for _ in range(workers)
        ]
        print("tasks have been created")
        await asyncio.gather(*workers)
        print(result)
        urls.close()
        return result


if __name__ == "__main__":
    asyncio.run(main())
    print(f"It took {time() - start} sec")
