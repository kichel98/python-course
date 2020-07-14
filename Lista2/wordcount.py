import sys


def read_file(filename, encoding="utf-8"):
    with open(filename, "r", encoding=encoding) as file:
        data = file.read()
        return data


def count_text_stats(data, encoding="utf-8"):
    bytes_count = len(bytes(data, encoding=encoding))

    lines = data.split("\n")
    lines_count = len(lines)
    max_line = len(max(lines, key=len))

    words_count = 0
    for line in lines:
        words_count += len(line.split())

    return bytes_count, words_count, lines_count, max_line


def main():
    if len(sys.argv) > 1:
        try:
            data = read_file(sys.argv[1])
        except FileNotFoundError:
            print("Plik nie istnieje")
        else:
            bytes_count, words_count, lines_count, max_line = count_text_stats(data)
            print("liczba bajtów:", bytes_count)
            print("liczba słów:", words_count)
            print("liczba linii:", lines_count)
            print("maksymalna długość linii:", max_line)
    else:
        print("Usage: python wordcount.py filename.txt")


main()
