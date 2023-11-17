import numpy as np

def loadAnimation(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()
        concerned_dofs = eval(lines[0])
        recorded_poses = []
        for line in lines[1:]:
            recorded_pose = eval(line[:-1])
            recorded_poses.append(recorded_pose)
        return (concerned_dofs,recorded_poses)
    raise(BaseException(filename+" does not exist"))

anim = np.array(loadAnimation('p1.txt')[1])

import numpy as np

def distance_point_to_line(point, start, end):
    """
    Calculate the perpendicular distance from a point to a line defined by two other points.
    This version works for N-dimensional space.
    """
    if np.all(start == end):
        return np.linalg.norm(point - start)
    
    line_vector = end - start
    point_vector = point - start
    projection = np.dot(point_vector, line_vector) / np.dot(line_vector, line_vector)
    if 0 <= projection <= 1:
        perpendicular = point_vector - projection * line_vector
        return np.linalg.norm(perpendicular)
    else:
        # If the projection is outside the segment, use the distance to the closest endpoint
        return min(np.linalg.norm(point - start), np.linalg.norm(point - end))

def rdp_simplify(points, epsilon):
    """
    Simplify a trajectory using the Ramer-Douglas-Peucker algorithm.
    """
    if len(points) <= 2:
        return points

    # Find the point with the maximum distance
    d_max = 0
    index = 0
    start, end = points[0], points[-1]

    for i in range(1, len(points) - 1):
        d = distance_point_to_line(points[i], start, end)
        if d > d_max:
            index = i
            d_max = d

    # If the maximum distance is greater than the threshold, recursively simplify both segments
    if d_max > epsilon:
        recursive1 = rdp_simplify(points[:index + 1], epsilon)
        recursive2 = rdp_simplify(points[index:], epsilon)

        # Concatenate the results
        result = np.vstack((recursive1[:-1], recursive2))
    else:
        # Otherwise, the current segment is within the accuracy threshold
        result = np.vstack((points[0], points[-1]))

    return result

# Set the desired accuracy (adjust as needed)
epsilon = 0.1

simplified_anim = rdp_simplify(anim, epsilon)
