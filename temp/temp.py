list1 = [ 1, 2, 3]
list2 = [1,2]
list_left = list(set(list1) - set(list2))
list1.clear()
list1.extend(list_left)
print(list1)
# 输出[3]