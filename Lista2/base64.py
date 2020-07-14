import argparse
import textwrap
from bitstring import BitArray


def set_parser():
    parser = argparse.ArgumentParser(description="Zamiana pliku binarnego na base64 i odwrotnie")
    type_group = parser.add_mutually_exclusive_group(required=True)
    type_group.add_argument("--encode", help="Tryb kodowania", action="store_true")
    type_group.add_argument("--decode", help="Tryb dekodowania", action="store_true")
    parser.add_argument("inputfile", help="Plik wejściowy")
    parser.add_argument("outputfile", help="Plik wyjściowy")

    return parser


def convert_bytes_to_text(chunk, mapping):
    padding_symbol = "="
    output = []

    binary_string = BitArray(hex=chunk.hex()).bin
    # binary_string = "{0:8b}".format(int(chunk.hex(), 16))
    sextets = textwrap.wrap(binary_string, 6)
    if len(sextets[-1]) < 6:
        sextets[-1] = sextets[-1].ljust(6, "0")
    for sextet in sextets:
        decimal_val = int(sextet, 2)
        output.append(mapping[decimal_val])
    output.append(padding_symbol * (4 - len(sextets)))

    return output


def convert_text_to_bytes(chunk, mapping):
    padding_symbol = "="
    output = []

    chunk = chunk.replace(padding_symbol, "")
    binary_string = "".join(["{0:06b}".format(mapping[char]) for char in chunk])
    octets = list(map(''.join, zip(*[iter(binary_string)]*8)))
    for octet in octets:
        output.append(int(octet, 2))
    return output


def encode(filename, mapping):
    chunk_size = 3
    output_list = []

    with open(filename, "rb") as f:
        chunk = f.read(chunk_size)
        while len(chunk) != 0:
            output_list.extend(convert_bytes_to_text(chunk, mapping))

            chunk = f.read(chunk_size)

    return "".join(output_list)


def decode(filename, mapping):
    chunk_size = 4
    output_list = bytearray()

    with open(filename, "r") as f:
        chunk = f.read(chunk_size)
        while len(chunk) != 0:
            output_list.extend(convert_text_to_bytes(chunk, mapping))
            chunk = f.read(chunk_size)

    return output_list


def write_output_to_file(filename, output, binary_file):
    mode = "wb" if binary_file else "w"
    with open(filename, mode) as f:
        f.write(output)


def base64():
    parser = set_parser()
    args = parser.parse_args()

    mapping_array = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"
    reversed_map = {v: i for i, v in enumerate(mapping_array)}

    try:
        if args.encode:
            output = encode(args.inputfile, mapping_array)
            write_output_to_file(args.outputfile, output, binary_file=False)
        else:
            output = decode(args.inputfile, reversed_map)
            write_output_to_file(args.outputfile, output, binary_file=True)
    except FileNotFoundError:
        print('Plik nie istnieje')


if __name__ == "__main__":
    base64()
