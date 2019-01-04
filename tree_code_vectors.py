import maya.cmds as cmds
import math
import random
import functools


def create_ui(pWindowTitle, pApplyCallBack):
    windowID = 'miniTree'  # unique id to make sure only one is open at a time
    if cmds.window(windowID, exists=True):
        cmds.deleteUI(windowID)

    cmds.window(windowID, title=pWindowTitle, sizeable=False, resizeToFitChildren=True)
    cmds.rowColumnLayout(numberOfColumns=1, adj=True)
    logopath = cmds.internalVar(upd=True) + "icons/mini_tree_logo.png"
    cmds.image(image=logopath)
    form = cmds.formLayout()
    tabs = cmds.tabLayout(innerMarginWidth=5, innerMarginHeight=5)
    cmds.formLayout(form, edit=True,
                    attachForm=((tabs, 'top', 0), (tabs, 'left', 0), (tabs, 'bottom', 0), (tabs, 'right', 0)))

    child1 = cmds.rowColumnLayout(numberOfColumns=1)

    cmds.separator(h=10, style='none')
    polyNumberField = cmds.intSliderGrp(label='Polygons:', min=3, max=20, value=4, step=1, field=True)
    treeDepthField = cmds.intSliderGrp(label='Tree depth:', min=1, max=8, value=3, step=1, field=True)
    treeSegmentLength = cmds.floatSliderGrp(label='Segment length:', min=0.2, max=20, value=5, step=0.1, field=True)
    treeFirstSegmentLength = cmds.floatSliderGrp(label='First segment multiplier:', min=0.1, max=5, value=1, step=0.1,
                                                 field=True)
    treeLengthDecrease = cmds.floatSliderGrp(label='Length decrease:', min=0.0, max=1, value=0.8, step=0.01, field=True)
    trunkRadius = cmds.floatSliderGrp(label='Trunk radius:', min=0.1, max=10, value=1, step=0.1, field=True)
    radiusDecrease = cmds.floatSliderGrp(label='Radius decrease:', min=0.0, max=1, value=0.45, step=0.01, field=True)
    treeBranches = cmds.intSliderGrp(label='Branches:', min=1, max=8, value=2, step=1, field=True)
    treeBranches_a = cmds.floatSliderGrp(label='Branches angle:', min=0, max=math.pi, value=0.5, step=0.01,
                                         field=True)
    treeColor = cmds.colorSliderGrp(label='Tree color:', rgb=(0.4, 0.3, 0.3))
    cmds.separator(h=10, style='none')

    cmds.setParent('..')

    child2 = cmds.rowColumnLayout(numberOfColumns=1, adj=True)

    cmds.separator(h=10, style='none')
    treeFoliageNumber = cmds.intSliderGrp(label='Foliage number:', min=1, max=20, value=1, step=1, field=True)
    treeFoliageSpread = cmds.floatSliderGrp(label='Foliage spread:', min=0, max=5, value=0, step=0.01, field=True)
    treeFoliageSze = cmds.floatSliderGrp(label='Foliage size:', min=0.1, max=6, value=1, step=0.01, field=True)
    treeFoliageRes = cmds.intSliderGrp(label='Foliage resolution:', min=0, max=4, value=1, step=1, field=True)
    foliageColor = cmds.colorSliderGrp(label='Foliage color:', rgb=(0.30, 0.7, 0.40))
    cmds.separator(h=10, style='none')

    cmds.setParent('..')

    cmds.tabLayout(tabs, edit=True, tabLabel=((child1, 'Tree'), (child2, 'Foliage')))
    cmds.setParent('..')
    cmds.setParent('..')

    cmds.rowColumnLayout(numberOfColumns=1, adj=True)

    treeTypeSelect = cmds.radioButtonGrp(label='Tree type', sl = 1, labelArray2=['Normal', 'Pine'], numberOfRadioButtons=2)
    cmds.separator(h=10, style='none')

    def changeTextFld(*args):
        cmds.intFieldGrp(randomSeed, edit=True, v1=random.randint(0, 9999))

    cmds.separator(h=10, style='none')
    cmds.separator(h=10, style='none')
    randomSeed = cmds.intFieldGrp(label='Seed:', numberOfFields=1, value1=1234)
    cmds.button(label='Randomize seed', command=changeTextFld)
    cmds.setParent('..')
    cmds.rowColumnLayout(numberOfColumns=1, adj=True)
    cmds.separator(h=10, style='none')
    cmds.separator(h=10, style='none')
    cmds.button(label='Create tree', align='center', command=functools.partial(pApplyCallBack,
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
                                                                               randomSeed,
                                                                               foliageColor,
                                                                               treeColor,
                                                                               treeFoliageNumber,
                                                                               treeFoliageSpread,
                                                                               treeFirstSegmentLength,
                                                                               treeTypeSelect
                                                                               ))
    cmds.separator(h=10, style='none')
    cmds.separator(h=10, style='none')

    def cancelCallBack(*pArgs):
        if cmds.window(windowID, exists=True):
            cmds.deleteUI(windowID)

    # cmds.button(label='Cancel', command=cancelCallBack)
    cmds.showWindow()


