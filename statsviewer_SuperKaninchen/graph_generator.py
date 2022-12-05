
class Graph(object):

    def __init__(self, data, width, height, max, unit) -> None:
        points = generatePointList(data, width, height)
        self.lines = generateLineList(points)
        self.width = width
        self.height = height
        self.max = max
        self.unit = unit


def generatePointList(entries, width, height):
    points = []

    for i in range(len(entries)):
        v = entries[i]
        y = height - v * (height / 100) if v else None

        point = {
            "x": i * (width / len(entries)),
            "y": y
        }

        points.append(point)
    
    return points


def generateLineList(points):
    lines = []

    for i in range(len(points)-1):
        p1 = points[i]
        p2 = points[i+1]

        line = {
            "x1": p1["x"],
            "y1": p1["y"],
            "x2": p2["x"],
            "y2": p2["y"]
        }
        
        lines.append(line)
    
    return lines