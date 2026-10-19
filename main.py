import csv
import requests
from bs4 import BeautifulSoup


URL = "https://quotes.toscrape.com/"


HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36")}




def fetch_html(url):

    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        print(f"Ошибка при запросе к сайту: {e}")
        return None


def parse_data(html):

    soup = BeautifulSoup(html, "html.parser")
    parsed_items = []

    quotes = soup.find_all("div", class_="quote")

    for item in quotes:
        text = item.find("span", class_="text").get_text(strip=True)
        author = item.find("small", class_="author").get_text(strip=True)
        tags = [tag.get_text(strip=True) for tag in item.find_all("a", class_="tag")]
        tags_str = ", ".join(tags)

        parsed_items.append({"text": text, "author": author, "tags": tags_str})

    return parsed_items


def save_to_csv(data, filename="scraped_quotes.csv"):

    if not data:
        print("Нет данных для сохранения.")
        return

    keys = data[0].keys()
    with open(filename, mode="w", encoding="utf-8-sig", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=keys)
        writer.writeheader()
        writer.writerows(data)

    print(f"Успешно сохранено {len(data)} записей в файл '{filename}'!")


def main():
    print("Начинаем парсинг...")
    html = fetch_html(URL)

    if html:
        data = parse_data(html)
        print(f"Найдено элементов: {len(data)}")

        if data:
            print("Пример первого элемента:", data[0])

        save_to_csv(data)


if __name__ == "__main__":
    main()