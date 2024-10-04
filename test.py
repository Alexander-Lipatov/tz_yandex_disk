import requests
import json
from urllib import parse

cookies = {
    'yashr': '5727451001715869894',
    'yuidss': '8760629071715869894',
    'font_loaded': 'YSv1',
    'gdpr': '0',
    '_ym_uid': '1716647019824106268',
    'ymex': '2032007020.yrts.1716647020',
    'amcuid': '738512931716789118',
    'my': 'YwA=',
    'L': 'CAFRYE5yf1FZCXpHQFdgXAt1VnFkd3BjLi4xeglWYWN1Aw==.1720849220.15803.344021.2cc16619df0660e4e7dcba7a9c7d87bf',
    'i': 'zwc4CKjX/ri5moBVc9kAsTqjsz7RSsy/j1UyB+Xbvrn1fZszorO4+QBacXEmoyIl6fUmVzUpxiTDHIByiMd3wmWa+88=',
    'Session_id': '3:1727699390.5.0.1716647314681:cqb5VQ:4a.1.2:1|973380703.-1.2.2:4201906.3:1720849220|3:10296041.297163.OA6rlJyWWPMydNtTEak6sLDtIJI',
    'sessar': '1.1194.CiDfzxNAYdjDencXEMypUSC4CUh0jehlBUKTtL7sjTskFQ.Z_r09gIxxh0QjFDITDGqywdBvfX_QoD_FLZUQlVNfkU',
    'sessionid2': '3:1727699390.5.0.1716647314681:cqb5VQ:4a.1.2:1|973380703.-1.2.2:4201906.3:1720849220|3:10296041.297163.fakesign0000000000000000000',
    'isa': 'qs/Ns9rBmYAL/U/Jwh1EJ4PdKt3y32l38HU0hNv0PqdmWEpGYlgGYVEfYD76RsWJj1Wjt4+efY/dH4KNFTyASFPtlmE=',
    'sae': '0:EC878522-2357-49FE-8040-3D7066F3D969:p:24.7.3.1248:m:d:RU:20240323',
    'yandex_gid': '239',
    '_ym_d': '1727772916',
    'yabs-vdrf': 'A0',
    '_ym_isad': '2',
    'cycada': 'UunWoIERiaTLln8PQsWr4qM4nV6RW/avOiXyn8Bxfnw=',
    '_yasc': 'AO9stV45yD/xQZTM/fIvUFPQMiVBJEq8oozbC3QGNPtmdZKrhQF64OlTAf04VeswZvAJxTutQsmJOO2dyoO/YXAeLtHjBIdU',
    'yp': '1752385220.cld.1955450#1728130015.dlp.2#1730377791.hdrc.1#2043314120.pcs.0#1743544992.szm.2%3A1680x1050%3A1632x847#2036209220.udn.cDrQkNC70LXQutGB0LDQvdC00YAg0JvQuNC%2F0LDRgtC%2B0LI%3D#1732624213.vhstfltr_onb.3%3A1724848212963#1730364915.ygu.1#1730455405.csc.1#1759490120.swntab.0',
    'ys': 'udn.cDrQkNC70LXQutGB0LDQvdC00YAg0JvQuNC%2F0LDRgtC%2B0LI%3D#wprid.1727942125325617-14110923834372222511-balancer-l7leveler-kubr-yp-sas-62-BAL#c_chck.347241054',
    'is_gdpr': '1',
    'is_gdpr_b': 'CNa0CBDGlgIYASgC',
    'bh': 'Ek8iTm90L0EpQnJhbmQiO3Y9IjgiLCAiQ2hyb21pdW0iO3Y9IjEyNiIsICJZYUJyb3dzZXIiO3Y9IjI0LjciLCAiWW93c2VyIjt2PSIyLjUiGgUieDg2IioCPzA6ByJtYWNPUyJCCCIxMy42LjciSgQiNjQiUmciTm90L0EpQnJhbmQiO3Y9IjguMC4wLjAiLCAiQ2hyb21pdW0iO3Y9IjEyNi4wLjY0NzguMjM0IiwgIllhQnJvd3NlciI7dj0iMjQuNy4zLjEyNDgiLCAiWW93c2VyIjt2PSIyLjUiWgI/MGCYhfq3Bmoj3MrRtgG78Z+rBPrWhswI0tHt6wP8ua//B9/998cB0IXNhwg=',
}

