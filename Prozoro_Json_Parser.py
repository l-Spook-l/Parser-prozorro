import requests
from pprint import pprint


def get_json():
    headers = {
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/98.0.4758.82 Safari/537.36",
    }
    list_data = []
    # url = f"https://prozorro.gov.ua/api/search/tenders?filterType=tenders&status%5B0%5D=active.enquiries&status%5B1%5D=active.tendering&cpv%5B0%5D=71630000-3"
    url = f"https://prozorro.gov.ua/api/search/tenders"
    # Получаем JSON файл
    s = requests.session()
    response = s.post(url=url, headers=headers)
    data = response.json()
    quantity_tender_in_page = 20
    total_tenders = data["total"]  # Всего тендеров
    pprint(f'data={data}')
    print(total_tenders)

    if total_tenders <= quantity_tender_in_page:
        page = 1
    else:
        page = total_tenders // quantity_tender_in_page + 1
    try:
        for item in range(1, page + 1):
            print("==============================================================================================")
            print(item)
            url_page = f"https://prozorro.gov.ua/api/search/tenders?filterType=tenders&status%5B0%5D=active.enquiries&status%5B1%5D=active.tendering&cpv%5B0%5D=71630000-3&page={item}"
            session = requests.session()
            response = session.post(url=url_page, headers=headers)
            data_page = response.json()
            for tender in range(quantity_tender_in_page):
                title = data_page["data"][tender]["title"]
                city_company = data_page["data"][tender]["procuringEntity"]["address"]["locality"]
                name_company = data_page["data"][tender]["procuringEntity"]["identifier"]["legalName"]
                ID_tender = data_page["data"][tender]["tenderID"]
                price = data_page["data"][tender]["value"]["amount"]
                start_date = data_page["data"][tender]["enquiryPeriod"]["startDate"][:10]
                link = (f"https://prozorro.gov.ua/tender/{ID_tender}")
                print("---------------------------------------------------------------------------------------")
                list_data += [[title, city_company, name_company, ID_tender, price, start_date, link]]
                print(tender)
                print(title, '\n', city_company, '\n', name_company, '\n', ID_tender,
                      '\n', price, '\n', start_date, '\n', link)
                print("---------------------------------------------------------------------------------------")
    except Exception as ex:
        print('SSSsssssssssssssssssssssssssssssssssssssssssSSS')

    return list_data, total_tenders


def main():
    get_json()


if __name__ == "__main__":
    main()
