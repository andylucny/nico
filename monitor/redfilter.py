import os
import cv2
import numpy as np

def red_filter(image):
    
    # Convert the image to HSV (Hue, Saturation, Value) color space
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Define the lower and upper range of red color in HSV
    lower_red = np.array([1, 100, 10])    # Red in lower range (1-10 hue)
    upper_red = np.array([8, 255, 255])

    # Create masks for the red color ranges
    red_mask = cv2.inRange(hsv_image, lower_red, upper_red)

    # Erosion removes isolated points, and dilation restores the shape of valid objects
    kernel = np.ones((3, 3), np.uint8)  # A 3x3 kernel to check neighbors
    red_mask = cv2.morphologyEx(red_mask, cv2.MORPH_OPEN, kernel)
    
    # Find all connected components
    num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(red_mask, connectivity=8)

    if num_labels < 2:  # Only background found
        return None, None

    # Ignore the background (label 0), find the largest component
    largest_label = 1 + np.argmax(stats[1:, cv2.CC_STAT_AREA])  # Skip background
    largest_area = stats[largest_label, cv2.CC_STAT_AREA]
    largest_component = (labels == largest_label).astype(np.uint8) * 255

    # Center of gravity of the largest component
    centroid = tuple(np.int32(np.round(centroids[largest_label])))
    return centroid, largest_area

if __name__ == '__main__':

    # Load the image
    image_path = "data2/color01240.png"
    image = cv2.imread(image_path)
    if image is None:
        print("Error: Image not found.")
        os._exit(0)
      
    # Specify the image path and apply the red filter
    point, _ = red_filter(image)

    disp = np.copy(image)
    cv2.circle(disp,point,3,(0,255,0),cv2.FILLED)
    cv2.imwrite('red_mask.png',disp)
