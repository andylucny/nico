from madcad import *

def basehalf():
    p1 = Point(0, 0, 0)
    p2 = Point(8, 0, 0) #64
    p3 = Point(8, 32, 0) #64
    p4 = Point(0, 32, 0)

    # Create segments between each pair of points
    side1 = Segment(p1, p2)
    side2 = Segment(p2, p3)
    side3 = Segment(p3, p4)
    side4 = Segment(p4, p1)

    profile = web([side1, side2, side3, side4])
    for i in range(2): #16
        for j in range(8):
            circle = Circle((Point(2+4*i,2+4*j,0), Z), 1.5)
            profile += web(circle).flip()

    head = flatsurface(profile)
    bottom = head.flip() # .flip() to reverse bright and dark surface
    head = head.transform(3*Z)

    model = extrusion(3*Z, profile) + head + bottom

    return model + model.transform(8*X) 

def basewall():
    p1 = Point(0, 0, 0)
    p2 = Point(32, 0, 0)
    p3 = Point(32, 32, 0)
    p4 = Point(0, 32, 0)
    side1 = Segment(p1, p2)
    side2 = Segment(p2, p3)
    side3 = Segment(p3, p4)
    side4 = Segment(p4, p1)
    innerprofile = web([side1, side2, side3, side4])

    p1 = Point(-1, -1, 0)
    p2 = Point(33, -1, 0)
    p3 = Point(33, 33, 0)
    p4 = Point(-1, 33, 0)
    side1 = Segment(p1, p2)
    side2 = Segment(p2, p3)
    side3 = Segment(p3, p4)
    side4 = Segment(p4, p1)
    outerprofile = web([side1, side2, side3, side4])
    
    profile = outerprofile + innerprofile.flip()

    head = flatsurface(profile)
    bottom = head.flip() # .flip() to reverse bright and dark surface
    head = head.transform(5.5*Z)

    model = extrusion(5.5*Z, profile) + head + bottom

    return model


base = basehalf()

wall = basewall()

m = base + base.transform(16*X) + wall

show([m])

write(m,'b.stl')

"""
int_circle = Circle((O, Z), 5)
# Create outline for extrusion to get the lateral surface
profile = web(ext_circle) + web(int_circle).flip() # .flip() to make a hole
# Create top and bottom surface
head = flatsurface(profile)
bottom = head.flip() # .flip() to reverse bright and dark surface
head = head.transform(10 * (Z + 0.2 * Y))
# Generate extrusion of `profile` with the direction `10 * (Z + 0.2 * Y)`
m = extrusion(10 * (Z + 0.2 * Y), profile) + head + bottom
show([m])
"""