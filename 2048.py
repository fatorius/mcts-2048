from game import Game

game = Game()

while True:
    game.show_table()

    coord = input("Seu movimento: ")

    if coord == "w":
        game.move_up()
    elif coord == "s":
        game.move_down()
    elif coord == "a":
        game.move_left()
    else:
        game.move_right()

