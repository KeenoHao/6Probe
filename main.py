import numpy as np

from Construct6ASForest import construct6ASForest, construct6ASTree

if __name__ == '__main__':
    # 读取种子地址数据
    data = np.load("./seeds.npy")
    # 构造6ASForest，并生成低维度地址模式
    construct6ASForest(data)
    # 使用 GenerateAddress{https://github.com/KeenoHao/GenerateAddress.git}工具快速生成地址

    # # construct6ASTree(data,"LeftVDPS","lowDimLeftVDPS")
    # # construct6ASTree(data, "RightVDPS", "lowDimRightVDPS")
    # # construct6ASTree(data, "MaxCover", "lowDimMaxCover")
    # construct6ASTree(data, "MinEntropy", "lowDimMinEntropy")


