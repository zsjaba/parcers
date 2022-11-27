from bs4 import BeautifulSoup
import requests
import fake_useragent

count_of_page = 0
def get_links(text):
    user_agent =fake_useragent.UserAgent()
    data = requests.get(
        url=f"https://habr.com/ru/search/page1/?q={text}&target_type=posts&order=relevance",
        headers={"user-agent":user_agent.random}
    )
    if data.status_code != 200:
        return
    soup = BeautifulSoup(data.content, features="html.parser")
    try:
        page_count = int(soup.find("div",attrs={"class":"tm-pagination__pages"}).find_all("div",recursive=False)[-1].find_all("a",recursive=False)[-1].text)
    except:
        return
    for page in range(page_count):
        try:
            data = requests.get(
                url=f"https://habr.com/ru/search/page{page}/?q={text}&target_type=posts&order=relevance",
                headers={"user-agent":user_agent.random}
            )
            if data.status_code == 200:
                soup = BeautifulSoup(data.content, features="html.parser")
                for a in soup.find_all("a", attrs={"class": "tm-article-snippet__title-link"}):
                    yield f'https://habr.com{a.attrs["href"]}'
        except Exception as e:
            print(f"{e}")
    print(page_count," - поиск завершен")


if __name__ == "__main__":
    for a in get_links("python"): #вместо Javascript любой запрос
        print(a)
        count_of_page += 1
        print(count_of_page)











