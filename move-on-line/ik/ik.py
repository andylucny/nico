import torch
from dk import dk

device = 'cpu'

start_point = torch.tensor([-11.446,  28.965,  45.596], dtype=torch.float32).to(device)
touch_point = torch.tensor([-45.279,   3.234,   0.092], dtype=torch.float32).to(device)
goal_vector = touch_point - start_point

initial_angles = torch.tensor([   3.149,   23.442,   43.397,   71.708,   38.377,  140.225,  -104.242], dtype=torch.float32).to(device)
points, vectors = dk(initial_angles) # == torch.tensor([-29.978,  14.916,  16.18 ], dtype=torch.float32)
point, vector = points[-1], vectors[-1]

def distance_point_to_line(A, B, C):
    AB = B - A
    AC = C - A
    cross_product = torch.cross(AB, AC)
    distance = torch.linalg.norm(cross_product,dim=-1) / torch.linalg.norm(AB,dim=-1)
    return distance

print(distance_point_to_line(start_point, touch_point, point)) # 3.0864214278276982

def angle_between_vectors(u,v):
    return torch.acos((u@v)/(u.norm()*v.norm()))*180.0/torch.pi

print(angle_between_vectors(goal_vector,vector))    

def closest_point_on_line(A, B, C):
    # Vector from A to B and from A to C
    AB = B - A
    AC = C - A
    # Calculate the fraction t (projection of AC onto AB, normalized)
    t = torch.dot(AC, AB) / torch.dot(AB, AB)
    return A + t*AB

goal_point = closest_point_on_line(start_point, touch_point, point).to(device)

angles = torch.tensor(list(initial_angles), requires_grad=True).to(device)

# Define learning rate
learning_rate = 0.05
lambd = 10.0

def train(epoches=60000):
    global angles
    same = 0
    for step in range(epoches):  # Number of iterations
        # Zero the gradients after updating
        if angles.grad is not None:
            angles.grad.zero_()

        points, vectors = dk(angles) # calculation
        point, vector = points[-1], vectors[-1]
        #print(goal_point.device,point.device,vector.device,goal_vector.device)
        loss = ((goal_point-point)**2).mean() + lambd*(1-torch.dot(vector/vector.norm(),goal_vector/goal_vector.norm())) # Loss to minimize
        loss.backward()      # Compute gradients

        # Update x using gradient descent
        with torch.no_grad():
            pom = learning_rate * angles.grad
            if ((10*(angles-pom)).round() - (10*angles).round()).abs().sum() == 0:
                same += 1
            else:
                same = 0
            angles -= pom

        # Early stopping condition
        if loss.item() < 1e-4:
            break
        if same >= 1000:
            break

        # Print progress
        #print(f"Step {step+1}: x = {[xi.item() for xi in x]}, y = {[yi.item() for yi in y]} grad: {[xi.item() for xi in x.grad]}")
        #if step % 1000 == 0:
        #    print(f"{[yi.item() for yi in y]} {loss.item()}")
        if step % 1000 == 0:
            print(f"{step}.",torch.norm(goal_point-point).item(), (1-torch.dot(vector/vector.norm(),goal_vector/goal_vector.norm())).item(), f"{point[0].item():.2f},{point[1].item():.2f},{point[2].item():.2f}")

def improve(start_point_, touch_point_, initial_angles_, point_=None, epoches=60000, device='cpu'):
    global start_point, touch_point, initial_angles, goal_vector, goal_point, angles
    start_point = torch.tensor(start_point_,dtype=torch.float32).to(device)
    touch_point = torch.tensor(touch_point_,dtype=torch.float32).to(device)
    initial_angles = torch.tensor(initial_angles_,dtype=torch.float32).to(device)
    goal_vector = touch_point - start_point
    points, vectors = dk(initial_angles)
    point, vector = points[-1], vectors[-1]
    if point_ is None:
        goal_point = closest_point_on_line(start_point, touch_point, point)
    else:
        goal_point = torch.tensor(point_,dtype=torch.float32).to(device)
    angles = torch.tensor(initial_angles_, requires_grad=True)
    train(epoches)
    points, vectors = dk(angles)
    point, vector = points[-1], vectors[-1]
    return [angle.item() for angle in angles], distance_point_to_line(start_point, touch_point, point).item(), angle_between_vectors(goal_vector,vector).item()

def angles2point(initial_angles_):
    return [ coord.item() for coord in dk(torch.tensor(initial_angles_,dtype=torch.float32))[0][-1]]

if __name__ == '__main__':
    train()

    print(angles)
    points, vectors = dk(angles)
    point, vector = points[-1], vectors[-1]
    print(distance_point_to_line(start_point, touch_point, point))
    print(angle_between_vectors(goal_vector,vector))
