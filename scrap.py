import requests
import lxml.html as html # para aplicar Xpath a HTML
import os
import datetime

HOME_URL = 'https://www.elcomercio.com/'


XPATH_LINK_TO_ARTICLE = '//h3[@class="article-highlighted__title"]/a/@href' #links of each of the news
XPATH_TITLE = '//h1[@class="entry__title"]/text()'
XPATH_BODY = '//div[@class="entry__content"]/p'

def parse_notice(link, today):
    try: 
        response =  requests.get(link)
        if response.status_code == 200:
            notice = response.content.decode('utf-8')#brings the html code from the website
            parsed = html.fromstring(notice)

            try:
                title =  parsed.xpath(XPATH_TITLE)[0]#extract title
                title = title.replace('\"', '')#deletes the character "
                title = title.replace('\'', '')#deletes the character "
                body =  parsed.xpath(XPATH_BODY)

                #for i in body:
                #    print(i.text_content())

            except IndexError:
                return
            with open(f'{today}/{title}.txt', 'w', encoding='utf-8') as f:
                f.write(title)
                f.write('\n\n')
                for p in body:
                    f.write(p.text_content())
                    f.write('\n')
            
                    
        else:
            raise ValueError(f'Error: {response.status_code}')
    except ValueError as ve:
        print(ve)
        


def parse_home():
    try:
        response = requests.get(HOME_URL)
        
        if response.status_code == 200:# Status code 200 means that everything is ok
            home = response.content.decode('utf-8')
            parsed = html.fromstring(home)
    
            links_to_notices = parsed.xpath(XPATH_LINK_TO_ARTICLE)
            #print(links_to_notices)

            today = datetime.date.today().strftime('%d-%m-%Y')
            if not os.path.isdir(today):
                os.mkdir(today)#make a dir with the name of the day
                for link in links_to_notices:
                    print(link)
                    parse_notice(link, today)
                    print('*'*10)



            
        else:
            raise ValueError(f"Error: {response.status_code}")


    except ValueError as ve: 
        print(ve)

def main():
    parse_home()

if __name__ == '__main__':
    main()
