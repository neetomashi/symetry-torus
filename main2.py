import cv2
import numpy as np

image_path = 'C:/Users/charl/Desktop/travaille/image/no symetry 1.png'

image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
edges = cv2.Canny(image, threshold1=30, threshold2=150)

contours, _ = cv2.findContours(edges.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
print(contours)
x = []
y = []
coordinate=[]
for contour in contours:
    for point in contour:
        x.append(point[0][0])
        y.append(point[0][1])
        


#need of tuples for the next  function instead of the array given by contour, much simpler to do,
#we will be stocking the coordinate of contour within the list of tuple coordinate

for i in range(len(x)):
    coordinate.append((x[i],y[i]))

"""now we have a way to find axe that might be symetry axis,
for that i created a function that separate the  contour into 2 list based on the position of the point to an axis i have given
"""

def separate_coordinates(coords, axis_slope, axis_intercept):
    side_a = []
    side_b = []

    for x, y in coords:
        if y > axis_slope * x + axis_intercept:
            side_a.append((x, y))
        else:
            side_b.append((x, y))

    return side_a, side_b
    
    # Renvoie les deux listes contenant les coordonnées de chaque côté de la droite
    return side_a, side_b




def calculate_slope(point1, point2):
    """
    Calcule la pente d'une droite à partir de deux points.
    
    point1: Tuple représentant le premier point (x1, y1).
    point2: Tuple représentant le deuxième point (x2, y2).
    :return pente de la droite.
    """

 
    x1, y1 = point1
    x2, y2 = point2
    
    if x1 == x2:
        slope =0 #réglechir a comment gerer la pente infinie
    
    else:slope = (y2 - y1) / (x2 - x1)
    return slope

#so now we will be looking at evert axis with  the same number of point on each side  and then we will apply condition to see 
#which of them are axis of symetry if non can be found then there is no symetry

axis=[]

for i in range(len(coordinate)):
    for j in range(i + 1, len(coordinate)):  # Start from i + 1 to avoid duplicates
        side_a, side_b = separate_coordinates(coordinate, calculate_slope(coordinate[i], coordinate[j]), coordinate[i])
        if abs(len(side_a) - len(side_b)) <=1:  #in case there are 2n+1 number of point 
            axis.append((coordinate[i], calculate_slope(coordinate[i], coordinate[j])))
            print("AAAXIIIIS",axis)

#now we have all the axis and the point from where they go without dupplication and with the same number of point on each side

# Now let's iterate through the identified potential axes and analyze symmetry
for axis_point, axis_slope in axis:
    opposite_points = []  # Stores the opposite points along the axis
    for x, y in coordinate:
        # Calculate the y-coordinate of the point on the other side of the axis
        opposite_y = axis_slope * (x - axis_point[0]) + axis_point[1]

        # Check if the opposite y-coordinate is within a certain threshold
        y_threshold = 5  # You can adjust this threshold as needed
        if abs(y - opposite_y) <= y_threshold:
            opposite_points.append((x, y))

    if len(opposite_points) > 0:
        print("Potential axis of symmetry:", axis_point, "with slope:", axis_slope)
        print("Opposite points:", opposite_points)
        
        # Check if the number of opposite points is close to the total number of coordinates
        if len(opposite_points) >= len(coordinate) - 1 and len(opposite_points) <= len(coordinate):
            print("Symmetric axis found!")
            print("Axis point:", axis_point, "Axis slope:", axis_slope)
            break  # Stop iterating through other potential axes
        
        # Now you can perform further analysis on these opposite points
        # to determine if the axis is indeed a symmetry axis
        # You can calculate distances, angles, etc. to verify symmetry



            
