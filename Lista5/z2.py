# author: Piotr Andrzejewski
import csv
import numpy as np


def read_matrix(users_last_id, movie_last_id):
    matrix = np.zeros((users_last_id + 1, movie_last_id + 1))
    with open("ml-latest-small/ratings.csv", encoding="utf-8") as ratings_file:
        reader = csv.reader(ratings_file)
        next(reader)
        for row in reader:
            user_id = int(row[0])
            movie_id = int(row[1])
            rating = float(row[2])
            if movie_id <= movie_last_id:
                matrix[user_id][movie_id] = rating
    return matrix


def read_movies(movie_last_id):
    movie_id_name = {}
    with open("ml-latest-small/movies.csv", encoding="utf-8") as movies_file:
        reader = csv.reader(movies_file)
        next(reader)
        for row in reader:
            movie_id = int(row[0])
            title = row[1]
            if movie_id > movie_last_id:
                break
            movie_id_name[movie_id] = title
    return movie_id_name


def read_data():
    users_last_id = 610
    movie_last_id = 9018
    matrix = read_matrix(users_last_id, movie_last_id)
    movie_names = read_movies(movie_last_id)
    return matrix, movie_names


def calculate_recommendations(matrix, user_ratings):
    norm_matrix = matrix / np.linalg.norm(matrix, axis=0)
    norm_matrix = np.nan_to_num(norm_matrix)
    norm_user_ratings = user_ratings / np.linalg.norm(user_ratings)
    norm_user_ratings = np.nan_to_num(norm_user_ratings)
    user_profile = np.dot(norm_matrix, norm_user_ratings)
    norm_user_profile = user_profile / np.linalg.norm(user_profile)
    result = np.dot(norm_matrix.T, norm_user_profile)
    return result, np.argsort(result, axis=0)[::-1]


def get_example_ratings():
    my_ratings = np.zeros((9019, 1))
    my_ratings[2571] = 5  # patrz movies.csv  2571 - Matrix
    my_ratings[32] = 4  # 32 - Twelve Monkeys
    my_ratings[260] = 5  # 260 - Star Wars IV
    my_ratings[1097] = 4
    return my_ratings


def main():
    matrix, movie_names = read_data()
    my_ratings = get_example_ratings()
    recomm_values, recomm_indices = calculate_recommendations(matrix, my_ratings)
    print("(cos(θ), movies_id), movie_name")
    for idx in recomm_indices.ravel()[:20]:
        similarity = recomm_values[idx][0]
        if similarity == 0.0:
            break
        print(f"({similarity}, {idx}), {movie_names[idx]}")


if __name__ == "__main__":
    main()
