import time
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed

# Helius API 密钥
API_KEY = "ce79497c-4d3e-41d5-ae64-6b33034c8003"

# 零交互
def get_tx_count(address):
    """获取地址的交易详情, 返回交易数量"""
    url = f"https://api.helius.xyz/v0/addresses/{address}/transactions?api-key={API_KEY}"
    
    try:
        response = requests.get(url, timeout=15)
        if response.status_code == 200:
            result = response.json()
            tx_count = len(result)
            print("tx_count", tx_count)
            # 同时满足 交易数量小于2 和 余额大于0.5 SOL
            return tx_count <= 2 and check_balance_greater_than(address, 0.5)
    except Exception as e:
        print(f"请求失败 {address}: {e}")
    return False

def check_balance_greater_than(address, threshold=0.5):
    """
    检查地址余额是否大于指定阈值
    
    Args:
        address (str): 要检查的地址
        threshold (float): 阈值，默认为0.5 SOL
    
    Returns:
        bool: 如果余额大于阈值返回True，否则返回False
    """
    url = f"https://mainnet.helius-rpc.com/?api-key={API_KEY}"
    
    payload = {
        "jsonrpc": "2.0",
        "id": "1",
        "method": "getBalance",
        "params": [address]
    }
    headers = {"Content-Type": "application/json"}
    
    try:
        response = requests.post(url, json=payload, headers=headers)
        result = response.json()
        
        if 'result' in result and 'value' in result['result']:
            lamports = result['result']['value']
            sol_balance = lamports / 1_000_000_000
            print(f"余额: {sol_balance:.2f} SOL")
            return sol_balance > threshold
        else:
            print("获取余额失败:", result)
            return False
    except Exception as e:
        print(f"请求失败: {e}")
        return False

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
    
    try:
        response = requests.post(url, json=payload, headers=headers, timeout=15)
        response.raise_for_status()  # 检查HTTP错误
            
        result = response.json()
        if 'result' in result and 'value' in result['result']:
            value_length = len(result['result']['value'])
            return value_length > 4
    except Exception as e:
        print(f"代币请求失败 {owner_address}: {e}")
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

def check_address(address):
    """检查地址是否符合条件"""
    is_valid = get_tx_count(address)
    return address, is_valid

def main():
    input_file = 'to_addresses.txt'
    output_file = 'valid_addresses.txt'

    addresses = read_addresses(input_file)
    max_workers = 3  # 并发度，可按需调整

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(check_address, addr) for addr in addresses]
        for future in as_completed(futures):
            try:
                address, is_valid = future.result()
            except Exception as e:
                print(f"任务执行异常: {e}")
                continue
            if is_valid:
                print(f"地址 {address} 符合条件")
                with open(output_file, 'a') as f:
                    f.write(f"{address}\n")
            else:
                print(f"地址 {address} 不符合条件")

if __name__ == "__main__":
    main()