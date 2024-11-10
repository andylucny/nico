import cv2
import numpy as np

# Parameters for the grid
rows, cols = 8, 16
cell_size = 40  # Size of each cell in pixels
grid_color = 255  # Color for white cells

# Meaning of the grid
halfbytes = np.array([
    [2,4,6,8,10,12,14,16,18,20,22,24,26,28,30,32],
    [2,4,6,8,10,12,14,16,18,20,22,24,26,28,30,32],
    [2,4,6,8,10,12,14,16,18,20,22,24,26,28,30,32],
    [2,4,6,8,10,12,14,16,18,20,22,24,26,28,30,32],
    [1,3,5,7, 9,11,13,15,17,19,21,23,25,27,29,31],
    [1,3,5,7, 9,11,13,15,17,19,21,23,25,27,29,31],
    [1,3,5,7, 9,11,13,15,17,19,21,23,25,27,29,31],
    [1,3,5,7, 9,11,13,15,17,19,21,23,25,27,29,31],
])
index = np.array([
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    [2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2],
    [3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3],
    [4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    [2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2],
    [3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3],
    [4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4],
])

# Initialize a grid of zeros (black cells)
grid = np.zeros((rows, cols), dtype=np.uint8)

def grid_code():
    hb = np.zeros((32,),np.int32)
    for i in range(rows):
        for j in range(cols):
            hb[halfbytes[i,j]-1] += grid[i,j] << index[i,j]-1
    return ''.join([hex(value)[2:].upper() for value in hb])

# Function to draw the grid
def draw_grid(img, grid):
    for i in range(rows):
        for j in range(cols):
            top_left = (j * cell_size, i * cell_size)
            bottom_right = ((j + 1) * cell_size, (i + 1) * cell_size)
            color = 255 if grid[i, j] == 1 else 0  # White if 1, black if 0
            cv2.rectangle(img, top_left, bottom_right, color, -1)
            cv2.rectangle(img, top_left, bottom_right, 128, 1)  # Grid lines

# Mouse callback function to toggle cell color
def toggle_cell(event, x, y, flags, param):
    global grid
    if event == cv2.EVENT_LBUTTONDOWN:
        col = x // cell_size
        row = y // cell_size
        if 0 <= row < rows and 0 <= col < cols:
            grid[row, col] = 1 - grid[row, col]  # Toggle cell
            update_display()

# Function to update display
def update_display():
    img = np.zeros((rows * cell_size, cols * cell_size), dtype=np.uint8)
    draw_grid(img, grid)
    cv2.imshow("Editable Grid", img)
    print(grid_code())

# Initialize display
cv2.namedWindow("Editable Grid")
cv2.setMouseCallback("Editable Grid", toggle_cell)
update_display()

# Main loop
while True:
    if cv2.waitKey(1) & 0xFF == 27:  # ESC key to exit
        break

cv2.destroyAllWindows()
