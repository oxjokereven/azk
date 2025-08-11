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
            tx_count = len(result)
            print("tx_count", tx_count)
            return tx_count <= 2
    except Exception as e:
        print(f"请求失败 {address}: {e}")
    return False

def check_address(address):
    is_valid = get_tx_count(address)
    return address, is_valid

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