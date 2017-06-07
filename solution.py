assignments = []
ROWS = 'ABCDEFGHI'
COLS = '123456789'

def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """

    # Don't waste memory appending actions that don't actually change any values
    if values[box] == value:
        return values

    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values

def naked_twins(values):
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """

    # Find all instances of naked twins
    # Eliminate the naked twins as possibilities for their peers

def cross(A, B):
    '''Combinations of concatenations of all the strings in a list of strings.'''
    return [a+b for a, b in A, B]

boxes = cross(ROWS, COLS)

def grid_values(grid_string):
    """
    Convert grid into a dict of {square: char} with '123456789' for empties.
    Args:
        grid_string - A grid in string form.
    Returns:
        A grid in dictionary form
            Keys: The boxes, e.g., 'A1'
            Values: The value in each box, e.g., '8'. If the box has no value, then the value will be '123456789'.
    """
    values = []
    all_digits = '123456789'
    for c in grid_string:
        if c == '.':
            values.append(all_digits)
        elif c in all_digits:
            values.append(c)
    return dict(zip(boxes, grid_string))

def display(values):
    """
    Display the values as a 2-D grid.
    Args:
        values(dict): The sudoku in dictionary form
    """
    # Allocate space for each cell in the Sudoku
    width = 1 + max(len(values[s]) for s in boxes)

    # Multiply the width by 3
    # Take three of these
    # Add '+'s in between them
    line = '+'.join(['-'*(width*3)]*3)

    # For each row and column in the data:
    # Print the value in that cell
    # Center it (https://www.tutorialspoint.com/python/string_center.htm)
    # Add "|" if the string is in column 3 or 6.
    # Print a "line" if the current row is the third or sixth
    for r in rows:
        print(''.join(values[r+c].center(width)+('|' if c in '36' else '')
            for c in cols))
        if r in 'CF': print(line)
    return

# Define three lists of lists, each of which contains 9 lists:
# * The first has each row's units in each list
# * The second has each column's units in each list
# * The third has each box's units in each list
ROW_UNITS = [cross(r, cols) for r in rows]
COLUMN_UNITS = [cross(rows, c) for c in cols]
SQUARE_UNITS = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]
UNIT_LIST = ROW_UNITS + COLUMN_UNITS + SQUARE_UNITS

def eliminate(values):
    pass

def only_choice(values):
    pass

def reduce_puzzle(values):
    pass

def search(values):
    pass

def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """
    return dict(zip(boxes, grid))

if __name__ == '__main__':
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    display(solve(diag_sudoku_grid))

    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
