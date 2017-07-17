#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Implement the code needed to solve sudoku puzzles

@author: Udacity, ucaiado

Created on 07/16/2017
"""


'''
Begin help functions and variables
'''


def cross(a, b):
    '''
    Cross product of elements in A and elements in B.
    '''
    return [s+t for s in a for t in b]

rows = 'ABCDEFGHI'
cols = '123456789'


boxes = cross(rows, cols)

row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC', 'DEF', 'GHI')
                for cs in ('123', '456', '789')]
unitlist = row_units + column_units + square_units
units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s], []))-set([s])) for s in boxes)

'''
end help functions and variables
'''

assignments = []


def assign_value(values, box, value):
    '''
    Update values dictionary. Assigns a value to a given box. If it updates
    the board record it.
    '''

    # Don't waste memory appending actions that don't actually change any val
    if values[box] == value:
        return values

    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values


def naked_twins(values):
    '''
    Eliminate values using the naked twins strategy.

    :param values: dict. a dict of the form {'box_name': '123456789', ...}
    :return: the values dictionary with the naked twins eliminated from peers.
    '''
    # constrain the search to the boxes than can be "twins"
    double_values = [box for box in values.keys() if len(values[box]) == 2]
    # Find all instances of naked twins
    for box in double_values:
        digit = values[box]
        for unit in units[box]:
            for peer in unit:
                if peer == box:
                    continue
                # check if the boxes have the same value
                if digit == values[peer]:
                    # the values are locked in those two boxes
                    for i_aux in digit:
                        # Eliminate the naked twins as possibilities for peers
                        # in the same unit
                        for peer2 in unit:
                            if (values[peer2] == digit):
                                continue
                            if (len(values[peer2]) < 2):
                                continue
                            values[peer2] = values[peer2].replace(i_aux, '')
    return values


def grid_values(grid):
    '''
    Convert grid into a dict of {square: char} with '123456789' for empties.

    :param grid. string. A grid in string form.
    :return: A grid in dictionary form
                Keys: The boxes, e.g., 'A1'
                Values: The value in each box, e.g., '8'. If the box has no
                    value, then the value will be '123456789'.
    '''
    chars = []
    digits = '123456789'
    for c in grid:
        if c in digits:
            chars.append(c)
        if c == '.':
            chars.append(digits)
    assert len(chars) == 81
    return dict(zip(boxes, chars))


def display(values):
    '''
    Display the values as a 2-D grid.

    :param values: dict. The sudoku in dictionary form
    '''
    width = 1+max(len(values[s]) for s in boxes)
    line = '+'.join(['-'*(width*3)]*3)
    for r in rows:
        print(''.join(values[r+c].center(width)+('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF':
            print(line)
    return


def eliminate(values):
    '''
    Go through all the boxes, and whenever there is a box with a value,
    eliminate this value from the values of all its peers.

    :param values: dict. The sudoku in dictionary form
    :return: The resulting sudoku in dictionary form.
    '''
    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    for box in solved_values:
        digit = values[box]
        for peer in peers[box]:
            values[peer] = values[peer].replace(digit, '')
    return values


def only_choice(values):
    '''
    Go through all the units, and whenever there is a unit with a value that
    only fits in one box, assign the value to this box.

    :param values: dict. A sudoku in dictionary form.
    :return The resulting sudoku in dictionary form.
    '''
    for unit in unitlist:
        for digit in '123456789':
            dplaces = [box for box in unit if digit in values[box]]
            if len(dplaces) == 1:
                values[dplaces[0]] = digit
    return values


def reduce_puzzle(values):
    '''
    Iterate eliminate() and only_choice(). If at some point, there is a box
    with no available values, return False. If the sudoku is solved, return the
    sudoku. If after an iteration of both functions, the sudoku remains the
    same, return the sudoku.

    :param values: dict. A sudoku in dictionary form.
    :return The resulting sudoku in dictionary form.
    '''
    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    stalled = False
    while not stalled:
        solved_values_before = len([box for box in values.keys()
                                    if len(values[box]) == 1])
        values = eliminate(values)
        values = only_choice(values)
        solved_values_after = len([box for box in values.keys() if
                                   len(values[box]) == 1])
        stalled = solved_values_before == solved_values_after
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values


def search(values):
    '''
    Using depth-first search and propagation, try all possible values.

    :param values: dict. A sudoku in dictionary form.
    '''
    # First, reduce the puzzle using the previous function
    values = reduce_puzzle(values)
    if values is False:
        return False  # Failed earlier
    if all(len(values[s]) == 1 for s in boxes):
        return values  # Solved!
    # Choose one of the unfilled squares with the fewest possibilities
    n, s = min((len(values[s]), s) for s in boxes if len(values[s]) > 1)
    # Now use recurrence to solve each one of the resulting sudokus, and
    for value in values[s]:
        new_sudoku = values.copy()
        new_sudoku[s] = value
        attempt = search(new_sudoku)
        if attempt:
            return attempt


def solve(grid):
    '''
    Find the solution to a Sudoku grid.

    :param grid: string. a string representing a sudoku grid.
        Example: '2.............62....1....7...6..8...3...9...7...6..4...4....
                  8....52.............3'
    :return: The dictionary representation of the final sudoku grid. False if
        no solution exists.
    '''
    values = grid_values(grid)
    return search(values)

if __name__ == '__main__':
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4..'
    diag_sudoku_grid += '.4....8....52.............3'
    display(solve(diag_sudoku_grid))

    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        s_err = 'We could not visualize your board due to a pygame issue. Not'
        s_err += ' a problem! It is not a requirement.'
        print(s_err)
