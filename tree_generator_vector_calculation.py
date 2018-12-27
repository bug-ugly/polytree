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
           0.0, 0.0, 0.0,
           polycount, branches, branches_a, foliage_s, foliage_r , 0.0
           )


createUI('miniTree', applyCallBack)


def get_rotations(px, py, pz,
                  pax, pay, paz,
                  paxx, paxy, paxz,
                  nonegative):
    # location - axis of rotation
    x = px - paxx
    y = py - paxy
    z = pz - paxz
    
    if nonegative: 
        if x < 0: 
            x = x*-1
        if y < 0: 
            y = y*-1
        if z < 0: 
            z = z*-1
    # z rotation
    x1 = x * math.cos(paz) - y * math.sin(paz)
    y1 = x * math.sin(paz) + y * math.cos(paz)
    z1 = z

    # x rotation
    y11 = y1 * math.cos(pax) - z1 * math.sin(pax)
    z11 = y1 * math.sin(pax) + z1 * math.cos(pax)
    x11 = x1

    # y rotation
    z111 = z11 * math.cos(pay) - x11 * math.sin(pay)
    x111 = z11 * math.sin(pay) + x11 * math.cos(pay)
    y111 = y11

    # adding axis of rotation again
    final = [x111 + paxx, y111 + paxy, z111 + paxz]
    return final


def polytube(p1_x, p1_y, p1_z,
             p2_x, p2_y, p2_z,
             p1_r, p2_r,
             a1_x, a1_y, a1_z,
             a2_x, a2_y, a2_z,
             polys):
    for i in range(0, polys):
        inc = math.pi * 2.0 / polys
        # points are being repositioned before rotation
        
        point1 = get_rotations(p1_x + p1_r * math.cos(inc * i),  # xyz of the point to be rotated
                               p1_y,
                               p1_z + p1_r * math.sin(inc * i),
                               a1_x, a1_y, a1_z,  # xyz angles of the rotation
                               p1_x, p1_y, p1_z,  # axis of the rotation
                               False)
        point2 = get_rotations(p1_x + p1_r * math.cos(inc * i + inc),
                               p1_y,
                               p1_z + p1_r * math.sin(inc * i + inc),
                               a1_x, a1_y, a1_z,
                               p1_x, p1_y, p1_z,
                               False
                               )
        point3 = get_rotations(p2_x + p2_r * math.cos(inc * i),
                               p2_y,
                               p2_z + p2_r * math.sin(inc * i),
                               a2_x, a2_y, a2_z,
                               p2_x, p2_y, p2_z,
                               False
                               )
        point4 = get_rotations(p2_x + p2_r * math.cos(inc * i + inc),
                               p2_y,
                               p2_z + p2_r * math.sin(inc * i + inc),
                               a2_x, a2_y, a2_z,
                               p2_x, p2_y, p2_z,
                               False
                               )

        cmds.polyCreateFacet(p=[point2,
                                point1,
                                point3,
                                point4])


# create a tree (depth of tree, min depth of tree = 0,
#                length of a segment, decrease of segment length, radius of segment, radius decrease rate,
#                xyz positions,
#                angle of segment
#                axis of rotation of segment
#                boolean switch, polycount per segment, number of branches per segment, angle of branches)
def create(p_depth, p_min_depth,
           p_length, p_length_inc, p_r, p_rate,
           p_lx, p_ly, p_lz,
           p_lax, p_lay, p_laz,
           p_nax, p_nay, p_naz,
           branch_ax, branch_ay, branch_az,
           polygons, num_branches, branch_ang, foliage_sze, foliage_res, turn):
    
    if p_depth > p_min_depth:

        # we are going to find the magnitude of vector p_lx, p_ly, p_lz
        m = math.sqrt(math.pow(p_lx, 2) + math.pow(p_ly, 2) + math.pow(p_lz, 2))

        # divide the vector by its magnitude to get unit vector
        ux = p_lx / m
        uy = p_ly / m
        uz = p_lz / m

        # now we add unit vector (multiplied by length) to the values to create new points
        p_vx = p_lx + (ux * p_length)
        p_vy = p_ly + (uy * p_length)
        p_vz = p_lz + (uz * p_length)
        
        points = get_rotations(p_vx ,p_vy, p_vz, branch_ax, branch_ay, 0.0, p_lx, p_ly, p_lz, True) 
        
        p_nx = points[0]
        p_ny = points[1]
        p_nz = points[2] 
            

        # create a tube using the old and new points the angles control the tilt of the base and the top of the segment
        polytube(
            p_lx, p_ly, p_lz,  # base point
            p_nx, p_ny, p_nz,  # top point
            p_r, p_r * p_rate,  # base and top radius
            p_lax, p_lay, p_laz,  # base tilt
            p_nax, p_nay, p_naz,  # top tilt
            polygons)

        # reducing length and radius for a new segment, counting depth
        p_length = p_length * p_length_inc
        p_r = p_r * p_rate
        p_depth = p_depth - 1.0

        p_lx = p_nx
        p_ly = p_ny
        p_lz = p_nz

        p_lax = p_nax
        p_lay = p_nay
        p_laz = p_naz
        
        branch = True 
        
        
        if p_depth > p_min_depth:
            branch_ax =  branch_ang
            turn = turn + math.pi/2.0
            print turn
            for i in range(0, num_branches):
                
                branch_ay = i* math.pi*2.0/num_branches + turn

                create(p_depth, p_min_depth, p_length, p_length_inc, p_r, p_rate,
                       p_lx, p_ly, p_lz,
                       p_lax, p_lay, p_laz,
                       p_nax, p_nay, p_naz,
                       branch_ax, branch_ay, branch_az,
                       polygons, num_branches, branch_ang, foliage_sze, foliage_res,turn)
        else:
            my_sphere = cmds.polySphere(r=foliage_sze, sa=foliage_res, sh=foliage_res, name='leaves#')
            cmds.move(p_lx, p_ly, p_lz, my_sphere)
