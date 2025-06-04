import time

import requests

headers = {
    "accept": "application/json, text/plain, */*",
    "accept-language": "ru,en-US;q=0.9,en;q=0.8,uk;q=0.7,de;q=0.6",
    "origin": "https://solscan.io",
    "priority": "u=1, i",
    "referer": "https://solscan.io/",
    "sec-ch-ua": '"Chromium";v="130", "Google Chrome";v="130", "Not?A_Brand";v="99"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-site",
    "sol-aut": "Yyt0823op-H=q2=vw4v79mB9dls0fK3YnhkSSmod",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
}

cookies = {
    "cf_clearance": "qK2njizO3KjDAOkvBN.7rXYrYO6e8f7TXPMprJn2tJA-1735031071-1.2.1.1-sTHLuQMgqWJ2_pa9LHSrj0aHVzIo5fnqsS9EqBmdYjrAnYZhcqmO2c_5SxRNsmKFJQaAKk3EIP8R_i39TzChajMfYV4xu5e44.Zeqkv849y62QQ5Uby1cA96iol6Zxc8VgmIn0e2JbQETj_pqArvxjNZApW7rVNIEvRrf2Q1_CixVE6hNq3VHisgMEfvGt6npXMrPMbWzVXKf3IqDGBgm5smN1fPK49CVYJDmsOkB49F3zKeL9o50aEV43eXOfuQy1rdKChYIoT1VFQFRlz7imDg14XD0YOy9Z2F6oNfmnTfETzeX3BKKgM.4JQgC2ENiotNhwFlRZRN1Mh0iDn7cLUqonvs2ry2xd6Dyp5LWn6q_IUW.PivmyyGiBZOpq2fICVLkKaHJ9chLUy_kGUKTzrEkV6zFNjrgQvokHghT3ffqRAcc0Qr48F2mtRnUSsm",
}

# 零交互
def get_tx_count(wallet_address):
    # https://api-v2.solscan.io/v2/account/transaction?address=DwmhQyJ2YGa7PNzjPV5En6jqDxmpuS3xDH8dzmuCZv4E&limit=10
    time.sleep(0.1)

    url = "https://api-v2.solscan.io/v2/account/transaction"
    params = {
        "address": f"{wallet_address}",
        "limit": 10,
    }

    response = requests.get(url, params=params, headers=headers, cookies=cookies)  # 添加代理
    data = response.json()
    tx_count = len(data['data']['transactions'])  # 获取交易数量
    print("tx_count:", tx_count)
    if tx_count == 1:
        return True
    else:
        return False

# 大于 0.5 SOL
def get_address_token(wallet_address):
    # https://api-v2.solscan.io/v2/account/tokenaccounts?address=nPosUpnDtaB4dBaJUMF1bm78E4BTZDwWQWGoEmEyESx&page=1&page_size=480&type=token&hide_zero=true
    time.sleep(0.1)

    url = "https://api-v2.solscan.io/v2/account/tokenaccounts"
    params = {
        "address": f"{wallet_address}",
        "page": 1,
        "page_size": 480,
        "type": "token",
        "hide_zero": True
    }

    response = requests.get(url, params=params, headers=headers, cookies=cookies)
    data = response.json()

    # 获取代币账户数量
    token_count = data['data']['count']
    print("token_count:", token_count)

    # 如果有代币账户, 返回 True
    if token_count > 4:
        return True
    else:
        return False

def read_addresses(file_path):
    """
    从文件中读取钱包地址

    Args:
        file_path (str): 包含钱包地址的文件路径

    Returns:
        list: 钱包地址列表
    """
    with open(file_path, 'r') as f:
        addresses = [line.strip() for line in f if line.strip()]
    return addresses

def process_addresses(addresses):
    """
    处理钱包地址，筛选符合条件的地址并实时写入文件

    Args:
        addresses (list): 钱包地址列表
    """
    output_file = 'valid_addresses.txt'

    # 以追加模式打开文件
    with open(output_file, 'a') as f:
        for address in addresses:
            print(address)
            try:
                if get_address_token(address):
                    f.write(f"{address}\n")  # 立即写入文件
                    f.flush()  # 确保立即写入磁盘
                    print(f"地址 {address} 符合条件")
            except Exception as e:
                print(f"处理地址 {address} 时出错: {e}")
            time.sleep(1)  # 避免请求过快

def main():
    """
    主函数，读取并处理钱包地址
    """
    input_file = 'to_addresses.txt'  # 假设地址存储在这个文件中

    addresses = read_addresses(input_file)
    process_addresses(addresses)

if __name__ == "__main__":
    main()