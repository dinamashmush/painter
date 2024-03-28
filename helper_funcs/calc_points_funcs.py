
def calculate_points_on_line(x0, y0, x1, y1, num_points=20):
    """Calculate a list of points on a line segment defined by two endpoints.

    Args:
        x0 (float): X-coordinate of the first endpoint.
        y0 (float): Y-coordinate of the first endpoint.
        x1 (float): X-coordinate of the second endpoint.
        y1 (float): Y-coordinate of the second endpoint.
        num_points (int, optional): Number of points to generate on the line segment. Default is 20.

    Returns:
        list: A list of (x, y) tuples representing the points on the line segment.
    """
    # Check if x0 is equal to x1
    if x0 == x1:
        # Handle the case of a vertical line
        m = None
        b = None
    else:
        # Calculate the slope and y-intercept of the line
        m = (y1 - y0) / (x1 - x0)
        b = y0 - m * x0

    # Calculate the x coordinates of the points
    x_values = [x0 + i * (x1 - x0) / (num_points - 1)
                for i in range(num_points)]

    # Calculate the corresponding y coordinates
    if m is None:
        # Handle the case of a vertical line
        y_values = [y0 + i * (y1 - y0) / (num_points - 1)
                    for i in range(num_points)]
    else:
        y_values = [m * x + b for x in x_values]

    # Combine the x and y coordinates into point tuples
    points = [(int(x), int(y)) for x, y in zip(x_values, y_values)]

    return points

def is_point_inside_triangle(point, A, B, C):
    """
    Check if a point is inside a triangle using cross product method.

    Arguments:
    point : tuple (x, y) - Coordinates of the point to be checked.
    A, B, C : tuple (x, y) - Coordinates of the vertices of the triangle.

    Returns:
    bool: True if the point is inside the triangle, False otherwise.
    """
    def sign(p1, p2, p3):
        return (p1[0] - p3[0]) * (p2[1] - p3[1]) - (p2[0] - p3[0]) * (p1[1] - p3[1])

    b1 = sign(point, A, B) < 0.0
    b2 = sign(point, B, C) < 0.0
    b3 = sign(point, C, A) < 0.0

    return ((b1 == b2) and (b2 == b3))


def is_point_inside_oval(point, rect_point1, rect_point2):
    """
    Check if a point is inside an oval given the bounding rectangle.

    Arguments:
    point: tuple (x, y) - Coordinates of the point to be checked.
    rect_point1: tuple (x, y) - Coordinates of one of the points of the bounding rectangle.
    rect_point2: tuple (x, y) - Coordinates of the opposite point of the bounding rectangle.

    Returns:
    bool: True if the point is inside the oval, False otherwise.
    """
    # Calculate center of the oval
    center = ((rect_point1[0] + rect_point2[0]) / 2, (rect_point1[1] + rect_point2[1]) / 2)

    # Calculate major and minor axes lengths
    major_axis = abs(rect_point2[0] - rect_point1[0]) / 2
    minor_axis = abs(rect_point2[1] - rect_point1[1]) / 2

    # Normalize point to oval coordinate system (centered at the oval's center)
    normalized_point = (point[0] - center[0], point[1] - center[1])

    # Use ellipse equation to check if the point is inside the oval
    return (((normalized_point[0] ** 2) / (major_axis ** 2) + (normalized_point[1] ** 2) / (minor_axis ** 2))) <= 1
    
    
