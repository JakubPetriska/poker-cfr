import numpy as np

from tools.constants import NUM_ACTIONS


def _tree_str_rec(root, offset):
    result = '%s%s\n' % (' ' * offset, root)
    for _, item in root.children.items():
        result += _tree_str_rec(item, offset + 1)
    return result


def tree_str(root):
    result = ''
    for _, item in root.children.items():
        result += _tree_str_rec(item, 0)
    return result


class Node:
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.children = {}

    def set_child(self, key, child):
        self.children[key] = child

    def __str__(self):
        if not self.parent:
            return ''
        parent_str = str(self.parent)
        parents_children = list(
            filter(lambda item: item[1] == self, self.parent.children.items()))
        if len(parents_children) == 0:
            raise RuntimeError('Parent does not have this node as a child')
        child_key = parents_children[0][0]
        if isinstance(self.parent, HoleCardsNode) or isinstance(self.parent, BoardCardsNode):
            child_key = ':'.join([str(card) for card in child_key]) + ':'
            if parent_str and not parent_str.endswith(':'):
                child_key = ':' + child_key
        else:
            if child_key == 0:
                child_key = 'f'
            elif child_key == 1:
                child_key = 'c'
            elif child_key == 2:
                child_key = 'r'
        return parent_str + child_key


class TerminalNode(Node):
    def __init__(self, parent, pot_commitment):
        super().__init__(parent)
        self.pot_commitment = pot_commitment


class HoleCardsNode(Node):
    def __init__(self, parent, card_count):
        super().__init__(parent)
        self.card_count = card_count


class BoardCardsNode(Node):
    def __init__(self, parent, card_count):
        super().__init__(parent)
        self.card_count = card_count


class ActionNode(Node):
    def __init__(self, parent, player):
        super().__init__(parent)
        self.player = player


class StrategyActionNode(ActionNode):
    def __init__(self, parent, player):
        super().__init__(parent, player)
        self.strategy = np.zeros(NUM_ACTIONS)
