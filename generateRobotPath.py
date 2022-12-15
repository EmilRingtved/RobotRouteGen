# This code converts an SVG path to a series of coordinates
# It is intended as tool for generating a driving path for a diff drive robot

from svg.path import parse_path
from xml.dom import minidom
from bs4 import BeautifulSoup
from matplotlib import pyplot as plt
import numpy as np

# Parse an SVG path and return the coordinates of a point
# at a given distance along the path
def get_point_at(path, distance, scale, offset):
    pos = path.point(distance)
    pos += offset
    pos *= scale
    return pos.real, pos.imag

# Generate a sequence of points along an SVG path
# with a given density and scale
def points_from_path(path, density, scale, offset):
    step = int(path.length() * density)
    last_step = step - 1

    # Handle the case where the path is only one point long,
    if last_step == 0:
        yield get_point_at(path, 0, scale, offset)
        return

    for distance in range(step):
        yield get_point_at(path, distance / last_step, scale, offset)

# Generate a sequence of points from an SVG document
# with a given density and scale
def points_from_doc(doc, density=5, scale=1, offset=0):
    offset = offset[0] + offset[1] * 1j
    route_points = []
    stop_points = []
    # Searches the svg file for paths to generate waypoints from
    for element in doc.getElementsByTagName("path"):
        for path in parse_path(element.getAttribute("d")):
            route_points.extend(points_from_path(path, density, scale, offset))
    
    #searches for stop points in the svg file and appends them to the list of stop points
    for circle in doc.getElementsByTagName("circle"):
        x = circle.getAttribute('cx')
        y = circle.getAttribute('cy')
        stop_point = np.array([x,y])
        stop_points = np.append(stop_points,stop_point)

    return route_points, stop_points

# Convert an SVG path to a sequence of coordinates
# and return them as numpy arrays
def svg_to_cords(svg_path):

    y_coords = np.empty(0,float)
    x_coords = np.empty(0,float)

    doc = minidom.parseString(svg_path)
    # change density or scale to scale up system
    points = points_from_doc(doc, density=1, scale=1, offset=(0,0))
    for i in range(len(points)):
        print([points[i][0],points[i][1]])
        x_coords = np.append(x_coords, (points[i][0]))
        y_coords = np.append(y_coords, (points[i][1]))

    return x_coords, y_coords
