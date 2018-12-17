import maya.cmds as cmds
import math
import random
import functools


def createUI(pWindowTitle, pApplyCallBack):
    windowID = 'miniTree'  # unique id to make sure only one is open at a time
    if cmds.window(windowID, exists=True):
        cmds.deleteUI(windowID)

    cmds.window(windowID, title=pWindowTitle, sizeable=False, resizeToFitChildren=True)
    cmds.rowColumnLayout(numberOfColumns=3, columnWidth=[(1, 80), (2, 200), (3, 60)], columnOffset=[(1, 'right', 3)])
    cmds.text(label='Polygons:')
    polyNumberField = cmds.intSliderGrp(min=3, max=20, value=4, step=1, field = True)
    cmds.separator(h=10, style='none')

    cmds.text(label='Tree depth:')
    treeDepthField = cmds.intSlider(min=1, max=8, value=3, step=1)
    cmds.separator(h=10, style='none')  # last column last row is blank

    cmds.separator(h=10, style='none')  # empty row
    cmds.separator(h=10, style='none')
    cmds.separator(h=10, style='none')

    cmds.separator(h=10, style='none')
    cmds.button(label='Create tree', command=functools.partial(pApplyCallBack,
                                                         polyNumberField,
                                                         treeDepthField
                                                         ))  # when the button is pressed, callback function is called

    def cancelCallBack(*pArgs):
        if cmds.window(windowID, exists=True):
            cmds.deleteUI(windowID)

    cmds.button(label='Cancel', command=cancelCallBack)
    cmds.showWindow()


def applyCallBack(pPolyNumberField, pTreeDepthField, *pArgs):
    polycount = cmds.intSliderGrp(pPolyNumberField, query=True, value=True)
    tree_depth = cmds.intSlider(pTreeDepthField, query=True, value=True)
    create(tree_depth, 0, 5, 0.5, 1, 0.1, 0.7,
           0, 0, 0,
           math.pi + math.pi / 2, math.pi / 2, math.pi / 2,
           math.pi + math.pi / 2, math.pi / 2, math.pi / 2,
           1, polycount, 2, math.pi / 2
           )


createUI('miniTree', applyCallBack)


def get_rotations(px, py, pz,
                  pax, pay, paz,
                  paxx, paxy, paxz):
    # location - axis of rotation
    x = px - paxx
    y = py - paxy
    z = pz - paxz
    # z rotation
    x1 = x * math.cos(paz) - y * math.sin(paz)
    y1 = x * math.sin(paz) + y * math.cos(paz)
    z1 = z
    # y rotation
    z11 = z1 * math.cos(pay) - x1 * math.sin(pay)
    x11 = z1 * math.sin(pay) + x1 * math.cos(pay)
    y11 = y1
    # x rotation
    y111 = y11 * math.cos(pax) - z11 * math.sin(pax)
    z111 = y11 * math.sin(pax) + z11 * math.cos(pax)
    x111 = x11

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
        inc = math.pi * 2 / polys
        # points are being repositioned before rotation
        point1 = get_rotations(p1_x + p1_r * math.cos(inc * i),  # xyz of the point to be rotated
                               p1_y,
                               p1_z + p1_r * math.sin(inc * i),
                               a1_x, a1_y, a1_z,  # xyz angles of the rotation
                               p1_x, p1_y, p1_z  # axis of the rotation
                               )
        point2 = get_rotations(p1_x + p1_r * math.cos(inc * i + inc),
                               p1_y,
                               p1_z + p1_r * math.sin(inc * i + inc),
                               a1_x, a1_y, a1_z,
                               p1_x, p1_y, p1_z
                               )
        point3 = get_rotations(p2_x + p2_r * math.cos(inc * i),
                               p2_y,
                               p2_z + p2_r * math.sin(inc * i),
                               a2_x, a2_y, a2_z,
                               p1_x, p1_y, p1_z
                               )
        point4 = get_rotations(p2_x + p2_r * math.cos(inc * i + inc),
                               p2_y,
                               p2_z + p2_r * math.sin(inc * i + inc),
                               a2_x, a2_y, a2_z,
                               p1_x, p1_y, p1_z
                               )

        cmds.polyCreateFacet(p=[point2,
                                point1,
                                point3,
                                point4])


# create a tree (depth of tree, min depth of tree = 0,
#                length of a segment, decrease of segment length, radius of segment, radius decrease rate, min radius,
#                xyz positions,
#                angle of segment
#                axis of rotation of segment
#                boolean switch, polycount per segment, number of branches per segment, angle of branches)
def create(p_depth, p_min_depth,
           p_length, p_length_inc, p_r, p_rate, p_min_r,
           p_lx, p_ly, p_lz,
           p_lax, p_lay, p_laz,
           p_nax, p_nay, p_naz,
           switch, polygons, num_branches, branch_ang):
    if p_depth > p_min_depth:
        p_length = p_length - p_length_inc
        p_nx = p_lx
        p_ny = p_ly + p_length
        p_nz = p_lz
        polytube(
            p_lx, p_ly, p_lz,
            p_nx, p_ny, p_nz,
            p_r, p_r - p_rate,
            p_lax, p_lay, p_laz,
            p_nax, p_nay, p_naz,
            polygons)

        point = get_rotations(p_nx, p_ny, p_nz, p_nax, p_nay, p_naz, p_lx, p_ly, p_lz)

        p_lx = point[0]
        p_ly = point[1]
        p_lz = point[2]

        p_r = p_r - p_rate
        p_depth = p_depth - 1

        p_lax = p_nax
        p_lay = p_nay
        p_laz = p_naz

        switch = switch * -1

        for i in range(0, num_branches):
            ang_split = p_nax
            ang_turn = p_nay
            if switch > 0:
                ang_split = (p_nax - branch_ang) + (branch_ang / num_branches) * (i + (num_branches + 1.0) / 2.0)
            else:
                ang_turn = (p_nay - branch_ang) + (branch_ang / num_branches) * (i + (num_branches + 1.0) / 2.0)
            create(p_depth, p_min_depth, p_length, p_length_inc, p_r, p_rate, p_min_r,
                   p_lx, p_ly, p_lz,
                   p_lax, p_lay, p_laz,
                   ang_split, ang_turn, p_naz,
                   switch, polygons, num_branches, branch_ang)
    else:
        my_sphere = cmds.polySphere(r=random.uniform(p_r * 2, p_r * 4), sa=5, sh=5, name='leaves#')
        cmds.move(p_lx, p_ly, p_lz, my_sphere)
