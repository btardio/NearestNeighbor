import open3d
import numpy as np
from decimal import Decimal

f = open('input', 'r')

inarr = None 
initialized = False

indexdict = {}

maxindex = 0

for line in f:
    index = line.split(" ")[0]
    
    foarray = []
    try:
        foarray.append(line.split(" ")[1].replace("(", "").replace(")", "").replace(",",""))
        foarray.append(line.split(" ")[2].replace("(", "").replace(")", "").replace(",",""))
        foarray.append(line.split(" ")[3].replace("(", "").replace(")", "").replace(",","").replace("\n",""))
    except IndexError as e:
        break

    foarray = [ Decimal(x) for x in foarray ]

    npfoarray = np.array(foarray, np.float64)
        
    indexdict[str(npfoarray)] = index.replace("#", "")

    if initialized: inarr = np.vstack((inarr, npfoarray))
    else: 
        inarr = npfoarray
        initialized = True

    maxindex = int(index.replace("#", ""))

radii = Decimal(line)

if radii > Decimal(0): radii = radii + Decimal(0.01) 
else: radii = radii - Decimal(0.01)

points = inarr

pcd = open3d.geometry.PointCloud()

# From numpy to Open3D
pcd.points = open3d.utility.Vector3dVector(points)

# From Open3D to numpy
np_points = np.asarray(pcd.points)

print ( np_points )

pcd_tree = open3d.geometry.KDTreeFlann(pcd)
print()

first = True
finalstr = "#1 [["
for index in range(0,maxindex):

    [k, idx, _] = pcd_tree.search_radius_vector_3d(pcd.points[index], radii)

    if not first: finalstr += "#" + str(index+1) + " ["
    finalstr += str(k-1) + ", "

    #print (np.asarray(pcd.points)[idx[1:], :])

    for point in np.asarray(pcd.points)[idx[1:], :]:
        #print (indexdict[str(point)])
        finalstr += indexdict[str(point)] + ", "
    
    finalstr = finalstr[:-2]

    finalstr += "],\n"

    first = False

finalstr = finalstr[:-2]
finalstr += "]"

print (finalstr)
