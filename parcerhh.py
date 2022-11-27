from bs4 import BeautifulSoup
import requests
import fake_useragent

count_of_page = 0

def get_links(text):
    user_agent =fake_useragent.UserAgent()
    data = requests.get(
        url=f"https://hh.ru/search/vacancy?text={text}&area=0",
        headers={"user-agent":user_agent.random}
    )
    if data.status_code != 200:
        return
    soup = BeautifulSoup(data.content, features="html.parser")
    try:
        page_count = int(soup.find("div",attrs={"class":"pager"}).find_all("span",recursive=False)[-1].find("a").find("span").text)
    except:
        return
    for page in range(page_count):
        try:
            data = requests.get(
                url=f"https://hh.ru/search/vacancy?text={text}&area={page}",
                headers={"user-agent":user_agent.random}
            )
            if data.status_code == 200:
                soup = BeautifulSoup(data.content, features="html.parser")
                for a in soup.find_all("a",attrs={"class":"serp-item__title"}):
                    yield f'{a.attrs["href"].split("?")[0]}'
        except Exception as e:
            print(f"{e}")
    print(page_count)

if __name__ == "__main__":
    for a in get_links("Javascript"): #вместо Javascript любой запрос
        print(a)
        count_of_page +=1
        print(count_of_page)