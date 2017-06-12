assignments = []
ROWS = 'ABCDEFGHI'
COLS = '123456789'

def cross(A, B):
    '''Combinations of concatenations of all the strings in a list of strings.'''
    return [s+t for s in A for t in B]

boxes = cross(ROWS, COLS)
print(boxes)

# Define three lists of lists, each of which contains 9 lists:
# * The first has each row's units in each list
# * The second has each column's units in each list
# * The third has each box's units in each list
ROW_UNITS = [cross(r, COLS) for r in ROWS]
COLUMN_UNITS = [cross(ROWS, c) for c in COLS]
SQUARE_UNITS = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]
UNIT_LIST = ROW_UNITS + COLUMN_UNITS + SQUARE_UNITS

# Creating the new "diagonal" units.
diag_list_1 = []
for i in range(len(ROWS)):
    diag_list_1.append(ROWS[i] + COLS[i])
diag_list_2 = []
for i in range(len(ROWS)):
    diag_list_2.append(ROWS[i] + COLS[::-1][i])
unitlist_diag = UNIT_LIST + [diag_list_1] + [diag_list_2]

# Creating the "peers" dictionary
units_diag = dict((s, [u for u in unitlist_diag if s in u]) for s in boxes)
peers_diag = dict((s, set(sum(units_diag[s],[]))-set([s])) for s in boxes)


# def assign_value(values, box, value):
#     """
#     Please use this function to update your values dictionary!
#     Assigns a value to a given box. If it updates the board record it.
#     """
#
#     # Don't waste memory appending actions that don't actually change any values
#     if values[box] == value:
#         return values
#
#     values[box] = value
#     if len(value) == 1:
#         assignments.append(values.copy())
#     return values


def grid_values(grid_string, blanks='.'):
    """
    Convert grid into a dict of {square: char} with '123456789' for empties.
    Args:
        grid_string - A grid in string form.
        blanks - what string to fill in the blanks with
    Returns:
        A grid in dictionary form
            Keys: The boxes, e.g., 'A1'
            Values: The value in each box, e.g., '8'. If the box has no value, then the value will be '123456789'.
    """
    values = []
    all_digits = '123456789'
    for c in grid_string:
        if c == '.':
            values.append(blanks)
        elif c in all_digits:
            values.append(c)
    return dict(zip(boxes, values))


def display(values):
    """
    Display the values as a 2-D grid.
    Args:
        values(dict): The sudoku in dictionary form
    """
    # Allocated the amount of space needed to hold the value of the greatest length.
    # For a complete board, this will just be 1.
    width = 1+max(len(values[s]) for s in boxes)

    # Multiply the width by 3
    # Take three of these
    # Add '+'s in between them
    line = '+'.join(['-'*(width*3)]*3)

    # For each row and column in the data:
    # Print the value in that cell
    # Center it (https://www.tutorialspoint.com/python/string_center.htm)
    # Add "|" if the string is in column 3 or 6.
    # Print a "line" if the current row is the third or sixth
    for r in ROWS:
        print(''.join(values[r+c].center(width)+('|' if c in '36' else '')
                      for c in COLS))
        if r in 'CF': print(line)
    return


def eliminate(values, peers):
    """Eliminate values from peers of each box with a single value.

    Go through all the boxes, and whenever there is a box with a single value,
    eliminate this value from the set of values of all its peers.

    Args:
        values: Sudoku in dictionary form.
    Returns:
        Resulting Sudoku in dictionary form after eliminating values.
    """
    # Get all the solved boxes
    solved_boxes = [box for box in values.keys() if len(values[box]) == 1]

    # For a given solved box...
    for box in solved_boxes:

        # ...get the value in the box
        digit = values[box]

        # ...and for each of that box's "peers"...
        for peer in peers[box]:

            # ...delete that value from the possible values in that box
            values[peer] = values[peer].replace(digit, '')
            # print("Eliminated ", digit, "from box ", peer, " using the 'eliminate' strategy.")
    return values


def only_choice(values, unitlist):
    """
    Go through all the units, and whenever there is a unit with a value that only fits in one box, assign the value to this box.
    Input: A sudoku in dictionary form.
    Output: The resulting sudoku in dictionary form.
    """
    for unit in unitlist:
        for digit in '123456789':
            dplaces = [box for box in unit if digit in values[box]]
            if len(dplaces) == 1 and values[dplaces[0]] != digit:
                values[dplaces[0]] = digit
                # print("Placed value ", digit, " in box ", dplaces[0])
    return values


def reduce_puzzle(values, unitlist, peers):
    """
    Iterate eliminate() and only_choice(). If at some point, there is a box with no available values, return False.
    If the sudoku is solved, return the sudoku.
    If after an iteration of both functions, the sudoku remains the same, return the sudoku.
    Input: A sudoku in dictionary form.
    Output: The resulting sudoku in dictionary form.
    """
    stalled = False
    while not stalled:
        # Check how many boxes have a determined value
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])
        # Use the Eliminate Strategy
        values = eliminate(values, peers)
        # Use the Only Choice Strategy
        values = only_choice(values, unitlist)
        # Use the Naked Twins Strategy
        values = naked_twins(values, peers)
        # Check how many boxes have a determined value, to compare
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        # If no new values were added, stop the loop.
        stalled = solved_values_before == solved_values_after
        # Sanity check, return False if there is a box with zero available values:
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values


def naked_twins(values, peers):
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}
        peers(dict): a dictionary with each cell as the key and each of its
        "peers" as a value
    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """
    """
    Implement the naked twins elimination strategy:
    Go through each cell:
    For each cell with two values:
    Find if there is a cell in "peers" that has the same two values in it
    Save those two box values
    For any cell that is a peer of both of those
    Eliminate those two values from those two boxes
    """
   # Get all the boxes with two values
    boxes_with_two = [box for box in values.keys() if len(values[box]) == 2]

    # Loop through these boxes
    for box_with_two in boxes_with_two:

        # Get that box's values
        box_values = values[box_with_two]

        # Peers that have the same two values:
        same_peers = [peer for peer in peers[box_with_two] if values[peer] == box_values]

        # Peers that have the same two values:
        if len(same_peers) == 1:

            # Peers that have the same two values:
            box_with_two_peers = same_peers[0]

            # Get the peers of each box
            peers_1, peers_2 = peers[box_with_two], peers[box_with_two_peers]

            # Get boxes that are peers of both
            peers_of_both = [peer2 for peer2 in peers_2 if peer2 in peers_1]

            # For each "peer of both"
            for peer_of_both in peers_of_both:

                # Eliminate the values from box's values
                for value in box_values:

                    # Eliminate the values from box's values
                    values[peer_of_both] = values[peer_of_both].replace(value, '')

            # print("Eliminated", box_values, "from", peers_of_both, "using naked twins.")
    return values

# def search(values):
#     pass

def solve_grid(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """
    print("Displaying the grid: ")
    grid_vals = grid_values(grid, blanks='.')
    display(grid_vals)
    print("Solving the puzzle: ")
    grid_vals_puzzle = grid_values(grid, blanks='123456789')
    final_values = reduce_puzzle(grid_vals_puzzle, unitlist_diag, peers_diag)
    return final_values

if __name__ == '__main__':
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    display(solve_grid(diag_sudoku_grid))

    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
