# 6Probe

This is a demo for IPv6 target generation based on seed addresses (active addresses). Its idea is introduced in the paper [An IPv6 Target Generation Approach Based on Address Space Forest](https://doi.org/10.1038/s41598-025-97640-w).



## Preparation Work

#### Environment

```
1. python 3.8 or higher version
2. numpy 2.2.2 or higher version
3. IPy 1.1 or higher version
```

#### Seed Address Preprocessing

1. Download seed address source Hitlist

   ```
   curl https://alcatraz.net.in.tum.de/ipv6-hitlist-service/open/responsive-addresses.txt.xz    --output responsive-addresses.txt.xz 
   xz -d responsive-addresses.txt.xz
   ```

2.  Construct seed set.

   A subset of addresses is sampled from the Hitlist through down-sampling to create a machine-readable seed set.

   ```
   sort responsive-addresses.txt > responsive-addressesSort
   shuf -n 100000(the number of seed addresses in seed set) responsive-addressesSort > seedSet
   ```

3. Format seed address.

   Convert IPv6 seeds in seed set to 32-dimensional vectors. 

   ```
   python convert.py
   ```



## 6ASForest Construction

Read IPv6 addresses from the seed set, cluster them, construct a 6ASForest, and generate low-dimensional patterns.

```
python main.py
```



## Post-Processing Work

#### IPv6 Target Address Generation

Use [Generate target address tool](https://github.com/KeenoHao/GenerateAddress.git) to quickly generate addresses.

```
 ./GenerateAddress -i lowDimPatternFile -o targetAddressFile
```

#### Probe

Under a 30Mbps bandwidth, utilize the asynchronous scanning tool [ZMap](https://github.com/tumi8/zmap) to scan IPv6 target addresses and collect responsive IPv6 active addresses.

```
sudo zmap --probe-module=icmp6_echoscan --ipv6-target-file=targetAddressFile  --output-file=activeAddressFile --ipv6-source-ip=(Machine IPv6 address) --bandwidth=30M --cooldown-time=4
```



## Reference

### Scanner

```
Durumeric, Z., Wustrow, E. & Halderman, J. A. ZMap: Fast Internet-wide scanning and its security applications. In 22nd
USENIX Security Symposium (USENIX Security 13), 605–620 (2013). https://www.usenix.org/conference/usenixsecurity13/
technical-sessions/paper/durumeric.

ZMap. ZMap Github code. https://github.com/tumi8/zmap.
```

### IPv6 Target Generation Algorithms

```

Murdock, A., Li, F., Bramsen, P., Durumeric, Z. & Paxson, V. Target generation for Internet-wide IPv6 scanning. In
Proceedings ofthe 2017 Internet Measurement Conference, 242–253, DOI: 10.1145/3131365.3131405 (2017).

Liu, Z., Xiong, Y., Liu, X., Xie, W. & Zhu, P. 6Tree: Efficient dynamic discovery of active addresses in the IPv6 address
space. Comput. Networks 155, 31–46, DOI: 10.1016/j.comnet.2019.03.010 (2019).

Hou, B., Cai, Z., Wu, K., Su, J. & Xiong, Y. 6Hit: A reinforcement learning-based approach to target generation for
Internet-wide IPv6 scanning. In IEEE INFOCOM 2021-IEEE Conference on Computer Communications, 1–10, DOI:
10.1109/INFOCOM42981.2021.9488794 (2021).

Yang, T., Cai, Z., Hou, B. & Zhou, T. 6Forest: An ensemble learning-based approach to target generation for Internet-
wide IPv6 scanning. In IEEE INFOCOM 2022-IEEE Conference on Computer Communications, 1679–1688, DOI:
10.1109/INFOCOM48880.2022.9796925 (2022).

Hou, B., Cai, Z., Wu, K., Yang, T. & Zhou, T. Search in the expanse: Towards active and global IPv6 hitlists. In IEEE
INFOCOM 2023-IEEE Conference on Computer Communications, 1–10, DOI: 10.1109/INFOCOM53939.2023.10229089
(2023).

Hou, B., Cai, Z., Wu, K., Yang, T. & Zhou, T. 6Scan: A high-efficiency dynamic Internet-wide IPv6 scanner with regional
encoding. IEEE/ACMTransactions on Netw. 31, 1870–1885, DOI: 10.1109/TNET.2023.3233953 (2023).

6Scan. 6Scan github code. https://github.com/hbn1987/6Scan.git.

Generate target address tool. https://github.com/KeenoHao/GenerateAddress.git.
```

### Hitlists & Aliases

```
O. Gasser et al., “Clusters in the Expanse: Understanding and Unbiasing IPv6 Hitlists,” in IMC, 2018.

Hitlist. Hitlist data. https://alcatraz.net.in.tum.de/ipv6-hitlist-service/open/responsive-addresses.txt.xz

Aliases. Aliases data. https://alcatraz.net.in.tum.de/ipv6-hitlist-service/open/aliased-prefixes.txt.xz

Longest prefix matching for aliased prefixes. Longest prefix matching for aliased prefixes github code. https://ipv6hitlist.github.io/lpm/aliases-lpm.py
```

## Cite

If the code is helpful in your work, please cite our paper:

```
@article{hao2025ipv6,
  title={An IPv6 target generation approach based on address space forest},
  author={Hao, Shunlong and Zhang, Liancheng and Zhang, Hongtao and Cheng, Lanxin and Guo, Yi and Li, Zhanbo and Lin, Bin and Zhu, Haojie and Ren, Mingyue and Zhang, Lanyun},
  journal={Scientific Reports},
  volume={15},
  number={1},
  pages={13933},
  year={2025},
  publisher={Nature Publishing Group UK London}
}
```


