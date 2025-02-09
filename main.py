import numpy as np

from Construct6ASForest import construct6ASForest, construct6ASTree

if __name__ == '__main__':
    # Read the seed address data
    data = np.load("./seeds.npy")
    # Construct the 6ASForest and generate low-dimensional pattern
    construct6ASForest(data,"lowDimPatterns",40)
    # Use the generate target address tool{https://github.com/KeenoHao/GenerateAddress.git} to quickly generate addresses.

    # # construct6ASTree(data,"LeftVDPS","lowDimLeftVDPS")
    # # construct6ASTree(data, "RightVDPS", "lowDimRightVDPS")
    # # construct6ASTree(data, "MaxCover", "lowDimMaxCover")
    # construct6ASTree(data, "MinEntropy", "lowDimMinEntropy")


