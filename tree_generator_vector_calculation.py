import maya.cmds as cmds
import math
import random
import functools


def createUI(pWindowTitle, pApplyCallBack):
    windowID = 'miniTree'  # unique id to make sure only one is open at a time
    if cmds.window(windowID, exists=True):
        cmds.deleteUI(windowID)

    cmds.window(windowID, title=pWindowTitle, sizeable=False, resizeToFitChildren=True)
    cmds.rowColumnLayout(numberOfColumns=3, columnWidth=[(1, 50), (2, 400), (3, 50)], columnOffset=[(1, 'right', 2)])
    cmds.separator(h=10, style='none')
    cmds.separator(h=10, style='none')
    cmds.separator(h=10, style='none')

    cmds.separator(h=10, style='none')
    polyNumberField = cmds.intSliderGrp(label='Polygons:', min=3, max=20, value=4, step=1, field=True)
    cmds.separator(h=10, style='none')

    cmds.separator(h=10, style='none')
    treeDepthField = cmds.intSliderGrp(label='Tree depth:', min=1, max=8, value=3, step=1, field=True)
    cmds.separator(h=10, style='none')  # last column last row is blank

    cmds.separator(h=10, style='none')
    treeSegmentLength = cmds.floatSliderGrp(label='Segment length:', min=0.2, max=20, value=5, step=0.1, field=True)
    cmds.separator(h=10, style='none')  # last column last row is blank

    cmds.separator(h=10, style='none')
    treeLengthDecrease = cmds.floatSliderGrp(label='Length decrease:', min=0.0, max=1, value=0.8, step=0.01, field=True)
    cmds.separator(h=10, style='none')  # last column last row is blank

    cmds.separator(h=10, style='none')
    trunkRadius = cmds.floatSliderGrp(label='Trunk radius:', min=0.1, max=10, value=1, step=0.1, field=True)
    cmds.separator(h=10, style='none')  # last column last row is blank

    cmds.separator(h=10, style='none')
    radiusDecrease = cmds.floatSliderGrp(label='Radius decrease:', min=0.0, max=1, value=0.8, step=0.01, field=True)
    cmds.separator(h=10, style='none')  # last column last row is blank

    cmds.separator(h=10, style='none')
    treeBranches = cmds.intSliderGrp(label='Branches:', min=1, max=8, value=2, step=1, field=True)
    cmds.separator(h=10, style='none')  # last column last row is blank

    cmds.separator(h=10, style='none')
    treeBranches_a = cmds.floatSliderGrp(label='Branches angle:', min=0, max=math.pi, value=0.5, step=0.01,
                                         field=True)
    cmds.separator(h=10, style='none')  # last column last row is blank

    cmds.separator(h=10, style='none')
    treeFoliageSze = cmds.floatSliderGrp(label='Foliage size:', min=0.1, max=20, value=1, step=0.01, field=True)
    cmds.separator(h=10, style='none')  # last column last row is blank

    cmds.separator(h=10, style='none')
    treeFoliageRes = cmds.intSliderGrp(label='Foliage resolution:', min=3, max=30, value=5, step=0.01, field=True)
    cmds.separator(h=10, style='none')  # last column last row is blank

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
                                                               treeFoliageRes
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

    cmds.button(label='Cancel', command=cancelCallBack)
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
    create(tree_depth, 0,
           segment_length, length_dec, radius, radius_d,
           0.0, 1.0, 0.0,
           0.0, 0.0, 0.0,
           0.0, 0.0, 0.0,
           polycount, branches, branches_a, foliage_s, foliage_r, 0.0, True
           )


createUI('miniTree', applyCallBack)


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


