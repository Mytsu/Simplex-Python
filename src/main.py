from json import JSONDecoder
from sys import argv
from typing import List

from matrix import Matrix
from simplex import Simplex
from solutions import interpretation


def read_file(file_name: str) -> (List[List[float]], List[float], List[float],
                                  List[int], str):
    with open(file_name) as file:
        json_string = file.read()
    return JSONDecoder().decode(json_string)


def main():

    if len(argv) > 1:
        file_name = argv[1]
    else:
        file_name = 'data/data.json'

    instance = read_file(file_name)
    coefficients = Matrix(data=instance['A'], byrow=instance['byrow'])
    simplex = Simplex(coefficients, instance['b'], instance['c'])
    simplex.run()

    interpretation(simplex, instance['vars'], instance['y'], instance['type'])


if __name__ == '__main__':
    main()
