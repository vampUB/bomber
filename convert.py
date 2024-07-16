headers = '''Accept: application/json, text/javascript, */*; q=0.01
Accept-Encoding: gzip, deflate, br
Accept-Language: ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7
Connection: keep-alive
Content-Type: application/x-www-form-urlencoded; charset=UTF-8
Cookie: sushifuji=OqECatFxKVDhfBrZyGW2vFpaaMjHtN2DAI5J8qsphlI%2CiFyE; city_id=1; city_url=ufa; order_delivery_type=pickup; cart_products=%7B%7D; _ym_uid=1689182384695473225; _ym_d=1689182384; _ga=GA1.2.1538392118.1689182384; _gid=GA1.2.2037129987.1689182384; _ym_visorc=w; _ym_isad=2; deviceId=5c238971e40ada29238fb63b5c496171
Host: www.sushifuji.ru
Origin: https://www.sushifuji.ru
Referer: https://www.sushifuji.ru/
Sec-Fetch-Dest: empty
Sec-Fetch-Mode: cors
Sec-Fetch-Site: same-origin
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36
X-Requested-With: XMLHttpRequest
sec-ch-ua: "Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"
sec-ch-ua-mobile: ?0
sec-ch-ua-platform: "Windows"'''

print('{\'' + headers.replace(': ', '\': \'').replace('\n', '\', \'') + '\'}')