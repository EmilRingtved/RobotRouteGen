from svg.path import parse_path
from xml.dom import minidom
from matplotlib import pyplot as plt
import numpy as np

def get_point_at(path, distance, scale, offset):
    pos = path.point(distance)
    pos += offset
    pos *= scale
    return pos.real, pos.imag


def points_from_path(path, density, scale, offset):
    step = int(path.length() * density)
    last_step = step - 1

    if last_step == 0:
        yield get_point_at(path, 0, scale, offset)
        return

    for distance in range(step):
        yield get_point_at(path, distance / last_step, scale, offset)


def points_from_doc(doc, density=5, scale=1, offset=0):
    offset = offset[0] + offset[1] * 1j
    points = []
    for element in doc.getElementsByTagName("path"):
        for path in parse_path(element.getAttribute("d")):
            points.extend(points_from_path(path, density, scale, offset))

    return points

def svg_to_cords(svg_path):

    y_coords = np.empty(0,float)
    x_coords = np.empty(0,float)

    doc = minidom.parseString(svg_path)
    points = points_from_doc(doc, density=1, scale=1, offset=(0, 0))
    for i in range(len(points)):
        print([points[i][0],points[i][1]])
        x_coords = np.append(x_coords, (points[i][0]))
        y_coords = np.append(y_coords, (points[i][1]))

    return x_coords, y_coords

#def coords_to_angles(x,y):


svg_file_path = input("Write path to route svg.\n")
with open(svg_file_path, "r") as f:
    # Read the contents of the file into a string variable
    svg_str = f.read()
x_coords, y_coords = svg_to_cords(svg_str)
plt.scatter(x_coords,y_coords)
plt.show()