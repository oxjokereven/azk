def extract_to_addresses(file_path):
    addresses = []

    with open(file_path, 'r') as file:
        for line in file:
            # 检查行是否包含 "to :"
            if 'to: ' in line:
                # 提取 "to: " 后的地址
                address = line.split('to: ')[1].strip()
                addresses.append(address)

    return addresses

# 使用示例
file_path = 'joker.txt'
to_addresses = extract_to_addresses(file_path)

# 打印所有地址
for address in to_addresses:
    print(address)

# 如果需要，可以保存到文件
with open('to_addresses.txt', 'w') as output_file:
    for address in to_addresses:
        output_file.write(address + '\n')

# 打印地址总数
print(f"总共找到 {len(to_addresses)} 个地址")