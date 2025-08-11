# 零交互
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed

API_KEY = "c4413624-6fed-4c2a-bcbd-967703786c34"

def get_tx_count(address):
    """获取地址的交易详情, 返回交易数量"""
    url = f"https://api.helius.xyz/v0/addresses/{address}/transactions?api-key={API_KEY}"
    
    try:
        response = requests.get(url, timeout=15)
        if response.status_code == 200:
            result = response.json()
            print("result", result)
            tx_count = len(result)
            print("tx_count", tx_count)
            return tx_count <= 2
    except Exception as e:
        print(f"请求失败 {address}: {e}")
    return False

def check_address(address):
    is_valid = get_tx_count(address) and check_balance_greater_than(address, 0.5)
    return address, is_valid

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

def main():
    input_file = 'T.txt'
    valid_file = '符合条件.txt'
    invalid_file = '不符合条件.txt'

    with open(input_file, 'r') as f:
        addresses = [line.strip() for line in f if line.strip()]

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
                print("符合条件")
                print(address)
                with open(valid_file, 'a') as vf:
                    vf.write(address + '\n')
            else:
                print("不符合条件")
                print(address)
                with open(invalid_file, 'a') as ivf:
                    ivf.write(address + '\n')

if __name__ == "__main__":
    main()