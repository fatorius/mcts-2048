from game import Game
from mcts import MCTS

game = Game()
mcts = MCTS(iterations=1000)

game.show_table()

result = mcts.search(game)

print(result['action'])

print(f"\nMelhor jogada: {result['action']}")
result['state'].game_state.show_table()