def polytube(p1_x, p1_y, p1_z,
             p2_x, p2_y, p2_z,
             p0_x, p0_y, p0_z,
             p1_r, p2_r,
             polys):
    for i in range(0, polys):
        inc = math.pi * 2.0 / polys
        # points are being repositioned before rotation

        point1 = PointRotate3D(p0_x, p0_y,p0_z,
                               p1_x, p1_y,p1_z,
                               p1_x + p1_r, p1_y, p1_z,  
                               -(inc*i)
                               )
        point2 = PointRotate3D(p0_x, p0_y,p0_z,
                               p1_x, p1_y,p1_z,
                               p1_x + p1_r, p1_y, p1_z,  
                               -(inc * i + inc)
                               )
        point3 = PointRotate3D(p1_x, p1_y,p1_z,
                               p2_x, p2_y,p2_z,
                               p2_x + p2_r, p2_y, p2_z,   
                               -(inc * i)
                               )
        point4 = PointRotate3D(p1_x, p1_y,p1_z,
                               p2_x, p2_y,p2_z, 
                               p2_x + p2_r, p2_y, p2_z,   
                               -(inc * i + inc)
                               )

        cmds.polyCreateFacet(p=[point2,
                                point1,
                                point3,
                                point4])


def create(p_depth, p_min_depth,
           p_length, p_length_inc, p_r, p_rate,
           p_lx, p_ly, p_lz,
           p_llx, p_lly, p_llz,
           branch_ax, branch_ay, branch_az,
           polygons, num_branches, branch_ang, foliage_sze, foliage_res, turn, branch):
    if p_depth > p_min_depth:
        
        #get vector of last segment
        p_lxv = p_lx - p_llx
        p_lyv = p_ly - p_lly
        p_lzv = p_lz - p_llz
        
        # find the magnitude of vector p_lx, p_ly, p_lz
        m = math.sqrt(math.pow(p_lxv, 2) + math.pow(p_lyv, 2) + math.pow(p_lzv, 2))

        # divide the vector by its magnitude to get unit vector
        ux = p_lxv / m
        uy = p_lyv / m
        uz = p_lzv / m

        # now we add unit vector (multiplied by length) to the values to create new points
        p_vx = p_lxv + p_llx + (ux * p_length)
        p_vy = p_lyv + p_lly + (uy * p_length)
        p_vz = p_lzv + p_llz + (uz * p_length)
        
        #if p_depth < 2: 
            #branch = False 
            
        if branch: 
            points = PointRotate3D(p_lx, p_ly, p_lz, 
                                    p_lx+1, p_ly,  p_lz, 
                                    p_vx, p_vy, p_vz, 
                                    branch_ax)
            yTurn = PointRotate3D(p_lz, p_ly, p_lz,
                                  p_vx, p_vy, p_vz,
                                  points[0], points[1], points[2],
                                  branch_ay)
    
            p_nx = yTurn[0]
            p_ny = yTurn[1]
            p_nz = yTurn[2]
            
            p_nax = branch_ax 
            p_nay = branch_ay
        else: 
            p_nx = p_vx
            p_ny = p_vy 
            p_nz = p_vz

        # create a tube using the old and new points the angles control the tilt of the base and the top of the segment
        polytube(
            p_lx, p_ly, p_lz,  # base point
            p_nx, p_ny, p_nz,  # top point
            p_llx, p_lly, p_llz,  
            p_r, p_r * p_rate,  # base and top radius
            polygons)

        # reducing length and radius for a new segment, counting depth
        p_length = p_length * p_length_inc
        p_r = p_r * p_rate
        p_depth = p_depth - 1.0
        
        p_llx = p_lx 
        p_lly = p_ly 
        p_llz = p_lz 
        
        p_lx = p_nx
        p_ly = p_ny
        p_lz = p_nz

        if p_depth > p_min_depth:
            branch_ax = branch_ang
            turn = turn + math.pi / 2.0
            branch_az = 0
            print turn
            for i in range(0, num_branches):
                branch_ay = ((i) * ((math.pi * 2.0) / num_branches)) + turn

                create(p_depth, p_min_depth, p_length, p_length_inc, p_r, p_rate,
                       p_lx, p_ly, p_lz,
                       p_llx, p_lly, p_llz,
                       branch_ax, branch_ay, branch_az,
                       polygons, num_branches, branch_ang, foliage_sze, foliage_res, turn, branch)
                
        else:
            my_sphere = cmds.polySphere(r=foliage_sze, sa=foliage_res, sh=foliage_res, name='leaves#')
            cmds.move(p_lx, p_ly, p_lz, my_sphere)




