# author: Piotr Andrzejewski

import csv
import numpy as np
import matplotlib.pyplot as plt


def read_toy_story_users_and_ratings():
    user_ids = []
    ratings = []
    with open("ml-latest-small/ratings.csv", encoding="utf-8") as ratings_file:
        reader = csv.reader(ratings_file)
        toy_story_id = 1
        next(reader)  # ignore header
        for entry in reader:
            if int(entry[1]) == toy_story_id:
                user_ids.append(int(entry[0]))
                ratings.append(float(entry[2]))
    return user_ids, ratings


def read_movie_ids_less_than_m(m):
    movie_ids = []
    with open("ml-latest-small/movies.csv", encoding="utf-8") as movies_file:
        reader = csv.reader(movies_file)
        next(reader)  # ignore header
        for row in reader:
            movie_id = int(row[0])
            if movie_id != 1 and movie_id <= m:
                movie_ids.append(movie_id)
    return movie_ids


def create_ratings_matrix(user_ids, movie_ids):
    matrix = np.zeros((len(user_ids), len(movie_ids)))
    with open("ml-latest-small/ratings.csv", encoding="utf-8") as ratings_file:
        reader = csv.reader(ratings_file)
        next(reader)  # ignore header
        for entry in reader:
            user_id = int(entry[0])
            movie_id = int(entry[1])
            try:
                user_index = user_ids.index(user_id)
                movie_index = movie_ids.index(movie_id)
            except ValueError:
                user_index = -1
                movie_index = -1
            if user_index != -1 and movie_index != -1:
                matrix[user_index][movie_index] = float(entry[2])
    return matrix


def read_data(m):
    user_ids, toy_story_ratings = read_toy_story_users_and_ratings()
    movie_ids = read_movie_ids_less_than_m(m)
    matrix = create_ratings_matrix(user_ids, movie_ids)

    return user_ids, matrix, np.array(toy_story_ratings).reshape(len(toy_story_ratings), 1)


def linear_regression(A, y):
    A = np.append(A, np.ones((A.shape[0], 1)), axis=1)
    return np.linalg.lstsq(A, y, rcond=None)[0]


def predict(A, x):
    A = np.append(A, np.ones((A.shape[0], 1)), axis=1)
    return np.dot(A, x)


def draw_plot(user_ids, A, y, x, idx, m):
    predicted_values = predict(A, x)
    errors = np.absolute(predicted_values - y)
    plt.figure(idx + 1)
    plt.title(f"m = {m}")
    plt.plot(user_ids, errors, 'r', label="Błąd")
    plt.xlabel("N-ty użytkownik")
    plt.ylabel("Błąd")


def main():
    for idx, m in enumerate([10, 1000, 10000]):
        user_ids, A, y = read_data(m)
        x = linear_regression(A, y)
        draw_plot(user_ids, A, y, x, idx, m)
    plt.show()


if __name__ == "__main__":
    main()
