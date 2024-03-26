from fake_useragent import UserAgent
from bs4 import BeautifulSoup
import requests
from openpyxl import load_workbook

ua = UserAgent()


def scrap():

    wb = load_workbook("table.xlsx")
    ws = wb["data"]

    response = requests.get(
            url=f'https://www.carlogos.org/car-brands/', 
            headers={'user-agent': f'{ua.random}'}
    )
        
    soup = BeautifulSoup(response.text, 'lxml')

    main_l = soup.find('div', class_='main-l')

                #Из за того что ссылка https://www.carlogos.org/car-brands/page-1.html не существует то приходится обходить так
                #Gotta do it like that 'cause https://www.carlogos.org/car-brands/page-1.html link doesn't exist

    if main_l is not None:
            brand_list = main_l.find('ul', class_='logo-list')
            for brand in brand_list.find_all('li'):
                car_link = 'https://www.carlogos.org' + brand.find('a').get('href')
                brand_link = 'https://www.carlogos.org' + brand.find('a').find('img').get('src')
                naname = brand.find('a').next_element.next_element
                car_name = naname.text
                type_ofcar = naname.find_next().text
                
                response = requests.get(
                    url=car_link, 
                    headers={'user-agent': f'{ua.random}'}
                )
        
                soup = BeautifulSoup(response.text, 'lxml')
                
                tags_list = soup.find('div', class_='byline-left')
                rr = ''
                for i in tags_list.find_all('a'):
                    rr = rr + ' #' + i.text
                    



                ws.append([car_name, type_ofcar, rr, brand_link])

    for page in range(2, 9):
        response = requests.get(
            url=f'https://www.carlogos.org/car-brands/page-{page}.html', 
            headers={'user-agent': f'{ua.random}'}
        )
        
        soup = BeautifulSoup(response.text, 'lxml')

        main_l = soup.find('div', class_='main-l')
        if main_l is not None:
            brand_list = main_l.find('ul', class_='logo-list')
            for brand in brand_list.find_all('li'):
                car_link = 'https://www.carlogos.org' + brand.find('a').get('href')
                brand_link = 'https://www.carlogos.org' + brand.find('a').find('img').get('src')
                naname = brand.find('a').next_element.next_element
                car_name = naname.text
                type_ofcar = naname.find_next().text
                
                response = requests.get(
                    url=car_link, 
                    headers={'user-agent': f'{ua.random}'}
                )
        
                soup = BeautifulSoup(response.text, 'lxml')
                
                tags_list = soup.find('div', class_='byline-left')
                rr = ''
                for i in tags_list.find_all('a'):
                    rr = rr + ' #' + i.text
                    



                ws.append([car_name, type_ofcar, rr, brand_link])

    wb.save('table.xlsx')
    wb.close()
                

def main():
    scrap()

if __name__ == '__main__':
    main()
