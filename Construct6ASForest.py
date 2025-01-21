import ipaddress
import queue
from nis import match

import numpy as np
import random
import time

from exceptiongroup import catch

from Definitions import TreeNode
from GenerateAddress import generate_allnode_addresses_without_scan_withWrite

allSpaceList = set()
allLeafList = set()


def construct6ASTree(V, DHCType, lowDimFile):
    init_start_time = time.time()
    start_time = time.time()
    lowDimPatterns = construct6ASTreeByDHC(V, DHCType,12)
    end_time = time.time()
    elapsed_time = end_time - start_time
    print("构建6ASTree耗时：", elapsed_time, "秒")
    print("6AsTree中包含低维度地址模式数量：", len(lowDimPatterns))
    with open(lowDimFile, 'w', encoding='utf-8') as f:
        for pattern in lowDimPatterns:
            f.write(pattern + '\n')
    end_time = time.time()
    elapsed_time = end_time - init_start_time
    print("代码总耗时：", elapsed_time, "秒")


def construct6ASForest(V, treeNum=10):
    init_start_time = time.time()
    start_time = time.time()
    # seeds = set([trancAddress(e) for e in V])
    lowDimPatterns = construct6ASTreeByDHC(V)
    end_time = time.time()
    elapsed_time = end_time - start_time
    print("构建6ASTree耗时：", elapsed_time, "秒")
    print("6AsTree中包含低维度地址模式数量：", len(lowDimPatterns))
    start_time = time.time()
    lowDimPatterns += constructAdditional6ASTrees(V, treeNum)
    end_time = time.time()
    elapsed_time = end_time - start_time
    print("构建6ASForest耗时：", elapsed_time, "秒")
    print("6AsForest中包含低维度地址模式数量：", len(lowDimPatterns))
    lowDimPatterns=list(set(lowDimPatterns))
    # 将IPv6地址模式输出到文件中，
    # 使用 GenerateAddress{https://github.com/KeenoHao/GenerateAddress.git}工具快速生成地址
    with open("lowDimPatterns", 'w', encoding='utf-8') as f:
        for pattern in lowDimPatterns:
            f.write(pattern + '\n')
    end_time = time.time()
    elapsed_time = end_time - init_start_time
    print("代码总耗时：", elapsed_time, "秒")

    # 也可用python生成，速度慢
    # start_time = time.time()
    # generate_allnode_addresses_without_scan_withWrite(lowDimPatterns, seeds)
    # end_time = time.time()
    # elapsed_time = end_time - start_time
    # print("生成IPv6目标地址耗时：", elapsed_time, "秒")
    # elapsed_time = end_time - init_start_time
    # print("代码总耗时：", elapsed_time, "秒")


def constructAdditional6ASTrees(V, treeNum, beta=12):
    root = TreeNode(V)
    init_subspace(root, V)
    spiltIndexArray = generateSpiltIndexArray(root.dimension, treeNum)
    leafs = []
    for i in range(treeNum):
        leafs += construct6ASTreeInForest(V, spiltIndexArray[i])
    return narrowDimension(leafs)


def construct6ASTreeInForest(V, curspiltIndexArray, beta=12):
    root = TreeNode(V)
    init_subspace(root, V)
    leaf_nodes = []
    spaceList = []
    DHCWithArray(root, beta, V, leaf_nodes, spaceList, curspiltIndexArray)
    return leaf_nodes


def construct6ASTreeByDHC(V, DHCType="LeftVDPS", beta=12):
    root = TreeNode(V)
    init_subspace(root, V)
    leafs = []
    DHC(root, beta, V, leafs, DHCType)
    return narrowDimension(leafs)


def generateSpiltIndexArray(dimension, number):
    spiltIndexArray = [[] for _ in range(number)]
    for i in range(number):
        # 初始化数组
        arr = []
        # 生成数组元素
        for j in range(dimension, 0, -1):
            # 生成i到1之间的随机整数（包括i但不包括0）
            element = random.randint(1, j)
            arr.append(element)
        spiltIndexArray[i] = arr
    return spiltIndexArray


