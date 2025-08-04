import time
import requests

# Helius API 密钥
API_KEY = "ce79497c-4d3e-41d5-ae64-6b33034c8003"

# 零交互
def get_tx_count(address):
    """获取地址的交易详情, 返回交易数量"""
    url = f"https://api.helius.xyz/v0/addresses/{address}/transactions?api-key={API_KEY}"
    
    response = requests.get(url)
    if response.status_code == 200:
        result = response.json()
        tx_count = len(result)

        if tx_count == 1:
            return True
        else:
            return False, result

# 大于 0.5 SOL, 这个函数暂时无法使用.
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

    response = requests.get(url, params=params)
    data = response.json()

    # 获取代币账户数量
    token_count = data['data']['count']
    print("token_count:", token_count)

    # 如果有代币账户, 返回 True
    if token_count > 4:
        return True
    else:
        return False

# 读取文件, 返回地址列表
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

# 解析文件, 筛选符合条件的地址
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
                if get_tx_count(address):
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