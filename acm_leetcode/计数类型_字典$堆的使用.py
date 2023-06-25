class Solution:
    def canConstruct(self, ransomNote: str, magazine: str) -> bool:

        arr = [0] * 26

        for x in magazine:
            #todo 1. ord()返回字符的ascii
            arr[ord(x) - ord('a')] += 1

        for x in ransomNote:
            if arr[ord(x) - ord('a')] == 0:
                return False
            else:
                arr[ord(x) - ord('a')] -= 1
        
        return True

    def canConstruct01(self, ransomNote: str, magazine: str) -> bool:

        #todo 2. 哈希表 （默认字典） defaultdict
        from collections import defaultdict
        hashmap = defaultdict(int)

        for x in magazine:
            hashmap[x] += 1

        for x in ransomNote:
            value = hashmap.get(x)
            if value is None or value == 0:
                return False
            else:
                hashmap[x] -= 1

        return True
    # 查找第一个字符
    def firstUniqChar(self, s: str) -> int:
        #todo 3. 计数器 统计每个出现的频率
        from collections import Counter
        cnt = Counter(s)
        for idx, ch in enumerate(s):
            if cnt[ch] == 1:
                return idx
        return -1

from typing import List
import heapq

class Solution:
    def topKFrequent(self, words: List[str], k: int) -> List[str]:
        # 字符串 -> 该字符串出现的频率
        wordToFreq = {}
        for word in words:
            wordToFreq[word] = wordToFreq.get(word, 0) + 1
        pq = []
        for word, freq in wordToFreq.items():
            # todo 存储负值，让小根堆变成大根堆
            pq.append((-freq, word))
        # 构建小根堆
        heapq.heapify(pq)
        # 取出前k个高频单词
        res = []
        for _ in range(k):
            freq, word = heapq.heappop(pq)
            res.append(word)

        return res