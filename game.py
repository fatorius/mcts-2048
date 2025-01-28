import random

def get_n_random_unique_numbers(n, max_value):
    return random.sample(range(max_value + 1), n)

def get_random_from_array(arr):
    return random.choice(arr)

def get_random_from_array_with_weights(values, weights):
    return random.choices(values, weights, k=1)[0]

class Game:
    def __init__(self):
        self.NUMBER_OF_CELLS = 16
        self.NUMBER_OF_ROWS_AND_COLUMNS = int(self.NUMBER_OF_CELLS ** 0.5)

        self.NEW_TILES_VALUES = [2, 4]
        self.NEW_TILES_WEIGHTS = [0.75, 0.25]

        self.tile_values = []
        self.score = 0


        self.init_grid()
        self.init_tiles()
        self.update_score()

    def init_grid(self):
        for _ in range(self.NUMBER_OF_CELLS):
            self.tile_values.append(0)

    def init_tiles(self):
        choosen_cells = get_n_random_unique_numbers(2, self.NUMBER_OF_CELLS - 1)
        for cell_number in choosen_cells:
            self.tile_values[cell_number] = get_random_from_array_with_weights(
                self.NEW_TILES_VALUES,
                self.NEW_TILES_WEIGHTS
            )

    def obter_celulas_vazias(self):
        return [index for index, num in enumerate(self.tile_values) if num == 0]

    def generate_new_tile(self):
        new_cell = get_random_from_array(self.obter_celulas_vazias())
        tile_value = get_random_from_array_with_weights(
            self.NEW_TILES_VALUES,
            self.NEW_TILES_WEIGHTS
        )
        self.tile_values[new_cell] = tile_value

    def update_score(self):
        self.score = sum(self.tile_values)

    def find_leftmost_available_tile(self, pos, value):
        tiles_left = pos % self.NUMBER_OF_ROWS_AND_COLUMNS

        for _ in range(tiles_left):
            checking_pos = pos - 1
            if self.tile_values[checking_pos] != 0:
                if self.tile_values[checking_pos] == value:
                    return checking_pos
                return pos
            pos = checking_pos
        return pos

    def find_topmost_available_tile(self, pos, value):
        tiles_up = pos // self.NUMBER_OF_ROWS_AND_COLUMNS

        for _ in range(tiles_up):
            checking_pos = pos - self.NUMBER_OF_ROWS_AND_COLUMNS
            if self.tile_values[checking_pos] != 0:
                if self.tile_values[checking_pos] == value:
                    return checking_pos
                return pos
            pos = checking_pos
        return pos

    def find_rightmost_available_tile(self, pos, value):
        tiles_right = ((pos // self.NUMBER_OF_ROWS_AND_COLUMNS + 1) * 4 - pos - 1)

        for _ in range(tiles_right):
            checking_pos = pos + 1
            if self.tile_values[checking_pos] != 0:
                if self.tile_values[checking_pos] == value:
                    return checking_pos
                return pos
            pos = checking_pos
        return pos

    def find_bottommost_available_tile(self, pos, value):
        tiles_down = (self.NUMBER_OF_CELLS - pos) // self.NUMBER_OF_ROWS_AND_COLUMNS

        for _ in range(tiles_down):
            checking_pos = pos + self.NUMBER_OF_ROWS_AND_COLUMNS

            if checking_pos >= self.NUMBER_OF_CELLS:
                return pos

            if self.tile_values[checking_pos] != 0:
                if self.tile_values[checking_pos] == value:
                    return checking_pos
                return pos
            pos = checking_pos
        return pos

    def move_tile_to(self, start, destination):
        if start == destination:
            return

        value = self.tile_values[start]
        destination_value = self.tile_values[destination]
        new_value = value

        if destination_value == value:
            new_value = value * 2

        self.tile_values[start] = 0
        self.tile_values[destination] = new_value

    def move_left(self):
        number_of_moves = 0
        for pos in range(self.NUMBER_OF_CELLS):
            if self.tile_values[pos] == 0:
                continue
            destination = self.find_leftmost_available_tile(pos, self.tile_values[pos])
            if destination != pos:
                self.move_tile_to(pos, destination)
                number_of_moves += 1

        if number_of_moves > 0:
            self.generate_new_tile()

    def move_up(self):
        number_of_moves = 0
        for pos in range(self.NUMBER_OF_CELLS):
            if self.tile_values[pos] == 0:
                continue
            destination = self.find_topmost_available_tile(pos, self.tile_values[pos])
            if destination != pos:
                self. move_tile_to(pos, destination)
                number_of_moves += 1

        if number_of_moves > 0:
            self.generate_new_tile()

    def move_right(self):
        number_of_moves = 0
        for pos in range(self.NUMBER_OF_CELLS - 1, -1, -1):
            if self.tile_values[pos] == 0:
                continue
            destination = self.find_rightmost_available_tile(pos, self.tile_values[pos])
            if destination != pos:
                self.move_tile_to(pos, destination)
                number_of_moves += 1

        if number_of_moves > 0:
            self.generate_new_tile()

    def move_down(self):
        number_of_moves = 0
        for pos in range(self.NUMBER_OF_CELLS - 1, -1, -1):
            if self.tile_values[pos] == 0:
                continue
            destination = self.find_bottommost_available_tile(pos, self.tile_values[pos])
            if destination != pos:
                self.move_tile_to(pos, destination)
                number_of_moves += 1

        if number_of_moves > 0:
            self.generate_new_tile()

    def show_table(self):
        print(f"Pontuação: {self.score}")
        for column in range(self.NUMBER_OF_ROWS_AND_COLUMNS):
            for row in range(self.NUMBER_OF_ROWS_AND_COLUMNS):
                print(self.tile_values[(column * 4) + (row % 4)], end=" ")
            print("")
