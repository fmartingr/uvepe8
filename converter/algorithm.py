class Algorithm(object):
    pass


class BinaryTreeNode(object):
    diff_key = None
    used = False
    x = 0
    y = 0
    width = 0
    height = 0
    down = None
    right = None
    
    def __init__(self, block=None):
        if block is not None:
            self.diff_key = block['diff_key']
            self.width = block['width']
            self.height = block['height']
        

class BinaryTreeAlgorithm(Algorithm):
    root = None

    growing = 'down'
    max_size = {
        'width': 0,
        'height': 0
    }

    def __init__(self, width=0, height=0):
        self.max_size['width'] = width
        self.max_size['height'] = height
        if height > 0: self.growing = 'right'

    def fit(self, block):
        if self.root is None:
            self.root = BinaryTreeNode(block)
        node = self.find(self.root, block)
        if node is not None:
            block_node = self.split(node, block)
        else:
            block_node = self.grow(block)
        return block_node

    def find(self, node, block):
        """
        size = tuple(width, height)
        """
        if node.used:
            return self.find(node.right, block) or self.find(node.down, block)
        elif block['width'] <= node.width and block['height'] <= node.height:
           return node
        else:
            return None

    def split(self, node, block):
        node.used = True
        #if self.max_size['width'] > 0 and self.max_size['width'] < block['width']:
        # New down node
        node.down = BinaryTreeNode()
        node.down.x = node.x
        node.down.y = node.y + block['height']
        node.down.width = node.width
        node.down.height = node.height - block['height']

        #if self.max_size['height'] > 0 and self.max_size['height'] < block['height']:
        # New right node
        node.right = BinaryTreeNode()
        node.right.x = node.x + block['width']
        node.right.y = node.y
        node.right.width = node.width - block['width']
        node.right.height = block['height']
        return node

    def grow(self, block):
        if self.grow == 'down':
            self.root.used = True
            self.root.x = 0
            self.root.y = 0
            self.root.height = self.root.height + block['height']
            self.root.down = BinaryTreeNode()
            self.root.down.x = 0
            self.root.down.y = self.root.height
            self.root.down.width = self.root.width
            self.root.down.height = block['height']
            self.root.width = self.root.width,
            self.root.right = BinaryTreeNode()
        else:
            self.root.used = True
            self.root.x = 0
            self.root.y = 0
            self.root.down = BinaryTreeNode()
            self.root.right = BinaryTreeNode()
            self.root.right.x = self.root.width
            self.root.right.y = 0
            self.root.right.width = block['width']
            self.root.right.height = self.root.height
            self.root.height = self.root.height
            self.root.width = self.root.width + block['width']

        node = self.find(self.root, block)
        if node is not None:
            return self.split(node, block)
        else:
            print "none"
            return None

    def append(self, diff):
        """
        Find empty space for the image and returns:
        tuple(node key, x, y)
        """
        block = {
            'diff_key': diff[0],
            'width': diff[1],
            'height': diff[2]
        }

        block_node = self.fit(block)
        return block['diff_key'], block_node.x, block_node.y, block_node.width, block_node.height

    def get_total_size(self):
        return self.root.width, self.root.height