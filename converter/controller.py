from objects import Frame, Diff
import diff_methods


class Controller(object):
    current = -1
    items = []

    def get_current(self):
        if self.current >= 0:
            return self.items[self.current]

    def get_previous(self):
        if self.current > 0:
            return self.items[self.current-1]


class FrameController(Controller):
    method = None
    current = -1
    items = []

    def __init__(self, method='Simple', difference=100):
        # Load diff method
        module = __import__("diff_methods")
        try:
            method = getattr(module, "%sMethod" % method)
        except Exception:
            print "Cant load %s diff method, using simple..." % method
            method = getattr(module, "SimpleMethod")
        self.method = method()
        self.method.min_difference = difference

    def append(self, path):
        new_item = Frame(self, path)
        self.items.append(new_item)
        self.current += 1

    def get_difference(self, current_frame, previous_frame):
        diffs = self.method.difference(current_frame, previous_frame)
        return diffs

    def remove(self, frame):
        self.items.remove(frame)
        self.current -= 1


class DiffController(Controller):
    current = -1
    items = []

    total = {
        "width": 0,
        "height": 0
    }

    def append(self, object):
        new_item = Diff(self, object['image'],
            object['size'][0],
            object['size'][1])
        self.total["width"] += object["size"][0]
        self.total["height"] += object["size"][1]
        new_item.hash = object['hash']
        self.items.append(new_item)
        self.current += 1

    def find_hash(self, hash):
        # Find if hash has already been stored
        # *What do we say to redundancy? Not today*
        if len(self.items) > 0:
            for item in self.items:
                if item.hash == hash:
                    return self.items.index(item)
        return None

    def sort_by_size(self):
        self.items.sort(key=lambda x: x.size, reverse=True)
