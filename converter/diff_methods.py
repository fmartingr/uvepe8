from objects import Diff


class DiffMethod(object):
    pass


class SimpleMethod(DiffMethod):
    """
    Simple PIL getbbox() difference between frames
    """
    def difference(self, first, second):
        import ImageChops
        from hashlib import md5
        difference = ImageChops.difference(first, second)
        diff_box = difference.getbbox()
        diffs = []
        if diff_box is not None:
            size = (diff_box[2] - diff_box[0], diff_box[3] - diff_box[1])
            position = (diff_box[0], diff_box[1])
            diff = {
                "hash": md5(difference.tostring()).hexdigest(),
                "image": difference,
                "position": position,
                "size": size
            }
            diffs.append(diff)

        return diffs


class GridMethod(DiffMethod):
    """
    TODO
    Converts frame to grid and compare each grid square with the previous frame square grid
    --
    1) Calc dividers from the frame resolution
    2) Select the bigger one (max: 16?)
    -- or --
    1) Get the square size from parameter (override)
    --
    """

class SquaresMethod(DiffMethod):
    """
    TODO
    """
    pass