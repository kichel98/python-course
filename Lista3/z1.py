def transpose(matrix):
    splitted_mat = [row.split() for row in matrix]
    return [" ".join([splitted_mat[i][j] for i in range(len(splitted_mat))]) for j in range(len(splitted_mat))]


print(transpose(["1.1 2.2 3.3", "4.4 5.5 6.6", "7.7 8.8 9.9"]))
