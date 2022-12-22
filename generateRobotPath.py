# This code converts an SVG path to a series of coordinates
# It is intended as tool for generating a driving path for a diff drive robot

from svg.path import parse_path
from xml.dom import minidom
from matplotlib import pyplot as plt

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
    orientation_vectors = []
    colours = []
    # Searches the svg file for paths to generate waypoints from
    for element in doc.getElementsByTagName("path"):
        # Append the colour of the path to seperate the paths for different robots
        style = element.getAttribute('style')
        # make sure the colors are given as basic strings in the svg file
        # Find the marker for the start and stop part of the stroke section
        start = style.find(':') + 1
        stop = style.find(';')
        # append the colorcode to the array
        colour_code = style[start:stop]
        colours.append(colour_code)

        for path in parse_path(element.getAttribute("d")):
            route_points.extend(points_from_path(path, density, scale, offset))

    # Serches for orientation and stop point lines in the svg file and appends to the orientation_vector list
    # The start of the line will mark the stop point, and the end point will function as a turning point for the robot to orient
    # itself towards.
    # Every time the robot is haltet it it will check if a new orientation is given before driving. 
    for lines in doc.getElementsByTagName("line"):
        x1 = lines.getAttribute('x1')
        y1 = lines.getAttribute('y1')
        x2 = lines.getAttribute('x2')
        y2 = lines.getAttribute('y2')
        orientation_vector = (int(x2),int(y2))
        stop_point = (int(x1),int(y1))
        orientation_vectors.append(orientation_vector)
        stop_points.append(stop_point)
    return route_points, stop_points, orientation_vectors, colours

# Convert an SVG path to a sequence of coordinates
# and return them as numpy arrays
def print_test(test_svg):
    svg_file_path = test_svg
    with open(svg_file_path, "r") as f:
        # Read the contents of the file into a string variable
        svg_path = f.read()
    doc = minidom.parseString(svg_path)
    route, stop, orientation, colours= points_from_doc(doc,density=0.5, scale=1, offset=(0,0))
    # Plot options
    plt.figure()
    print('stroke %s' % colours)
    plt.scatter(*zip(*route),s=10,c='b', marker='x', label='way points')
    plt.scatter(*zip(*stop),s=10,c='r', marker='o', label='stop points')
    plt.scatter(*zip(*orientation),s=20,c='g',marker='+',label='orientation point')
    plt.legend(loc='upper left')
    plt.xlabel('x-axis')
    plt.ylabel('y-axis')
    plt.show()