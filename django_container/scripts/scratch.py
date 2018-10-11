from __future__ import annotations
import itertools
import os
from collections import Iterable


class Cell(object):

    def __init__(self, x: int, y: int):
        self._x = x
        self._y = y

    @property
    def right(self) -> Cell:
        return Cell(self.x + 1, self.y)

    @property
    def left(self) -> Cell:
        return Cell(self.x - 1, self.y)

    @property
    def up(self) -> Cell:
        return Cell(self.x, self.y - 1)

    @property
    def down(self) -> Cell:
        return Cell(self.x, self.y + 1)

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash(self.x) ^ hash(self.y)

    def __repr__(self):
        return '<%s, %s>' % (self.x, self.y)


class Room(object):

    def __init__(self, matrix: [str]):
        self._matrix = matrix
        self._width = len(self._matrix[0])
        self._height = len(self._matrix)

    @property
    def width(self) -> int:
        return self._width

    @property
    def height(self) -> int:
        return self._height

    def find_locations(self, flag) -> [Cell]:
        for count, line in enumerate(self._matrix):
            x_coords = find_positions(flag, line)
            cells = map(tuple, itertools.product(x_coords, [count]))
            for cell in cells:
                yield Cell(cell[0], cell[1])

    def contains(self, cell: Cell) -> bool:
        return 0 <= cell.x < self.width and 0 <= cell.y < self.height

    def explore(self, from_cell: Cell, targets: [Cell], walls: [Cell], already_explored: [Cell]):
        if from_cell in already_explored or not self.contains(from_cell) or from_cell in walls:
            already_explored.add(from_cell)
            return False

        elif self.contains(from_cell) and from_cell in targets:
            already_explored.add(from_cell)
            print('target reached: %s' % from_cell)
            return True

        else:
            print('exploring cell %s' % from_cell)
            already_explored.add(from_cell)
            res1 = self.explore(from_cell.left, targets, walls, already_explored)
            res2 = self.explore(from_cell.right, targets, walls, already_explored)
            res3 = self.explore(from_cell.up, targets, walls, already_explored)
            res4 = self.explore(from_cell.down, targets, walls, already_explored)
            return res1 or res2 or res3 or res4

    def exists_path(self, starts: Iterable[Cell], targets: Iterable[Cell], walls: [Cell]) -> bool:
        print('walls: %s' % str(walls))
        for from_cell in list(starts):
            print()
            print('trying from cell %s' % str(from_cell))
            if self.explore(from_cell, list(targets), list(walls), set()):
                return True

        return False

    def __repr__(self):
        return os.linesep.join(self._matrix)


def find_positions(delimiter, line):
    """
    >>> print(find_positions('x', '01234x67x9'))
    [5, 8]
    >>> print(find_positions('x', '0x234x67xx'))
    [1, 5, 8, 9]
    >>> print(find_positions('x', 'xxxxxxxxxx'))
    [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    >>> print(find_positions('x', '0123456789'))
    []
    """
    sections = line.split(delimiter)

    def decrease(x):
        return x - 1

    def len_plus_1(x):
        return len(x) + 1

    return list(map(decrease, itertools.accumulate(map(len_plus_1, sections))))[:-1]


def powerset(iterable):
    """
    >>> powerset([1,2,3])
    () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)

   : param iterable:
   : return:
    """
    s = list(iterable)
    sets = (itertools.combinations(s, r) for r in range(len(s) + 1))
    return itertools.chain.from_iterable(sets)


def run(*args):
    print(find_positions('x', '01234x67x9'))
    print(find_positions('x', '0x234x67xx'))
    print(find_positions('x', 'xxxxxxxxxx'))
    print(find_positions('x', '0123456789'))

    room_desc = [
        '.?.#.?.',
        'P#.#.#C',
        '.#.#.#.',
        '##.?.##',
        '.#.#.#.',
        'P#.#.#C',
        '.?.#.?.',
    ]

    room = Room(room_desc)
    starts = list(room.find_locations('P'))
    targets = list(room.find_locations('C'))
    walls = list(room.find_locations('#'))
    doors = list(room.find_locations('?'))
    print('starts: %s' % str(starts))
    print('targets: %s' % str(targets))
    print('walls: %s' % str(walls))
    print('doors: %s' % str(doors))

    print(room)

    success = False
    alternatives = powerset(doors)
    for closed_doors in alternatives:
        print()
        print('---------------------------------------')
        print('closed doors: %s' % str(closed_doors))
        print()
        success = not room.exists_path(starts, targets, walls + list(closed_doors))
        if success:
            print('targets not reachable from starting points when closing doors: %s' % str(closed_doors))
            break

    if not success:
        print('targets always reachable from starting points')
