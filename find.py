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

def get_address_token(owner_address, api_key="c33e38d0-8f94-4140-990a-8548b1eb61d2"):
    """
    获取指定地址的代币账户数量
    
    Args:
        owner_address (str): 要查询的钱包地址
        api_key (str): Helius API密钥, 默认为预设值
    
    Returns:
        int: 代币账户数量
    """
    url = f"https://mainnet.helius-rpc.com/?api-key={api_key}"
    
    payload = {
        "jsonrpc": "2.0",
        "id": "1",
        "method": "getTokenAccountsByOwner",
        "params": [
            owner_address, 
            {"programId": "TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA"}, 
            {"encoding": "jsonParsed"}
        ]
    }
    headers = {"Content-Type": "application/json"}
    
    response = requests.post(url, json=payload, headers=headers)
    response.raise_for_status()  # 检查HTTP错误
        
    result = response.json()
    if 'result' in result and 'value' in result['result']:
        value_length = len(result['result']['value'])
        if value_length > 4:
            return True
        else:
            return False
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