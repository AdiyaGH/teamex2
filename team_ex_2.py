import os
import time
import wikipedia
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor

def convert_to_str(obj):
    if type(obj) == list:
        mystr = '\n'.join(obj)
        return mystr
    elif type(obj) in [str, int, float]:
        return str(obj)

def dl_and_save(item):
    try:
        page = wikipedia.page(item, auto_suggest=False)
        title = page.title
        references = convert_to_str(page.references)
        out_filename = os.path.join("wiki_dl", title + ".txt")
        print(f'writing to {out_filename}')
        with open(out_filename, 'w') as fileobj:
            fileobj.write(references)
    except Exception as e:
        print(f"Error processing {item}: {e}")

def wiki_sequentially(results):
    print('\nsequential function:')
    t_start = time.perf_counter()
    for item in results:
        dl_and_save(item)
    t_end = time.perf_counter()
    t_lapse = t_end - t_start
    print(f'code executed in {t_lapse} seconds')

def concurrent_threads(results):
    print('\nthread pool function:')
    t_start = time.perf_counter()
    with ThreadPoolExecutor() as executor:
        executor.map(dl_and_save, results)
    t_end = time.perf_counter()
    t_lapse = t_end - t_start
    print(f'code executed in {t_lapse} seconds')

def concurrent_process(results):
    print('\nprocess pool function:')
    t_start = time.perf_counter()
    with ProcessPoolExecutor() as executor:
        executor.map(dl_and_save, results)
    t_end = time.perf_counter()
    t_lapse = t_end - t_start
    print(f'code executed in {t_lapse} seconds')

def get_search_term():
    term = input("Enter a Wikipedia topic to search: ").strip()
    if len(term) < 4:
        term = "generative artificial intelligence"
    return term

def main():
    os.makedirs("wiki_dl", exist_ok=True)
    term = get_search_term()
    results = wikipedia.search(term)
    if not results:
        print("No results found for the search term.")
        return
    print(f"Found {len(results)} results.")
    choice = input("Choose concurrency model: (1) Sequential, (2) Threads, (3) Processes: ")
    if choice == "1":
        wiki_sequentially(results)
    elif choice == "2":
        concurrent_threads(results)
    elif choice == "3":
        concurrent_process(results)
    else:
        print("Invalid choice.")

if __name__ == "__main__":
    main()