# 使用已生成的根节点调用函数
def DHC(node, beta, V, leaf_nodes, DHCType):
    if node.dimension == 1 or len(V) < beta:
        leaf_nodes.append(node)
        return

    if DHCType == "LeftVDPS":
        splits = leftmost(V)
    elif DHCType == "RightVDPS":
        splits = rightmost(V,1)
    elif DHCType == "MinEntropy":
        splits = minEntropy(V)
    elif DHCType == "MaxCover":
        splits = maxcovering(V)

    for s in splits:
        data = V[s]
        dimension, subspace, density = init_subspace_by_seeds(data)
        currentSpace = "".join(map(str, subspace))
        if (currentSpace in allSpaceList) or dimension <= 0:
            continue
        allSpaceList.add(currentSpace)
        newNode = TreeNode(data, node)
        newNode.dimension = dimension
        newNode.subspace = subspace
        node.children.append(newNode)
        DHC(newNode, beta, data, leaf_nodes, DHCType)


def DHCWithArray(node, beta, V, leaf_nodes, spaceList, spiltArray):
    if node.dimension == 1 or len(V) < beta:
        leaf_nodes.append(node)
        return
    splits = rightmost(V, spiltArray[node.level])

    for s in splits:
        data = V[s]
        dimension, subspace, density = init_subspace_by_seeds(data)
        currentSpace = "".join(map(str, subspace))
        if (currentSpace in allSpaceList) or dimension <= 0:
            continue
        spaceList.append(currentSpace)
        allSpaceList.add(currentSpace)
        newNode = TreeNode(data, node)
        newNode.dimension = dimension
        newNode.subspace = subspace
        node.children.append(newNode)
        DHCWithArray(newNode, beta, data, leaf_nodes, spaceList, spiltArray)


def narrowDimension(leafNodes):
    lowDimPatterns = []
    for treeNode in leafNodes:
        arrs = treeNode.seeds
        parentNode = treeNode.parent
        if treeNode.size == 2:
            if seed_distance(arrs[0], arrs[1]) <= 2:
                if treeNode.dimension == 1:
                    lowDimPatterns.append(':'.join(''.join(treeNode.subspace[i:i + 4]) for i in range(0, 32, 4)))
            else:
                parentNode.remove_child_node(treeNode)
            continue
        parentNode.remove_child_node(treeNode)
        if treeNode.size == 1:
            continue
        Tarrs = arrs.T
        free_dimension_num = 0
        Weights = [0] * len(arrs)

        for i in range(32):
            splits = np.bincount(Tarrs[i], minlength=16)
            if np.count_nonzero(splits) == 1:
                continue
            free_dimension_num += 1
            IoslatedForest(Weights, splits, Tarrs[i])

        OutlierIndices = []
        for oW in Four_D(Weights):
            OutlierIndices.append(np.where(Weights == oW)[0][0])
        region = arrs[list(set(list(range(len(arrs)))) - set(OutlierIndices))]
        outlierDetect(treeNode, lowDimPatterns, region)
    return lowDimPatterns


def maxcovering(arrs):
    Tarrs = arrs.T
    Covering = []
    leftmost_index = -1
    leftmost_Covering = -1
    for i in range(32):
        splits = np.bincount(Tarrs[i], minlength=16)
        if np.count_nonzero(splits) == 1:
            # fixed dimension
            Covering.append(-1)
        else:
            if leftmost_index == -1:
                leftmost_index = i
                leftmost_Covering = np.sum(splits * (splits != 1))
            Covering.append(np.sum(splits * (splits != 1)))
    index = np.argmax(Covering)
    if np.max(Covering) - leftmost_Covering <= index - leftmost_index:
        index = leftmost_index
    splits = np.bincount(Tarrs[index], minlength=16)
    split_nibbles = np.argwhere(splits).reshape(-1)
    return [
        np.argwhere(Tarrs[index] == nibble).reshape(-1) for nibble in split_nibbles
    ]


def leftmost(arrs):
    Tarrs = arrs.T
    for i in range(32):
        splits = np.bincount(Tarrs[i], minlength=16)

        if len(splits[splits > 0]) > 1:
            split_index = i
            split_nibbles = np.where(splits != 0)[0]
            break
    return [
        np.where(Tarrs[split_index] == nibble)[0] for nibble in split_nibbles
    ]


def minEntropy(arrs):
    Tarrs = arrs.T
    minLeftEntropyIndex = -1
    minLeftEntropyValue = 17
    for i in range(32):
        splits = np.bincount(Tarrs[i], minlength=16)
        unique_elements, counts = np.unique(Tarrs[i], return_counts=True)
        if len(unique_elements) == 1:
            continue
        if len(unique_elements) == 2:
            minLeftEntropyIndex = i
            split_nibbles = np.where(splits != 0)[0]
            break
        elif len(unique_elements) < minLeftEntropyValue:
            minLeftEntropyValue = len(unique_elements)
            split_nibbles = np.where(splits != 0)[0]
            minLeftEntropyIndex = i

    return [
        np.argwhere(Tarrs[minLeftEntropyIndex] == nibble).reshape(-1) for nibble in split_nibbles
    ]


