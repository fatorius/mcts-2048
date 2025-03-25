from game import Game
from mcts import MCTS

game = Game()
mcts = MCTS(iterations=100)

mcts.collect_training_data(game)