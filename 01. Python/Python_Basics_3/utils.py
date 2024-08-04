#Return unique sorted items only #Remove duplicates, filter odd and sort 
def returnSortedEven(lst):
    maxNum = max(lst)
    return_set = set(range(1,maxNum+1,2))
    print(return_set)
    return sorted(list(return_set.intersection(lst)))

def returnSortedEvenfor(lst):
    newlist = []
    for i in lst: 
        if i%2 == 0:
            newlist.append(i)
    newlist.sort()
    return newlist

def dummy():
    print("Dummy")