headers = {
    'Accept': '*/*',
    'Accept-Language': 'ru,en;q=0.9',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Content-Type': 'text/plain',
    'Origin': 'https://disk.yandex.ru',
    'Pragma': 'no-cache',
    'Referer': 'https://disk.yandex.ru/d/rvxmhiSIhDSMCA/Django/%D0%94%D0%97',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 YaBrowser/24.7.0.0 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest',
    'X-Retpath-Y': 'https://disk.yandex.ru/d/rvxmhiSIhDSMCA/Django/%D0%94%D0%97',
    'sec-ch-ua': '"Not/A)Brand";v="8", "Chromium";v="126", "YaBrowser";v="24.7", "Yowser";v="2.5"',
    'sec-ch-ua-arch': '"x86"',
    'sec-ch-ua-bitness': '"64"',
    'sec-ch-ua-full-version-list': '"Not/A)Brand";v="8.0.0.0", "Chromium";v="126.0.6478.234", "YaBrowser";v="24.7.3.1248", "Yowser";v="2.5"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
    'sec-ch-ua-platform-version': '"13.6.7"',
    'sec-ch-ua-wow64': '?0',
}


json_data = json.dumps({
    "items": [
        "A60RFmVbsWH2LscugN4z7VXUZ/EAWxWNK81MKSYf8MZQav9bLzM+qv5SxdHBy1dVq/J6bpmRyOJonT3VoXnDag==:/Django/ДЗ/Python_ДЗ_Модуль_20_Фреймворки_ч_1.pdf",
        "A60RFmVbsWH2LscugN4z7VXUZ/EAWxWNK81MKSYf8MZQav9bLzM+qv5SxdHBy1dVq/J6bpmRyOJonT3VoXnDag==:/Django/ДЗ/Python_ДЗ_Модуль_20_Фреймворки_ч_2.pdf",
        "A60RFmVbsWH2LscugN4z7VXUZ/EAWxWNK81MKSYf8MZQav9bLzM+qv5SxdHBy1dVq/J6bpmRyOJonT3VoXnDag==:/Django/ДЗ/Python_ДЗ_Модуль_20_Фреймворки_ч_3.pdf",
        "A60RFmVbsWH2LscugN4z7VXUZ/EAWxWNK81MKSYf8MZQav9bLzM+qv5SxdHBy1dVq/J6bpmRyOJonT3VoXnDag==:/Django/ДЗ/Python_ДЗ_Модуль_20_Фреймворки_ч_4.pdf",
        "A60RFmVbsWH2LscugN4z7VXUZ/EAWxWNK81MKSYf8MZQav9bLzM+qv5SxdHBy1dVq/J6bpmRyOJonT3VoXnDag==:/Django/ДЗ/Python_ДЗ_Модуль_20_Фреймворки_ч_5.pdf",
        "A60RFmVbsWH2LscugN4z7VXUZ/EAWxWNK81MKSYf8MZQav9bLzM+qv5SxdHBy1dVq/J6bpmRyOJonT3VoXnDag==:/Django/ДЗ/Python_ДЗ_Модуль_20_Фреймворки_ч_6.pdf",
    ],
    "sk": "u65fda96044586e15c2613e29a8b80cd0",
    "uid": "973380703"
})

data = parse.quote(json_data)
print(data)
response = requests.post('https://disk.yandex.ru/public/api/bulk-download-url',
                         cookies=cookies, headers=headers, data=data)

print(response.json())
