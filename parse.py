from bs4 import BeautifulSoup
import requests

# URL страницы


# Заголовки для запроса
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

def parse_obj(link):
    url = link
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        price_div = soup.find("div", class_="MainInfo_priceBar__tcUgc").text
        name_div = soup.find("h1", class_="MainInfo_title__YSsXk").text
        return [price_div, name_div]
    else:
        print(f"Ошибка при запросе страницы: {response.status_code}")

    return None


def photo_parse(link):
    import requests
    from bs4 import BeautifulSoup


    url = link

    # Отправляем GET-запрос
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36"
    }
    response = requests.get(url, headers=headers)

    # Проверяем успешность запроса
    if response.status_code == 200:
        # Парсим HTML-код страницы
        soup = BeautifulSoup(response.text, "html.parser")

        # Находим тег изображения по классу
        image_tag = soup.find("img", class_="PoizonImage_img__BNSaU")

        if image_tag and "src" in image_tag.attrs:
            # Извлекаем URL изображения
            image_url = image_tag["src"]
            return image_url

