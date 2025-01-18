
class TreeNode:
    def __init__(self, seeds, _parent=None):
        if _parent is None:
            self.level = 1
        else:
            self.level = _parent.level + 1
        self.seeds = seeds
        self.size = len(seeds)
        self.parent = _parent
        self.children = []
        self.subspace = ['0'] * 32
        self.dimension = 0
        self.is_leaf = False

    def remove_child_node(self, child_node):
        if child_node in self.children:
            self.children.remove(child_node)
