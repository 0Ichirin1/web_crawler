# 单链表的节点 存储两个信息: 数据内容和指针
class ListNode:
    def __init__(self, val):
        self.val = val
        self.next = None

# 反转单链表
class Solution:
    def reverse(self, head):
        prev = None
        current = head
        while current:
            middle, current.next = current.next, prev
            prev, current = current, middle
        return prev


first_node = ListNode('A')
second_node = ListNode('B')
third_node = ListNode('C')
first_node.next = second_node
second_node.next = third_node
print(first_node.val, first_node.next.val, first_node.next.next.val)

solution = Solution()
res = solution.reverse(first_node)
print(res.val, res.next.val, res.next.next.val)
