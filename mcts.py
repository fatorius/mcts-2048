import math
import copy
import random

class MCTSNode:
    def __init__(self, game_state, parent=None, is_player_turn=True):
        self.game_state = game_state
        self.parent = parent
        self.children = {}
        self.is_player_turn = is_player_turn
        self.visits = 0
        self.value = 0

    def is_fully_expanded(self):
        return len(self.children) == 4

    def best_child(self, exploration_weight=1.0):
        return max(
            self.children.values(),
            key=lambda child: child.value / (child.visits + 1e-6) + exploration_weight * math.sqrt(
                math.log(self.visits + 1) / (child.visits + 1e-6)
            )
        )

    def best_action(self, exploration_weight=1.0):
        return max(
            self.children.items(),
            key=lambda item: item[1].value / (item[1].visits + 1e-6) + exploration_weight * math.sqrt(
                math.log(self.visits + 1) / (item[1].visits + 1e-6)
            )
        )[0]

    def select_child(self):
        if self.is_player_turn:
            return self.best_action()
        else:
            return random.choice(list(self.children.items()))

    def add_child(self, action, child_node):
        self.children[action] = child_node

class MCTS:
    def __init__(self, iterations=1000):
        self.iterations = iterations

    def search(self, root_state):
        root_node = MCTSNode(root_state)

        for _ in range(self.iterations):
            node = root_node
            state = copy.deepcopy(root_state)

            # Selection
            while not self.is_terminal(state):
                if not node.is_fully_expanded():
                    self.expand(node)
                    break
                elif node.is_player_turn:
                    action = node.select_child()
                    node = node.children[action]
                    state = self.apply_action(state, action)
                else:
                    action = random.choice(list(node.children.keys()))
                    node = node.children[action]
                    state = self.apply_action(state, action)

            # Expansion
            if not self.is_terminal(state):
                self.expand(node)

            # Simulation
            rollout_result = self.rollout(state)

            # Backpropagation
            self.backpropagate(node, rollout_result)

        return {"action": root_node.best_action(exploration_weight=0), "state": root_node.best_child(exploration_weight=0)}

    def expand(self, node):
        if node.is_player_turn:
            for action in self.get_possible_actions(node.game_state):
                if action not in node.children:
                    next_state = copy.deepcopy(node.game_state)
                    self.apply_action(next_state, action)
                    child_node = MCTSNode(next_state, parent=node, is_player_turn=False)
                    node.add_child(action, child_node)
        else:
            empty_cells = node.game_state.obter_celulas_vazias()
            for cell in empty_cells:
                for value in [2, 4]:
                    next_state = copy.deepcopy(node.game_state)
                    next_state.tile_values[cell] = value
                    next_state.update_score()
                    child_node = MCTSNode(next_state, parent=node, is_player_turn=True)
                    node.add_child((cell, value), child_node)

    def get_possible_actions(self, game_state):
        return game_state.get_possible_actions()

    def apply_action(self, game_state, action):
        if action == 'up':
            game_state.move_up()
        elif action == 'down':
            game_state.move_down()
        elif action == 'left':
            game_state.move_left()
        elif action == 'right':
            game_state.move_right()
        return game_state

    def is_terminal(self, game_state):
        return len(game_state.get_possible_actions()) == 0

    def rollout(self, game_state, max_rollout_depth=20):
        for _ in range(max_rollout_depth):
            possible_actions = self.get_possible_actions(game_state)
            if not possible_actions:
                break
            action = random.choice(possible_actions)
            self.apply_action(game_state, action)

        non_zero_tiles = len([v for v in game_state.tile_values if v > 0])
        return 1 / non_zero_tiles

    def backpropagate(self, node, reward):
        while node is not None:
            node.visits += 1
            node.value += reward
            node = node.parent