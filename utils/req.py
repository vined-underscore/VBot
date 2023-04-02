import random

__api__ = "https://discord.com/api/v9"


def randstr(length: int) -> str:
    alpha = "abcdefghijklmnopqrstuvwxyz0123456789"
    text = ''
    for _ in range(0, length):
        text += alpha[random.randint(0, len(alpha) - 1)]

    return text


def headers(bot_token: str) -> dict:
    return {
        "authorization": bot_token,
        "accept": "*/*",
        'accept-encoding': 'gzip, deflate, br',
        "accept-language": "en-US,en;q=0.9,it-IT;q=0.8,it;q=0.7,en-GB;q=0.6",
        "content-type": "application/json",
        "cookie": f"__cfuid={randstr(43)}; __dcfduid={randstr(32)}; locale=en-US",
        "origin": "https://discord.com",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (Linux armv7l) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36 OPR/40.0.2207.0 OMI/4.9.0.237.Martell-2.258 Model/Hisense-MT5658-SDK4-9 (Hisense;HU43K303UW;V1000.01.00a.I1207) CE-HTML/1.0 HbbTV/1.2.1 MTK5658US Hisense-MT5658-US",
        "x-context-properties": "eyJsb2NhdGlvbiI6IlVzZXIgUHJvZmlsZSJ9",
        "x-debug-options": "bugReporterEnabled",
        "x-discord-locale": "en-US",
        "x-super-properties": "eyJvcyI6IldpbmRvd3MiLCJicm93c2VyIjoiRGlzY29yZCBDbGllbnQiLCJyZWxlYXNlX2NoYW5uZWwiOiJzdGFibGUiLCJjbGllbnRfdmVyc2lvbiI6IjEuMC45MDExIiwib3NfdmVyc2lvbiI6IjEwLjAuMTkwNDUiLCJvc19hcmNoIjoieDY0Iiwic3lzdGVtX2xvY2FsZSI6ImVuLVVTIiwiY2xpZW50X2J1aWxkX251bWJlciI6MTc4ODUwLCJuYXRpdmVfYnVpbGRfbnVtYmVyIjoyOTU4NCwiY2xpZW50X2V2ZW50X3NvdXJjZSI6bnVsbCwiZGVzaWduX2lkIjowfQ=="
    }
