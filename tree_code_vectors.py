import maya.cmds as cmds
import math
import random
import functools


def createUI(pWindowTitle, pApplyCallBack):
    windowID = 'miniTree'  # unique id to make sure only one is open at a time
    if cmds.window(windowID, exists=True):
        cmds.deleteUI(windowID)

    cmds.window(windowID, title=pWindowTitle, sizeable=True, resizeToFitChildren=True)
    cmds.rowColumnLayout(numberOfColumns=1, columnWidth=[(2, 400)], columnOffset=[(2, 'right', 5)])
    cmds.separator(h=10, style='none')
    randomSeed = cmds.intFieldGrp(label='Seed:',numberOfFields = 1,  value1=1234)
    cmds.separator(h=10, style='in')
    polyNumberField = cmds.intSliderGrp(label='Polygons:', min=3, max=20, value=4, step=1, field=True)
    cmds.separator(h=10, style='none')
    treeDepthField = cmds.intSliderGrp(label='Tree depth:', min=1, max=8, value=3, step=1, field=True)

    cmds.separator(h=10, style='none')
    treeSegmentLength = cmds.floatSliderGrp(label='Segment length:', min=0.2, max=20, value=5, step=0.1, field=True)

    cmds.separator(h=10, style='none')
    treeLengthDecrease = cmds.floatSliderGrp(label='Length decrease:', min=0.0, max=1, value=0.8, step=0.01, field=True)

    cmds.separator(h=10, style='none')
    trunkRadius = cmds.floatSliderGrp(label='Trunk radius:', min=0.1, max=10, value=1, step=0.1, field=True)

    cmds.separator(h=10, style='none')
    radiusDecrease = cmds.floatSliderGrp(label='Radius decrease:', min=0.0, max=1, value=0.8, step=0.01, field=True)

    cmds.separator(h=10, style='none')
    treeBranches = cmds.intSliderGrp(label='Branches:', min=1, max=8, value=2, step=1, field=True)

    cmds.separator(h=10, style='none')
    treeBranches_a = cmds.floatSliderGrp(label='Branches angle:', min=0, max=math.pi, value=0.5, step=0.01,
                                         field=True)

    cmds.separator(h=10, style='none')
    treeFoliageSze = cmds.floatSliderGrp(label='Foliage size:', min=0.1, max=20, value=1, step=0.01, field=True)

    cmds.separator(h=10, style='none')
    treeFoliageRes = cmds.intSliderGrp(label='Foliage resolution:', min=3, max=30, value=5, step=0.01, field=True)

    cmds.separator(h=10, style='none')  # empty row
    cmds.separator(h=10, style='none')
    cmds.separator(h=10, style='none')

    cmds.separator(h=10, style='none')
    cmds.button(label='Create tree', command=functools.partial(pApplyCallBack,
                                                               polyNumberField,
                                                               treeDepthField,
                                                               treeSegmentLength,
                                                               treeLengthDecrease,
                                                               trunkRadius,
                                                               radiusDecrease,
                                                               treeBranches,
                                                               treeBranches_a,
                                                               treeFoliageSze,
                                                               treeFoliageRes,
                                                               randomSeed
                                                               ))
    # when the button is pressed, callback function is called

    cmds.separator(h=10, style='none')
    cmds.separator(h=10, style='none')
    cmds.separator(h=10, style='none')
    cmds.separator(h=10, style='none')
    cmds.separator(h=10, style='none')

    def cancelCallBack(*pArgs):
        if cmds.window(windowID, exists=True):
            cmds.deleteUI(windowID)

   # cmds.button(label='Cancel', command=cancelCallBack)
    cmds.showWindow()


def applyCallBack(pPolyNumberField,
                  pTreeDepthField,
                  pTreeSegmentLength,
                  pLengthDecrease,
                  pRadius,
                  pRadDecrease,
                  pBranches,
                  pBranches_a,
                  pFoliageSze,
                  pFoliageRes,
                  pSeed,
                  *pArgs
                  ):
    polycount = cmds.intSliderGrp(pPolyNumberField, query=True, value=True)
    tree_depth = cmds.intSliderGrp(pTreeDepthField, query=True, value=True)
    segment_length = cmds.floatSliderGrp(pTreeSegmentLength, query=True, value=True)
    length_dec = cmds.floatSliderGrp(pLengthDecrease, query=True, value=True)
    radius = cmds.floatSliderGrp(pRadius, query=True, value=True)
    radius_d = cmds.floatSliderGrp(pRadDecrease, query=True, value=True)
    branches = cmds.intSliderGrp(pBranches, query=True, value=True)
    branches_a = cmds.floatSliderGrp(pBranches_a, query=True, value=True)
    foliage_s = cmds.floatSliderGrp(pFoliageSze, query=True, value=True)
    foliage_r = cmds.intSliderGrp(pFoliageRes, query=True, value=True)
    p_seed = cmds.intFieldGrp(pSeed, query = True, value = True)
    random.seed(p_seed[0])
    delete_previous()
    create(tree_depth,
           segment_length, length_dec, radius, radius_d,
           [0.0, 1.0, 0.0],
           [0.0, 0.0, 0.0],
           0.0, 0.0,
           polycount, branches, branches_a,
           foliage_s, foliage_r, 0.0, True
           )
    merge_tree()

