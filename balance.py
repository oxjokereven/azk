import requests

API_KEY = "c4413624-6fed-4c2a-bcbd-967703786c34"

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

# 测试函数
if __name__ == "__main__":
    address = "FgL5jQzoiXXBM1nFxZyHmeZDmZEfVC5RUchnfjvvESMm"
    is_greater = check_balance_greater_than(address, 0.5)
    print(f"余额是否大于0.5 SOL: {is_greater}")