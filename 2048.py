import random

# Funções auxiliares para gerar números aleatórios e pesos
def get_n_random_unique_numbers(n, max_value):
    return random.sample(range(max_value + 1), n)

def get_random_from_array(arr):
    return random.choice(arr)

def get_random_from_array_with_weights(values, weights):
    return random.choices(values, weights, k=1)[0]

# =======================================================================

NUMBER_OF_CELLS = 16
NUMBER_OF_ROWS_AND_COLUMNS = int(NUMBER_OF_CELLS ** 0.5)

NEW_TILES_VALUES = [2, 4]
NEW_TILES_WEIGHTS = [0.75, 0.25]

# =======================================================================

tile_values = [0] * NUMBER_OF_CELLS
score = 0

def init_grid():
    global tile_values
    tile_values = [0] * NUMBER_OF_CELLS

def init_tiles():
    choosen_cells = get_n_random_unique_numbers(2, NUMBER_OF_CELLS - 1)
    for cell_number in choosen_cells:
        tile_values[cell_number] = get_random_from_array_with_weights(
            NEW_TILES_VALUES,
            NEW_TILES_WEIGHTS
        )

def obter_celulas_vazias():
    return [index for index, num in enumerate(tile_values) if num == 0]

def generate_new_tile():
    new_cell = get_random_from_array(obter_celulas_vazias())
    tile_value = get_random_from_array_with_weights(
        NEW_TILES_VALUES,
        NEW_TILES_WEIGHTS
    )
    tile_values[new_cell] = tile_value

def update_score():
    global score
    score = sum(tile_values)

def find_leftmost_available_tile(pos, value):
    tiles_left = pos % NUMBER_OF_ROWS_AND_COLUMNS

    for _ in range(tiles_left):
        checking_pos = pos - 1
        if tile_values[checking_pos] != 0:
            if tile_values[checking_pos] == value:
                return checking_pos
            return pos
        pos = checking_pos
    return pos

def find_topmost_available_tile(pos, value):
    tiles_up = pos // NUMBER_OF_ROWS_AND_COLUMNS

    for _ in range(tiles_up):
        checking_pos = pos - NUMBER_OF_ROWS_AND_COLUMNS
        if tile_values[checking_pos] != 0:
            if tile_values[checking_pos] == value:
                return checking_pos
            return pos
        pos = checking_pos
    return pos

def find_rightmost_available_tile(pos, value):
    tiles_right = ((pos // NUMBER_OF_ROWS_AND_COLUMNS + 1) * 4 - pos - 1)

    for _ in range(tiles_right):
        checking_pos = pos + 1
        if tile_values[checking_pos] != 0:
            if tile_values[checking_pos] == value:
                return checking_pos
            return pos
        pos = checking_pos
    return pos

def find_bottommost_available_tile(pos, value):
    tiles_down = (NUMBER_OF_CELLS - pos) // NUMBER_OF_ROWS_AND_COLUMNS

    for _ in range(tiles_down):
        checking_pos = pos + NUMBER_OF_ROWS_AND_COLUMNS

        if checking_pos >= NUMBER_OF_CELLS:
            return pos

        if tile_values[checking_pos] != 0:
            if tile_values[checking_pos] == value:
                return checking_pos
            return pos
        pos = checking_pos
    return pos

def move_tile_to(start, destination):
    if start == destination:
        return

    value = tile_values[start]
    destination_value = tile_values[destination]
    new_value = value

    if destination_value == value:
        new_value = value * 2

    tile_values[start] = 0
    tile_values[destination] = new_value

def move_left():
    number_of_moves = 0
    for pos in range(NUMBER_OF_CELLS):
        if tile_values[pos] == 0:
            continue
        destination = find_leftmost_available_tile(pos, tile_values[pos])
        if destination != pos:
            move_tile_to(pos, destination)
            number_of_moves += 1

    if number_of_moves > 0:
        generate_new_tile()

def move_up():
    number_of_moves = 0
    for pos in range(NUMBER_OF_CELLS):
        if tile_values[pos] == 0:
            continue
        destination = find_topmost_available_tile(pos, tile_values[pos])
        if destination != pos:
            move_tile_to(pos, destination)
            number_of_moves += 1

    if number_of_moves > 0:
        generate_new_tile()

def move_right():
    number_of_moves = 0
    for pos in range(NUMBER_OF_CELLS - 1, -1, -1):
        if tile_values[pos] == 0:
            continue
        destination = find_rightmost_available_tile(pos, tile_values[pos])
        if destination != pos:
            move_tile_to(pos, destination)
            number_of_moves += 1

    if number_of_moves > 0:
        generate_new_tile()

def move_down():
    number_of_moves = 0
    for pos in range(NUMBER_OF_CELLS - 1, -1, -1):
        if tile_values[pos] == 0:
            continue
        destination = find_bottommost_available_tile(pos, tile_values[pos])
        if destination != pos:
            move_tile_to(pos, destination)
            number_of_moves += 1

    if number_of_moves > 0:
        generate_new_tile()

def show_table():
    for column in range(NUMBER_OF_ROWS_AND_COLUMNS):
        for row in range(NUMBER_OF_ROWS_AND_COLUMNS):
            print(tile_values[(column * 4) + (row % 4)], end=" ")
        print("")

def main():
    init_grid()
    init_tiles()
    update_score()

    while True:
        show_table()
        coord = input("Insira o movimento: ")

        if coord == "w":
            move_up()
        elif coord == "a":
            move_left()
        elif coord == "d":
            move_right()
        elif coord == "s":
            move_down()

        update_score()

main()