def rightmost(arrs, num=-1):
    if num > -1:
        a = num
    Tarrs = arrs.T
    for i in range(31, -1, -1):
        splits = np.bincount(Tarrs[i], minlength=16)

        if len(splits[splits > 0]) > 1:
            split_index = i
            split_nibbles = np.where(splits != 0)[0]
            a -= 1
            if a <= 0:
                break
    return [
        np.where(Tarrs[split_index] == nibble)[0] for nibble in split_nibbles
    ]


def init_subspace_by_seeds(activeSeeds):
    Tars = activeSeeds.T
    dimension = 0
    subspace = ['0'] * 32
    for i in range(32):
        a = np.unique(Tars[i])
        if len(a) > 1:
            dimension += 1
            subspace[i] = "*"
        else:
            subspace[i] = str(format(a[0], 'x'))
    density = len(activeSeeds) / pow(16, dimension)
    return dimension, subspace, density


def init_subspace(treeNode, activeSeeds):
    Tars = activeSeeds.T
    for i in range(32):
        a = np.unique(Tars[i])
        if len(a) > 1:
            treeNode.dimension += 1
            treeNode.subspace[i] = "*"
        else:
            treeNode.subspace[i] = str(format(a[0], 'x'))


def dealPatterns(treeNode, patterns, lowDimPatterns):
    parentNode = treeNode.parent
    for p in patterns:
        dimension, subspace, density = init_subspace_by_seeds(p)
        if dimension == 0 or dimension > 4:
            continue
        currentNodeSpace = ':'.join(''.join(subspace[i:i + 4]) for i in range(0, 32, 4))
        if currentNodeSpace in allLeafList:
            continue
        allLeafList.add(currentNodeSpace)
        newNode = TreeNode(p, treeNode.parent)
        newNode.dimension = dimension
        newNode.subspace = subspace
        parentNode.children.append(newNode)
        if dimension <= 3:
            lowDimPatterns.append(currentNodeSpace)
        else:
            if len(p) >= 3:
                lowDimPatterns.append(currentNodeSpace)


def outlierDetect(treeNode, lowDimPatterns, region):
    patterns = iter_devide(region)
    dealPatterns(treeNode, patterns, lowDimPatterns)


def seed_distance(a, b):
    return len(np.argwhere(a != b))


def IoslatedForest(Weights, splits, Tarr_i):
    OutlierNum = np.sum(splits == 1)

    # unique nibbles
    for j in np.argwhere(splits == 1).reshape(-1):
        outlier_index = np.argwhere(Tarr_i == j).reshape(-1)[0]
        Weights[outlier_index] += 1 / OutlierNum


def Four_D(Weights):
    if len(Weights) <= 2:
        return []
    OutLierIndex = np.argmax(Weights)

    OutRemovedWeights = list(Weights)
    OutRemovedWeights.remove(Weights[OutLierIndex])
    OutRemovedD = np.sqrt(np.var(OutRemovedWeights))
    OutRemovedAvg = np.average(OutRemovedWeights)

    if Weights[OutLierIndex] - OutRemovedAvg > 3 * OutRemovedD:
        return [Weights[OutLierIndex]] + Four_D(OutRemovedWeights)
    else:
        return []


def iter_devide(arrs):
    q = queue.LifoQueue()
    q.put(arrs)
    regions_arrs = []
    while not q.empty():
        arrs = q.get()
        splits = maxcovering(arrs)
        if 1 in [len(s) for s in splits]:
            regions_arrs.append(arrs)
        else:
            for s in splits:
                q.put(arrs[s])

    return regions_arrs


def iter_devide_All(arrs):
    q = queue.LifoQueue()
    q.put(arrs)
    regions_arrs = []
    while not q.empty():
        arrs = q.get()
        splits = rightmost(arrs,1)

        if 1 in [len(s) for s in splits]:
            regions_arrs.append(arrs)
        else:
            for s in splits:
                q.put(arrs[s])

    return regions_arrs


def trancAddress(address):
    hex_strings = ''.join([format(i, 'x') for i in address])
    return ipaddress.IPv6Address(int(hex_strings, 16)).compressed
