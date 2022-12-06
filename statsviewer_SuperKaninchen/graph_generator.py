
class Graph(object):

    def __init__(self, title, data, width, height, max, unit, resolution=500) -> None:
        self.title = title
        data = averageDataToLength(data, resolution)
        points = generatePointList(data, width, height, max)
        self.lines = generateLineList(points)
        self.width = width
        self.height = height
        self.max = max
        self.unit = unit
        self.segment_width = width / len(data)
        for i in range(len(data)-1, 0, -1):
            if data[i]:
                self.last_value = int(data[i])
                break


def averageDataToLength(data, length):
    step = int(len(data)/length)
    if step < 2:
        return data
    
    averaged_data = []
    for i in range(length):
        sum = 0
        average = 10
        for j in range(step):
            if not data[i*step+j]:
                average = None
                break
            sum += data[i*step+j]
        
        if average:
            average = sum/step
        averaged_data.append(average)
        
    return averaged_data


def generatePointList(entries, width, height, max):
    points = []

    for i in range(len(entries)):
        v = entries[i]
        y = height - v * (height / max) if v else None

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