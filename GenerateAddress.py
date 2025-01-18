import ipaddress
import threading
import concurrent.futures
from tqdm import tqdm
tid = 0
AllScope = '0123456789abcdef'
file_lock = threading.Lock()
def expand(pattern, index, string):
    if index >= len(pattern):
        yield pattern
        return
    if pattern[index] == '*':
        for digit in string:
            yield from expand(pattern[:index] + digit + pattern[index + 1:], index, string)
    else:
        yield from expand(pattern, index + 1, string)



def generate_allnode_addresses_without_scan_withWrite(lowDimPatterns, seeds):
    global tid
    type = "target" + str(tid) + "-"
    num = 0
    if len(lowDimPatterns) <= 10000:
        # print(1)
        parallel_new(lowDimPatterns, num, type)
    else:
        round = int((len(lowDimPatterns) / 10000) + 1)
        if len(lowDimPatterns) % 10000 == 0:
            round = round - 1
        for i in range(round):
            if i == round - 1:
                parallel_new(lowDimPatterns[i * 10000:], num, type)
            else:
                parallel_new(lowDimPatterns[i * 10000:(i + 1) * 10000], num, type)
            num += 1
    tid += 1

def parallel_new(data_list, num, type):
    # generateAddressAndWrite(0,data_list[0])
    # 创建一个线程池
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
        # 使用 enumerate 获取索引和元素，然后提交到线程池中执行
        futures = {executor.submit(generateAddressAndWrite, item, num, type): item for
                   index, item in enumerate(data_list)}

        # 等待所有任务完成
        for future in tqdm(concurrent.futures.as_completed(futures)):
            # 可以捕获异常等，此处为了简化没有展示
            pass

def generateAddressAndWrite(space, num, type):
    addrList = []
    for address in expand(space, 0, AllScope):
        addrList.append(ipaddress.IPv6Address(address).compressed)

    if len(addrList) > 0:
        with file_lock:
            with open(type + str(num), 'a', encoding='utf-8') as f:
                for addr in addrList:
                    f.write(addr + '\n')



