createUI('miniTree', applyCallBack)

def delete_previous(): 
    segmentsList = cmds.ls('miniTreeTrunk*')
    foliageList = cmds.ls('miniTreeFoliage*')
    if len(segmentsList)>0:
       cmds.delete(segmentsList)
    if len(foliageList)>0:
       cmds.delete(foliageList)
        
def merge_tree(): 
    segmentsList = cmds.ls('treePart*')
    foliageList = cmds.ls('leaves*')
    
    treeTrunk = cmds.polyUnite(segmentsList)
    newTree = cmds.duplicate(treeTrunk[0], name= 'miniTreeTrunk')
    cmds.polyMergeVertex(newTree)
    cmds.delete(treeTrunk)
    
    leaves = cmds.polyUnite(foliageList)
    cmds.duplicate(leaves[0], name = 'miniTreeFoliage')
    cmds.delete(leaves)
    
    segmentsList = cmds.ls('treePart*')
    if len(segmentsList)>0:
        cmds.delete(segmentsList)
        
    foliageList = cmds.ls('leaves*')
    if len(foliageList)>0:
        cmds.delete(foliageList)

# Arguments: 'axis point 1', 'axis point 2', 'point to be rotated', 'angle of rotation (in radians)' >> 'new point'
def PointRotate3D(p1_x, p1_y, p1_z, p2_x, p2_y, p2_z, p0_x, p0_y, p0_z, theta):
    # Translate so axis is at origin
    p_x = p0_x - p1_x
    p_y = p0_y - p1_y
    p_z = p0_z - p1_z

    # Initialize point q
    q = [0.0, 0.0, 0.0]
    N_x = (p2_x - p1_x)
    N_y = (p2_y - p1_y)
    N_z = (p2_z - p1_z)

    Nm = math.sqrt(math.pow(N_x, 2) + math.pow(N_y, 2) + math.pow(N_z, 2))

    # Rotation axis unit vector
    n = [N_x / Nm, N_y / Nm, N_z / Nm]

    # Matrix common factors
    c = math.cos(theta)
    t = (1 - math.cos(theta))
    s = math.sin(theta)
    X = n[0]
    Y = n[1]
    Z = n[2]

    # Matrix 'M'
    d11 = t * X ** 2 + c
    d12 = t * X * Y - s * Z
    d13 = t * X * Z + s * Y
    d21 = t * X * Y + s * Z
    d22 = t * Y ** 2 + c
    d23 = t * Y * Z - s * X
    d31 = t * X * Z - s * Y
    d32 = t * Y * Z + s * X
    d33 = t * Z ** 2 + c

    #            |p.x|
    # Matrix 'M'*|p.y|
    #            |p.z|
    q[0] = d11 * p_x + d12 * p_y + d13 * p_z
    q[1] = d21 * p_x + d22 * p_y + d23 * p_z
    q[2] = d31 * p_x + d32 * p_y + d33 * p_z

    # Translate axis and rotated point back to original location
    return [q[0] + p1_x, q[1] + p1_y, q[2] + p1_z]


def getSpPoint(A,B,C):
    # first convert line to normalized unit vector
    x1 = A[0]
    y1 = A[1]
    z1 = A[2]
    x2 = B[0] 
    y2 = B[1]
    z2 = B[2]
    x3 = C[0] 
    y3 = C[1]
    z3 = C[2]
    dx = x2 - x1
    dy = y2 - y1
    dz = z2 - z1
    mag = math.sqrt(dx*dx + dy*dy + dz*dz)
    dx = dx/mag
    dy = dy/mag
    dz = dz/mag
    
    # translate the point and get the dot product
    theta = (dx * (x3 - x1)) + (dy * (y3 - y1)) + (dz * (z3 - z1))
    x4 = (dx * theta) + x1
    y4 = (dy * theta) + y1
    z4 = (dz * theta) + z1
    return [x4,y4,z4]

def get_point_given_dist(a, b, dist):
    #"""Return the point c such that line segment bc is perpendicular to
    #line segment ab and segment bc has length dist.
    #a and b are tuples of length 3, dist is a positive float.
    vec_ab = (b[0]-a[0], b[1]-a[1], b[2]-a[2])
    # Find a vector not parallel or antiparallel to vector ab
    if vec_ab[1] != 0 or vec_ab[2] != 0:
        vec = (1, 0, 0)
    else:
        vec = (0, 1, 0)
    # Find the cross product of the vectors
    cross = (vec_ab[1] * vec[2] - vec_ab[2] * vec[1],
             vec_ab[2] * vec[0] - vec_ab[0] * vec[2],
             vec_ab[0] * vec[1] - vec_ab[1] * vec[0])
    # Find the vector in the same direction with length dist
    factor = dist / math.sqrt(cross[0]**2 + cross[1]**2 + cross[2]**2)
    newvec = (factor * cross[0], factor * cross[1], factor * cross[2])
    # Find point c such that vector bc is that vector
    c = (b[0] + newvec[0], b[1] + newvec[1], b[2] + newvec[2])
    # Done!
    return c
    
