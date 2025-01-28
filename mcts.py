import math
import copy
import random

class MCTSNode:
    def __init__(self, game_state, parent=None):
        self.game_state = game_state
        self.parent = parent
        self.children = {}
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

            while not self.is_terminal(state) and node.is_fully_expanded():
                node = node.best_child()
                state = self.apply_action(state, node)

            if not self.is_terminal(state):
                for action in self.get_possible_actions(state):
                    if action not in node.children:
                        next_state = copy.deepcopy(state)
                        self.apply_action(next_state, action)
                        child_node = MCTSNode(next_state, parent=node)
                        node.add_child(action, child_node)
                        break

            rollout_result = self.rollout(state)

            self.backpropagate(node, rollout_result)

        return {"action": root_node.best_action(exploration_weight=0), "state": root_node.best_child(exploration_weight=0)}

    def get_possible_actions(self, game_state):
        return ['up', 'down', 'left', 'right']

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
        temp_state = copy.deepcopy(game_state)
        for action in self.get_possible_actions(temp_state):
            state_copy = copy.deepcopy(temp_state)
            self.apply_action(state_copy, action)
            if state_copy.tile_values != temp_state.tile_values:
                return False
        return True

    def rollout(self, game_state):
        while not self.is_terminal(game_state):
            action = random.choice(self.get_possible_actions(game_state))
            self.apply_action(game_state, action)

        non_zero_tiles = len([v for v in game_state.tile_values if v > 0])
        return game_state.score / non_zero_tiles if non_zero_tiles > 0 else 0

    def backpropagate(self, node, reward):
        while node is not None:
            node.visits += 1
            node.value += reward
            node = node.parent