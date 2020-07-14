def allsubsets(arr):
    if not arr:
        return [[]]
    else:
        a = arr[0]
        t = arr[1:]
        res = allsubsets(t)
        return list(map(lambda b: [a, *b], res)) + res
        # return [[a, *b] for b in res] + res


print(allsubsets([1, 2, 3]))
