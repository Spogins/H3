import requests
from bs4 import BeautifulSoup

URL = 'https://ru.wikipedia.org/wiki/%D0%A1%D0%BF%D0%B8%D1%81%D0%BE%D0%BA' \
          '_%D0%B3%D0%BE%D1%81%D1%83%D0%B4%D0%B0%D1%80%D1%81%D1%82%D0%B2'
HEADERS = {
    'accept':
        'text/html,application/xhtml+xml,application/xml;q=0.9,image'
        '/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'user-agent':
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit'
        '/537.36 (KHTML, like Gecko) Chrome/102.0.5005.115 Safari/537.36 OPR/88.0.4412.75'
}


#получение html
def get_html(url):
    result = requests.get(url, headers=HEADERS)
    return result


#получение странн
def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find('tbody').find_all('td')
    return items


#высчитывание одинаковых букв и составление словаря
def same_letter_ct(source):
    result = {}
    for lt in source:
        country = lt.find('img').get('alt')
        if country[0] not in result:
            result[country[0]] = 1
        else:
            result[country[0]] += 1

    return result


#преобразование и структурирование данных в список из словарей
def create_list_of_dict(items):
    item_list = items[1::2]
    full_names = item_list[1::2]
    source = item_list[::2]

    letter_dict = same_letter_ct(source)
    country_list = []

    for i in range(len(full_names)):
        country = source[i].find('img').get('alt')
        full_name = full_names[i].text.strip()
        flag_url = source[i].find('img').get('src')

        country_list.append(
            {
                'country': country,
                'full_country_name': full_name,
                'same_letter_count': letter_dict[country[0]],
                'flag_url': flag_url,
                'full_country_name_word_ct': full_name.count(' ') + 1
            }
        )

    return country_list


#получение словаря по короткому названию страны
def get_country(country):
    html = get_html(URL)
    content = get_content(html.text)
    list_of_dict = create_list_of_dict(content)

    for elem in list_of_dict:
        if elem['country'].lower() == country.lower():
            return print(elem)
    return print('No result')



#вызов функции
get_country(input("Сountry: "))
