import json,os,re,requests,threading,urllib3,m3
from concurrent.futures import ThreadPoolExecutor, as_completed
from openpyxl.workbook import Workbook
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

session = requests.session()

wb = Workbook()
ws = wb.active
ws.append(["avgRating", "numRatings", "firstName", "lastName", "department", "school_name", "avgDifficulty"])
ex_list = []
lock = threading.Lock()


def send(url):
    try:
        #cookie
        cookie = 'logglytrackingsession=a4ef94f4-a0bd-46e5-928c-54258feff8f4; __browsiUID=fd4698a7-81d2-4a76-8ad5-2371457da02b; _gid=GA1.2.1634526718.1697180095; _pbjs_userid_consent_data=3524755945110770; _pubcid=bb76ee83-9d15-44ee-948b-11021bb48679; _hjFirstSeen=1; _hjSession_1667000=eyJpZCI6ImRjNTlkMDI4LTdlY2ItNDZlOC05ZDg1LTY2OTk0YWY2NjdiNSIsImNyZWF0ZWQiOjE2OTcxODAxMDA1NjksImluU2FtcGxlIjpmYWxzZSwic2Vzc2lvbml6ZXJCZXRhRW5hYmxlZCI6dHJ1ZX0=; _hjAbsoluteSessionInProgress=0; _au_1d=AU1D-0100-001697180102-AALWE1CR-LCXL; pjs-unifiedid=%7B%22TDID%22%3A%22d9f8dc0c-1c4a-4dfe-949f-0306a576e9a3%22%2C%22TDID_LOOKUP%22%3A%22FALSE%22%2C%22TDID_CREATED_AT%22%3A%222023-10-13T06%3A55%3A01%22%7D; panoramaId_expiry=1697266509298; _cc_id=3dad1ad50a194be55aab67636fcc2cc8; panoramaId=82d6ab7ace9d6a5d058ea051793ea9fb927aa6480a3d3d6db33b51c25e8ccd8d; ccpa-notice-viewed-02=true; _hjSessionUser_1667000=eyJpZCI6IjQyMmFhMTNhLWQ3ZDEtNWUxMC05YWI4LTdjMWZlMGQwMTljYiIsImNyZWF0ZWQiOjE2OTcxODAxMDA1NjQsImV4aXN0aW5nIjp0cnVlfQ==; _ga_J1PYGTS7GG=GS1.1.1697180159.1.0.1697180204.0.0.0; _au_last_seen_pixels=eyJhcG4iOjE2OTcxODAxMDIsInR0ZCI6MTY5NzE4MDEwMiwicHViIjoxNjk3MTgwMTAyLCJydWIiOjE2OTcxODAxMDIsInRhcGFkIjoxNjk3MTgwMTAyLCJhZHgiOjE2OTcxODAxMDIsImdvbyI6MTY5NzE4MDEwMiwidW5ydWx5IjoxNjk3MTgwMTAyLCJvcGVueCI6MTY5NzE4MDEwMiwiY29sb3NzdXMiOjE2OTcxODAxMDIsImFkbyI6MTY5NzE4MDI3MiwidGFib29sYSI6MTY5NzE4MDI3MiwiYmVlcyI6MTY5NzE4MDI3Miwic29uIjoxNjk3MTgwMjcyLCJpbXByIjoxNjk3MTgwMjcyLCJpbmRleCI6MTY5NzE4MDI3MiwicHBudCI6MTY5NzE4MDI3MiwiYW1vIjoxNjk3MTgwMjcyLCJzbWFydCI6MTY5NzE4MDI3Mn0%3D; cid=lu_nEKX8Ma-20231013; trc_cookie_storage=taboola%2520global%253Auser-id%3Dbcbc1b4b-ee10-44bd-af97-70e62d5a5ee8-tuctc227303; cto_bidid=ufksyl9PYkk5NXp6d3R6QiUyQmttNTJQM0tLRWdhMmpRd2slMkJKVjNQZ1FWMVJWMlZzQWNualpLNElpRXo2VXp5ZUdNSWVSZDJDQWY2dUZoUFo0cXE2VGhRMlAzWSUyQnpNZ2E1RmRKU1I4dGZyZiUyQnF1c2JUQU85RlhLRWxMYlRtUUluV1pFRHhw; cto_bundle=KCP4_19Ld3o3UGdnRXpRT1BrVnJUenc5dUh6WHB5S3VkUkNIbElLNmswV1JmMHpMUyUyQjVzbzhPbEZrQXkxTFhFRDdBcm4wUEQxJTJGYXU2ZnNnc2VmS0pYMlZhN1hjUmVqeVRHOE5paTdYUXIlMkJGN3ZiNiUyQkc4dElGVkhYcUlWT1c5TWlCelhybzBiWiUyRk51TUFFMVF6N2ZraXd0TTRXSURaak85JTJGMFBYRHdJNDdSUWdIdmMlM0Q; __gads=ID=2a2bebe34903a8be:T=1697180096:RT=1697190065:S=ALNI_MYlvkY_dY3mD3vuFAZiEe4PVDND1A; __gpi=UID=00000c5e22df0d95:T=1697180096:RT=1697190065:S=ALNI_MbsneoX0qzVWJQha41EkfZwLickKQ; __browsiSessionID=1d2a55e6-51e1-45f2-a460-039dfeba1cf9&true&false&DEFAULT&cn&desktop-4.20.11&false; _ga=GA1.1.2033181820.1697180095; _hjIncludedInSessionSample_1667000=0; _ga_WET17VWCJ3=GS1.1.1697190758.3.1.1697190920.0.0.0'
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'Host': 'www.ratemyprofessors.com',
            'Pragma': 'no-cache',
            'Sec-Ch-Ua': '"Microsoft Edge";v="117", "Not;A=Brand";v="8", "Chromium";v="117"',
            'Sec-Ch-Ua-Mobile': '?0',
            'Sec-Ch-Ua-Platform': '"Windows"',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-User': '?1',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36 Edg/117.0.2045.60',
            'Cookie': cookie
        }
        print('start:', url)
        # home
        resp = session.get(url, verify=False, headers=headers)
        # id
        start = resp.text.index('STORE__ = {') + 9
        end = resp.text.index('window.process = {}')
        dict = json.loads(resp.text[start:end].strip()[:-1])
        id=dict['client:root'].keys().__str__().split('"')[1]

        print('id:', id)

        # Authorization
        authorization = 'Basic ' + re.search(r'GRAPHQL_AUTH":"(.*?)",', resp.text).group(1).strip()
        print('用户认证:', authorization)

        dict = m3.get_count(authorization, url, id)

        try:
            count = dict['data']['search']['teachers']['resultCount']
        except Exception as ex:
            dict = m3.get_count(authorization, url, id)
        print('count:', dict)
        data = m3.get_data(authorization, url, id, count)

        for e in data:
            list = []
            # avgRating
            avgRating = e['node']['avgRating']
            list.append(avgRating)
            # numRatings
            numRatings = e['node']['numRatings']
            list.append(numRatings)
            # firstName
            firstName = e['node']['firstName']
            list.append(firstName)
            # lastName
            lastName = e['node']['lastName']
            list.append(lastName)
            # department
            department = e['node']['department']
            list.append(department)
            # school_name
            school_name = e['node']['school']['name']
            list.append(school_name)
            # avgDifficulty
            avgDifficulty = e['node']['avgDifficulty']
            list.append(avgDifficulty)
            with lock:
                ws.append(list)
    except Exception as e:
        ex_list.append(url)


url_list = []
with open('link.txt', 'r', encoding='utf-8') as f:
    for readline in f.readlines():
        url_list.append(readline.strip())
executor = ThreadPoolExecutor(max_workers=1)
tasks = []
for link in url_list:
    task = executor.submit(send, link)
    task.daemon = True
    tasks.append(task)
for future in as_completed(tasks):
    result = future.result()

print(f'down,{len(url_list)}link,fialed{len(ex_list)}')
for ex in ex_list:
    print(ex)
wb.save("output.xlsx")