def apply_call_back(pPolyNumberField,
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
                    pFoliageC,
                    pTreeC,
                    pFoliageN,
                    pFoliageSpread,
                    pFirstSegmentL,
                    pTreeType,
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
    p_seed = cmds.intFieldGrp(pSeed, query=True, value=True)
    treeCor = cmds.colorSliderGrp(pTreeC, query=True, rgbValue=True)
    foliageCor = cmds.colorSliderGrp(pFoliageC, query=True, rgbValue=True)
    foliage_n = cmds.intSliderGrp(pFoliageN, query=True, value=True)
    foliage_spread = cmds.floatSliderGrp(pFoliageSpread, query=True, value=True)
    first_segment_l = cmds.floatSliderGrp(pFirstSegmentL, query=True, value=True)
    tree_type = cmds.radioButtonGrp(pTreeType, query=True, select=True)
    
    cmds.setAttr(treeTrunkShader + '.color', treeCor[0], treeCor[1], treeCor[2], type='double3')
    # cmds.connectAttr( treeTrunkShader+'.outColor', treeTrunkShaderSG+'.surfaceShader', f=1) 
    cmds.setAttr(foliageShader + '.color', foliageCor[0], foliageCor[1], foliageCor[2], type='double3')
    # cmds.connectAttr( foliageShader+'.outColor', foliageShaderSG+'.surfaceShader', force=True)

    random.seed(p_seed[0])
    delete_previous()
    if tree_type == 1:
        create(tree_depth,
               segment_length, length_dec, radius, radius_d,
               [0.0, 1.0, 0.0],
               [0.0, 0.0, 0.0],
               0.0, 0.0,
               polycount, branches, branches_a,
               foliage_s, foliage_r, 0.0, True, foliage_n, foliage_spread, first_segment_l
               )
    if tree_type == 2: 
        createPine(tree_depth,
               segment_length, length_dec, radius, radius_d,
               [0.0, 1.0, 0.0],
               [0.0, 0.0, 0.0],
               0.0, 0.0,
               polycount, branches, branches_a,
               foliage_s, foliage_r, 0.0, True, foliage_n, foliage_spread, first_segment_l, 1
               )

    merge_tree()


def delete_previous():
    segmentsList = cmds.ls('miniTreeTrunk*')
    foliageList = cmds.ls('miniTreeFoliage*')
    if len(segmentsList) > 0:
        cmds.delete(segmentsList)
    if len(foliageList) > 0:
        cmds.delete(foliageList)


def merge_tree():
    segmentsList = cmds.ls('treePart*')
    foliageList = cmds.ls('leaves*')

    if len(segmentsList) < 3:
        treeTrunk = segmentsList[0]
    else:
        treeTrunk = cmds.polyUnite(segmentsList)
        
    newTree = cmds.duplicate(treeTrunk, name='miniTreeTrunk')
    cmds.polyMergeVertex(newTree)
    cmds.sets(newTree, e=1, forceElement=treeTrunkShaderSG)
    cmds.delete(treeTrunk)

    if len(foliageList) < 3:
        leaves = foliageList[0]
    else:
        leaves = cmds.polyUnite(foliageList)
        
    newLeaves = cmds.duplicate(leaves, name='miniTreeFoliage')
    cmds.sets(newLeaves, e=1, forceElement=foliageShaderSG)
    cmds.delete(leaves)

    segmentsList = cmds.ls('treePart*')
    if len(segmentsList) > 0:
        cmds.delete(segmentsList)

    foliageList = cmds.ls('leaves*')
    if len(foliageList) > 0:
        cmds.delete(foliageList)


# Arguments: 'axis point 1', 'axis point 2', 'point to be rotated', 'angle of rotation (in radians)' >> 'new point'
def point_rotate_3d(p1_x, p1_y, p1_z, p2_x, p2_y, p2_z, p0_x, p0_y, p0_z, theta):
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


def get_sp_point(a, b, c):
    # first convert line to normalized unit vector
    dx = b[0] - a[0]
    dy = b[1] - a[1]
    dz = b[2] - a[2]
    mag = math.sqrt(dx * dx + dy * dy + dz * dz)
    dx = dx / mag
    dy = dy / mag
    dz = dz / mag
    # translate the point and get the dot product
    theta = (dx * (c[0] - a[0])) + (dy * (c[1] - a[1])) + (dz * (c[2] - a[2]))
    x4 = (dx * theta) + a[0]
    y4 = (dy * theta) + a[1]
    z4 = (dz * theta) + a[2]
    return [x4, y4, z4]


def get_point_given_dist(a, b, dist):
    # """Return the point c such that line segment bc is perpendicular to
    # line segment ab and segment bc has length dist.
    # a and b are tuples of length 3, dist is a positive float.
    vec_ab = (b[0] - a[0], b[1] - a[1], b[2] - a[2])
    # Find a vector not parallel or anti-parallel to vector ab
    if vec_ab[1] != 0 or vec_ab[2] != 0:
        vec = (1, 0, 0)
    else:
        vec = (0, 1, 0)
    # Find the cross product of the vectors
    cross = (vec_ab[1] * vec[2] - vec_ab[2] * vec[1],
             vec_ab[2] * vec[0] - vec_ab[0] * vec[2],
             vec_ab[0] * vec[1] - vec_ab[1] * vec[0])
    # Find the vector in the same direction with length dist
    factor = dist / math.sqrt(cross[0] ** 2 + cross[1] ** 2 + cross[2] ** 2)
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

        p = get_point_given_dist([p0_x, p0_y, p0_z], [p1_x, p1_y, p1_z], p1_r)
        point1 = point_rotate_3d(p0_x, p0_y, p0_z,
                                 p1_x, p1_y, p1_z,
                                 p[0], p[1], p[2],
                                 -(inc * i)
                                 )
        point2 = point_rotate_3d(p0_x, p0_y, p0_z,
                                 p1_x, p1_y, p1_z,
                                 p[0], p[1], p[2],
                                 -(inc * i + inc)
                                 )
        p = get_point_given_dist([p1_x, p1_y, p1_z], [p2_x, p2_y, p2_z], p2_r)
        point3 = point_rotate_3d(p1_x, p1_y, p1_z,
                                 p2_x, p2_y, p2_z,
                                 p[0], p[1], p[2],
                                 -(inc * i)
                                 )
        point4 = point_rotate_3d(p1_x, p1_y, p1_z,
                                 p2_x, p2_y, p2_z,
                                 p[0], p[1], p[2],
                                 -(inc * i + inc)
                                 )

        cmds.polyCreateFacet(p=[point2,
                                point1,
                                point3,
                                point4],
                             name='treePart#')


def create(p_depth,  # tree depth,
           p_length, p_length_inc, p_r, p_rate,
           p_l,  # last segment tip
           p_ll,  # last segment base
           branch_turn, branch_shift,
           polygons, num_branches, branch_ang, foliage_sze, foliage_res, turn, branch, foliage_num, foliage_spr,
           first_segment_l):
    if p_depth > 0:

        branch_length = p_length * first_segment_l

        # get vector of last segment
        lv = [p_l[0] - p_ll[0], p_l[1] - p_ll[1], p_l[2] - p_ll[2]]
        # find the magnitude of vector p_lx, p_ly, p_lz
        m = math.sqrt(math.pow(lv[0], 2) + math.pow(lv[1], 2) + math.pow(lv[2], 2))
        # divide the vector by its magnitude to get unit vector
        u = [lv[0] / m, lv[1] / m, lv[2] / m]
        # now we add unit vector (multiplied by length) to the values to create new points
        v = [lv[0] + p_ll[0] + (u[0] * branch_length), lv[1] + p_ll[1] + (u[1] * branch_length),
             lv[2] + p_ll[2] + (u[2] * branch_length)]

        if random.uniform(0, 1) < 0.1:
            branch = False
        if random.uniform(0, 1) < 0.1:
            p_depth = 0

        if branch:
            newP = [p_l[0] + 0.1, p_l[1], p_l[2]]
            p = get_sp_point(p_l, p_ll, newP)
            points = point_rotate_3d(p[0], p[1], p[2],
                                     newP[0], newP[1], newP[2],
                                     v[0], v[1], v[2],
                                     branch_turn)
            yTurn = point_rotate_3d(p_l[0], p_l[1], p_l[2],
                                    v[0], v[1], v[2],
                                    points[0], points[1], points[2],
                                    branch_shift)
            p_n = yTurn
        else:
            p_n = v

        # create a tube using the old and new points the angles control the tilt of the base and the top of the segment
        polytube(
            p_l[0], p_l[1], p_l[2],  # base point
            p_n[0], p_n[1], p_n[2],  # top point
            p_ll[0], p_ll[1], p_ll[2],
            p_r, p_r * p_rate,  # base and top radius
            polygons)

        # reducing length and radius for a new segment, counting depth
        p_length = (p_length * p_length_inc)
        p_r = p_r * p_rate
        p_depth = p_depth - 1.0

        if p_depth > 0:
            branch_turn = branch_ang
            turn = turn + math.pi / 2.0
            for i in range(0, num_branches):
                p_length = p_length + random.uniform(-0.5, 0.5)
                if random.uniform(0, 1) < 0.9:
                    turn = turn + random.uniform(-math.pi / 2, math.pi / 2)
                if random.uniform(0, 1) < 0.9:
                    branch_turn = branch_turn + random.uniform(-math.pi / 6, math.pi / 6)

                branch_shift = (i * ((math.pi * 2.0) / num_branches)) + turn
                create(p_depth, p_length, p_length_inc, p_r, p_rate,
                       p_n,
                       p_l,
                       branch_turn, branch_shift,
                       polygons, num_branches, branch_ang,
                       foliage_sze, foliage_res, turn, branch, foliage_num, foliage_spr, 1)

        else:
            randx = []
            randy = []  # i am creating random lists because otherwise changing the number of foliage would affect the seed
            randz = []
            for r in range(0, 20):
                randx.append(random.uniform(-foliage_spr, foliage_spr))
                randy.append(random.uniform(-foliage_spr, foliage_spr))
                randz.append(random.uniform(-foliage_spr, foliage_spr))
            for j in range(0, foliage_num):
                my_sphere = cmds.polyPlatonicSolid(l=foliage_sze, name='leaves#')
                for i in range(0, foliage_res):
                    cmds.polySmooth(my_sphere)
                cmds.move(p_n[0] + randx[j],
                          p_n[1] + randy[j],
                          p_n[2] + randz[j], my_sphere)

def createPine(p_depth,  # tree depth,
           p_length, p_length_inc, p_r, p_rate,
           p_l,  # last segment tip
           p_ll,  # last segment base
           branch_turn, branch_shift,
           polygons, num_branches, branch_ang, foliage_sze, foliage_res, turn, branch, foliage_num, foliage_spr,
           first_segment_l, pine_level):
    if p_depth > 0:

        branch_length = p_length * first_segment_l

        # get vector of last segment
        lv = [p_l[0] - p_ll[0], p_l[1] - p_ll[1], p_l[2] - p_ll[2]]
        # find the magnitude of vector p_lx, p_ly, p_lz
        m = math.sqrt(math.pow(lv[0], 2) + math.pow(lv[1], 2) + math.pow(lv[2], 2))
        # divide the vector by its magnitude to get unit vector
        u = [lv[0] / m, lv[1] / m, lv[2] / m]
        # now we add unit vector (multiplied by length) to the values to create new points
        v = [lv[0] + p_ll[0] + (u[0] * branch_length), lv[1] + p_ll[1] + (u[1] * branch_length),
             lv[2] + p_ll[2] + (u[2] * branch_length)]

        if pine_level == 3 or pine_level ==2 :
            newP = [p_l[0] + 0.1, p_l[1], p_l[2]]
            p = get_sp_point(p_l, p_ll, newP)

            points = point_rotate_3d(p[0], p[1], p[2],
                                     newP[0], newP[1], newP[2],
                                     v[0], v[1], v[2],
                                     branch_turn)
            yTurn = point_rotate_3d(p_l[0], p_l[1], p_l[2],
                                     v[0], v[1], v[2],
                                     points[0], points[1], points[2],
                                     branch_shift)
            
            p_n = yTurn
            
            
            
        else:
            p_n = v

        # create a tube using the old and new points the angles control the tilt of the base and the top of the segment
        polytube(
            p_l[0], p_l[1], p_l[2],  # base point
            p_n[0], p_n[1], p_n[2],  # top point
            p_ll[0], p_ll[1], p_ll[2],
            p_r, p_r * p_rate,  # base and top radius
            polygons)

        # reducing length and radius for a new segment, counting depth
        p_length = (p_length * p_length_inc)
        p_r = p_r * p_rate
        p_depth = p_depth - 1.0
        
        if pine_level == 1:
            createPine(p_depth, p_length, p_length_inc, p_r, p_rate,
                       p_n,
                       p_l,
                       branch_turn, branch_shift,
                       polygons, num_branches, branch_ang,
                       foliage_sze, foliage_res, turn, branch, foliage_num, foliage_spr, 1, 1)
        
                        
        if p_depth > 0:
            branch_turn = branch_ang
            turn = turn + math.pi / 2.0
            for i in range(0, num_branches):
                p_length = p_length + random.uniform(-0.5, 0.5)
                if random.uniform(0, 1) < 0.9:
                    turn = turn + random.uniform(-math.pi / 2, math.pi / 2)
                if random.uniform(0, 1) < 0.9:
                    branch_turn = branch_turn + random.uniform(-math.pi / 6, math.pi / 6)

                branch_shift = (i * ((math.pi * 2.0) / num_branches)) + turn
                createPine(p_depth * 0.5, p_length  *0.7, p_length_inc, p_r, p_rate,
                       p_n,
                       p_l,
                       branch_turn, branch_shift,
                       polygons, num_branches, branch_ang,
                       foliage_sze, foliage_res, turn, branch, foliage_num, foliage_spr, 1, 2)

        else:
            randx = []
            randy = []  # i am creating random lists because otherwise changing the number of foliage would affect the seed
            randz = []
            for r in range(0, 20):
                randx.append(random.uniform(-foliage_spr, foliage_spr))
                randy.append(random.uniform(-foliage_spr, foliage_spr))
                randz.append(random.uniform(-foliage_spr, foliage_spr))
            for j in range(0, foliage_num):
                my_sphere = cmds.polyPlatonicSolid(l=foliage_sze, name='leaves#')
                for i in range(0, foliage_res):
                    cmds.polySmooth(my_sphere)
                cmds.move(p_n[0] + randx[j],
                          p_n[1] + randy[j],
                          p_n[2] + randz[j], my_sphere)

create_ui('miniTree', apply_call_back)

# Create a new trunk shader
treeTrunkShader = cmds.shadingNode('lambert', asShader=True)
cmds.setAttr(treeTrunkShader + '.color', 0.4, 0.3, 0.3, type='double3')
treeTrunkShaderSG = cmds.sets(renderable=1, noSurfaceShader=1, empty=1, name='treeTrunkShaderSG');
cmds.connectAttr(treeTrunkShader + '.outColor', treeTrunkShaderSG + '.surfaceShader', f=1)

# Create a new foliage shader
foliageShader = cmds.shadingNode('lambert', asShader=True)
cmds.setAttr(foliageShader + '.color', 0.30, 0.7, 0.40, type='double3')
foliageShaderSG = cmds.sets(renderable=True, noSurfaceShader=True, empty=True, name='foliageShaderSG');
cmds.connectAttr(foliageShader + '.outColor', foliageShaderSG + '.surfaceShader', force=True)

