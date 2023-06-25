# 注意：python 代码由 chatGPT🤖 根据我的 java 代码翻译，旨在帮助不同背景的读者理解算法逻辑。
# 本代码还未经过力扣测试，仅供参考，如有疑惑，可以参照我写的 java 代码对比查看。
# heapq.heappush(heap, item)
# 将 item 的值加入 heap 中，保持堆的不变性。

# heapq.heappop(heap)
# 弹出并返回 heap 的最小的元素，保持堆的不变性。如果堆为空，抛出 IndexError 。使用 heap[0] ，可以只访问最小的元素而不弹出它。

# heapq.heappushpop(heap, item)
# 将 item 放入堆中，然后弹出并返回 heap 的最小元素。该组合操作比先调用 heappush() 再调用 heappop() 运行起来更有效率。

# heapq.heapify(x)
# 将list x 转换成堆，原地，线性时间内。

# heapq.heapreplace(heap, item)
# 弹出并返回 heap 中最小的一项，同时推入新的 item。 堆的大小不变。 如果堆为空则引发 IndexError。

# 这个单步骤操作比 heappop() 加 heappush() 更高效，并且在使用固定大小的堆时更为适宜。 pop/push 组合总是会从堆中返回一个元素并将其替换为 item。

# 返回的值可能会比添加的 item 更大。 如果不希望如此，可考虑改用 heappushpop()。 它的 push/pop 组合会返回两个值中较小的一个，将较大的值留在堆中。

# 该模块还提供了三个基于堆的通用功能函数。

# heapq.merge(*iterables, key=None, reverse=False)
# 将多个已排序的输入合并为一个已排序的输出（例如，合并来自多个日志文件的带时间戳的条目）。 返回已排序值的 iterator。

# 类似于 sorted(itertools.chain(*iterables)) 但返回一个可迭代对象，不会一次性地将数据全部放入内存，并假定每个输入流都是已排序的（从小到大）。

# 具有两个可选参数，它们都必须指定为关键字参数。

# key 指定带有单个参数的 key function，用于从每个输入元素中提取比较键。 默认值为 None (直接比较元素)。

# reverse 为一个布尔值。 如果设为 True，则输入元素将按比较结果逆序进行合并。 要达成与 sorted(itertools.chain(*iterables), reverse=True) 类似的行为，所有可迭代对象必须是已从大到小排序的。

# 在 3.5 版更改: 添加了可选的 key 和 reverse 形参。

# heapq.nlargest(n, iterable, key=None)
# 从 iterable 所定义的数据集中返回前 n 个最大元素组成的列表。 如果提供了 key 则其应指定一个单参数的函数，用于从 iterable 的每个元素中提取比较键 (例如 key=str.lower)。 等价于: sorted(iterable, key=key, reverse=True)[:n]。

# heapq.nsmallest(n, iterable, key=None)
# 从 iterable 所定义的数据集中返回前 n 个最小元素组成的列表。 如果提供了 key 则其应指定一个单参数的函数，用于从 iterable 的每个元素中提取比较键 (例如 key=str.lower)。 等价于: sorted(iterable, key=key)[:n]。

# 后两个函数在 n 值较小时性能最好。 对于更大的值，使用 sorted() 函数会更有效率。 此外，当 n==1 时，使用内置的 min() 和 max() 函数会更有效率。 如果需要重复使用这些函数，请考虑将可迭代对象转为真正的堆。
from typing import List
import heapq
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

def mergeTwoLists(l1: ListNode, l2: ListNode) -> ListNode:
    # 合并两链表
    # 虚拟头结点
    dummy = ListNode(-1)
    p = dummy
    p1 = l1
    p2 = l2

    while p1 and p2: 
        # 比较 p1 和 p2 两个指针
        # 将值较小的的节点接到 p 指针
        if p1.val > p2.val:
            p.next = p2
            p2 = p2.next
        else:
            p.next = p1
            p1 = p1.next
        # p 指针不断前进
        p = p.next

    if p1:
        p.next = p1

    if p2:
        p.next = p2

    return dummy.next

def mergeKLists(lists: List[ListNode]) -> ListNode:
    if not lists:
        return None
    # 虚拟头结点
    dummy = ListNode(-1)
    p = dummy
    # 优先级队列，最小堆
    pq = []
    for head in lists:
        if head:
            #todo 列表
            heapq.heappush(pq, (head.val, head))

    while pq:
        # 获取最小节点，接到结果链表中
        node = heapq.heappop(pq)[1]
        p.next = node
        if node.next:#如果这条虫子还有尾巴就加进来 value和node都要
            heapq.heappush(pq, (node.next.val, node.next))
        # p 指针不断前进
        p = p.next
        # 有点类似层序遍历
    return dummy.next
def count(val):
    zerosum=0
    while val:
        if val%10 == 0:
            zerosum+=1
            val=val//10
        else:
            break
    return val,zerosum

if __name__ =='__main__':
    lists = [[1,4,5],[1,3,4],[2,6]]
    # mergeKLists
    print(count(4))
    n=10
    choices = [x for x in reversed(range(1,n+1))]
    print(choices)