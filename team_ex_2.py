import os
import time
import wikipedia
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor

# Task 3: make convert_to_str always return a safe string
def convert_to_str(obj):
    # If it's a list, convert each element to string and join with newlines
    if isinstance(obj, list):
        return '\n'.join(str(x) for x in obj)
    # If it's None, return an empty string
    if obj is None:
        return ""
    # For any other type (str, int, float, dict, custom objects), just use str()
    return str(obj)

# Task 4: new function that does the same job but matches your task description
def ask_topic_from_usr():
    term = input("Enter a Wikipedia topic to search (4+ characters): ").strip()
    if len(term) < 4:
        print("Search term too short. Using default: 'generative artificial intelligence'.")
        return "generative artificial intelligence"
    return term

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

def main():
    os.makedirs("wiki_dl", exist_ok=True)

    # Task 4: use your new function instead of get_search_term
    term = ask_topic_from_usr()

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