def polytube(p1_x, p1_y, p1_z,
             p2_x, p2_y, p2_z,
             p0_x, p0_y, p0_z,
             p1_r, p2_r,
             polys):
    for i in range(0, polys):
        inc = math.pi * 2.0 / polys
        # points are being repositioned before rotation
        
        p = get_point_given_dist ([p0_x, p0_y, p0_z], [p1_x, p1_y, p1_z],p1_r) 
        point1 = PointRotate3D(p0_x, p0_y, p0_z,
                               p1_x, p1_y, p1_z,
                               p[0], p[1], p[2],
                               -(inc * i)
                               )                  
        point2 = PointRotate3D(p0_x, p0_y, p0_z,
                               p1_x, p1_y, p1_z,
                               p[0], p[1], p[2],
                               -(inc * i + inc)
                               )
        p = get_point_given_dist ([p1_x, p1_y, p1_z], [p2_x, p2_y, p2_z],p2_r) 
        point3 = PointRotate3D(p1_x, p1_y, p1_z,
                               p2_x, p2_y, p2_z,
                               p[0], p[1], p[2],
                               -(inc * i)
                               )
        point4 = PointRotate3D(p1_x, p1_y, p1_z,
                               p2_x, p2_y, p2_z,
                               p[0], p[1], p[2],
                               -(inc * i + inc)
                               )

        cmds.polyCreateFacet(p=[point2,
                                point1,
                                point3,
                                point4],
                                name = 'treePart#')


def create(p_depth,  # tree depth,
           p_length, p_length_inc, p_r, p_rate,
           p_l,  # last segment tip
           p_ll,  # last segment base
           branch_turn, branch_shift,
           polygons, num_branches, branch_ang, foliage_sze, foliage_res, turn, branch):
    if p_depth > 0:

        # get vector of last segment
        lv = [p_l[0] - p_ll[0], p_l[1] - p_ll[1], p_l[2] - p_ll[2]]

        # find the magnitude of vector p_lx, p_ly, p_lz
        m = math.sqrt(math.pow(lv[0], 2) + math.pow(lv[1], 2) + math.pow(lv[2], 2))

        # divide the vector by its magnitude to get unit vector
        u = [lv[0] / m, lv[1] / m, lv[2] / m]

        # now we add unit vector (multiplied by length) to the values to create new points
        v = [lv[0] + p_ll[0] + (u[0] * p_length), lv[1] + p_ll[1] + (u[1] * p_length), lv[2] + p_ll[2] + (u[2] * p_length)]

        # if p_depth < 2:
        # branch = False

        if branch:
            newP = [p_l[0] + 0.1, p_l[1], p_l[2]]
            p = getSpPoint (p_l, p_ll, newP)
            
            points = PointRotate3D(p[0], p[1], p[2],
                                   newP[0], newP[1], newP[2],
                                   v[0], v[1], v[2],
                                   branch_turn)
            yTurn = PointRotate3D(p_l[0], p_l[1], p_l[2],
                                  v[0], v[1], v[2],
                                  points[0], points[1], points[2],
                                  branch_shift)

            p_n = yTurn

        else:
            p_n = v

        # create a tube using the old and new points the angles control the tilt of the base and the top of the segment
        polytube(
            p_l[0], p_l[1], p_l[2],  # base point
            p_n[0], p_n[1], p_n[2], # top point
            p_ll[0], p_ll[1], p_ll[2],
            p_r, p_r * p_rate,  # base and top radius
            polygons)

        # reducing length and radius for a new segment, counting depth
        p_length = p_length * p_length_inc
        p_r = p_r * p_rate
        p_depth = p_depth - 1.0

        p_ll = p_l
        p_l = p_n

        if p_depth > 0:
            branch_turn = branch_ang
            turn = turn + math.pi / 2.0

            for i in range(0, num_branches):
                branch_shift = (i * ((math.pi * 2.0) / num_branches)) + turn

                create(p_depth, p_length, p_length_inc, p_r, p_rate,
                       p_l,
                       p_ll,
                       branch_turn, branch_shift,
                       polygons, num_branches, branch_ang,
                       foliage_sze, foliage_res, turn, branch)

        else:
            my_sphere = cmds.polySphere(r=foliage_sze, sa=foliage_res, sh=foliage_res, name='leaves#')
            cmds.move(p_l[0], p_l[1], p_l[2], my_sphere)
