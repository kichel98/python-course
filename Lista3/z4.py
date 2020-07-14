def qsort(arr):
    if not arr:
        return arr
    head = arr[0]
    tail = arr[1:]
    elts_lt_x = list(filter(lambda num: num < head, tail))
    elts_greq_x = list(filter(lambda num: num >= head, tail))

    # elts_lt_x = [num for num in tail if num < head]
    # elts_greq_x = [num for num in tail if num >= head]

    return [*qsort(elts_lt_x), head, *qsort(elts_greq_x)]


print(qsort([7, 3, 8, 3, 6, 31, 5, 6, 2]))

