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

    child1 = cmds.rowColumnLayout(numberOfColumns=1, adj=True)

    cmds.separator(h=10, style='in')
    cmds.text( label='General', align='center' )
    cmds.separator(h=10, style='in')
    
    polyNumberField = cmds.intSliderGrp(label='Polygons:', min=3, max=20, value=4, step=1, field=True,
                                        annotation='Changes number of polygons in each tree segment')
    treeDepthField = cmds.intSliderGrp(label='Levels (tree size):', min=1, max=8, value=3, step=1, field=True,
                                       annotation='Changes number of branching levels')
    treeFirstSegmentLength = cmds.floatSliderGrp(label='Base length:', min=0.1, max=5, value=1, step=0.1,
                                                 field=True,
                                                 annotation='Increases/decreases the length of the first tree segment')                                   
    cmds.separator(h=10, style='in')
    cmds.text( label='Branch length', align='center' )
    cmds.separator(h=10, style='in')
    treeSegmentLength = cmds.floatSliderGrp(label='Length:', min=0.2, max=20, value=5, step=0.1, field=True,
                                            annotation='Changes the initial length of each branch')
    
    treeLengthDecrease = cmds.floatSliderGrp(label='Decrease:', min=0.0, max=1, value=0.8, step=0.01, field=True,
                                             annotation='Affects how the length of each branch decreases as the tree grows')
    cmds.separator(h=10, style='in')
    cmds.text( label='Trunk/branch radius', align='center' )
    cmds.separator(h=10, style='in')                                        
    trunkRadius = cmds.floatSliderGrp(label='Radius:', min=0.1, max=10, value=1, step=0.1, field=True,
                                      annotation='Changes the initial radius of the tree trunk')
    radiusDecrease = cmds.floatSliderGrp(label='Decrease:', min=0.0, max=1, value=0.45, step=0.01, field=True,
                                         annotation='Affects how the radius of the branches decreases as the tree grows')
    cmds.separator(h=10, style='in')
    cmds.text( label='Branching', align='center' )
    cmds.separator(h=10, style='in')                                          
    treeBranches = cmds.intSliderGrp(label='Max branches:', min=1, max=8, value=2, step=1, field=True,
                                     annotation='Changes the maximum number of branches that may occur when branching')
    treeBranches_a = cmds.floatSliderGrp(label='Branches angle:', min=0, max=math.pi, value=0.5, step=0.01,
                                         field=True, annotation='Manipulates the angle of braches')
    cmds.separator(h=10, style='in')
    cmds.text( label='Randomness', align='center' )
    cmds.separator(h=10, style='in')                                     
    branchingChance = cmds.floatSliderGrp(label='Branching chance:', min=0, max=1, value=0.9,
                                          step=0.01,
                                          field=True,
                                          annotation='Lower values increase a chance of a branch not appearing')
    cmds.separator(h=10, style='in')                                       
    branchAngleChance = cmds.floatSliderGrp(label='Angle shift shance:', min=0, max=1, value=0.9,
                                            step=0.01,
                                            field=True,
                                            annotation='Chance of a branch angle deviating from the angle of all other branches')
    branchAngleRAmount = cmds.floatSliderGrp(label='Angle random amount:', min=0, max=math.pi, value=math.pi / 6,
                                             step=0.01,
                                             field=True,
                                             annotation='Angle of how much a branch angle can change randomly')
    cmds.separator(h=10, style='in')                                                                                 
    branchTurnChance = cmds.floatSliderGrp(label='Turn shift chance:', min=0, max=1, value=0.9,
                                           step=0.01,
                                           field=True,
                                           annotation='Chance of a branch turn deviating from the turn of all other branches')
    branchTurnRAmount = cmds.floatSliderGrp(label='Turn random amount:', min=0, max=math.pi, value=math.pi / 2,
                                            step=0.01,
                                            field=True, annotation='Angle of how much a branch can turn randomly')
    
    cmds.separator(h=10, style='in')
    cmds.text( label='Colour', align='center' )
    cmds.separator(h=10, style='in')           
    treeColor = cmds.colorSliderGrp(label='Tree colour:', rgb=(0.4, 0.3, 0.3),
                                    annotation='Double click the colour to open the palette, changes tree colour')
    cmds.separator(h=10, style='none')

    cmds.setParent('..')

    child2 = cmds.rowColumnLayout(numberOfColumns=1, adj=True)

    cmds.separator(h=10, style='in')
    cmds.text( label='General', align='center' )
    cmds.separator(h=10, style='in')   
    treeFoliageSze = cmds.floatSliderGrp(label='Size:', min=0.1, max=6, value=1, step=0.01, field=True,
                                         annotation='Size of each foliage sphere')
    treeFoliageRes = cmds.intSliderGrp(label='Resolution:', min=0, max=4, value=1, step=1, field=True,
                                       annotation='Subdivides each of the foliage spheres')
    cmds.separator(h=10, style='in')
    cmds.text( label='More foliage', align='center' )
    cmds.separator(h=10, style='in')                                      
    treeFoliageNumber = cmds.intSliderGrp(label='Spheres number:', min=1, max=20, value=1, step=1, field=True,
                                          annotation='Number of foliage spheres per branch')
    treeFoliageSpread = cmds.floatSliderGrp(label='Randomise positions:', min=0, max=5, value=0, step=0.01, field=True,
                                            annotation='Randomise the foliage spheres position (necessary when changing foliage number)')

    cmds.separator(h=10, style='in')
    cmds.text( label='Colour', align='center' )
    cmds.separator(h=10, style='in')                                      
    foliageColor = cmds.colorSliderGrp(label='Foliage colour:', rgb=(0.30, 0.7, 0.40),
                                       annotation='Double click the colour to open the palette, changes foliage colour')
    cmds.separator(h=10, style='none')

    cmds.setParent('..')

    cmds.tabLayout(tabs, edit=True, tabLabel=((child1, 'Tree'), (child2, 'Foliage')))
    cmds.setParent('..')
    cmds.setParent('..')

    cmds.rowColumnLayout(numberOfColumns=1, adj=True)

    treeTypeSelect = cmds.radioButtonGrp(label='Tree type', sl=1, labelArray2=['Normal', 'Pine'],
                                         numberOfRadioButtons=2)
    cmds.separator(h=10, style='none')

    def changeTextFld(*args):
        cmds.intFieldGrp(randomSeed, edit=True, v1=random.randint(0, 9999))

    cmds.separator(h=10, style='none')
    cmds.separator(h=10, style='none')
    randomSeed = cmds.intFieldGrp(label='Seed:', numberOfFields=1, value1=9981,
                                  annotation='Number affecting random generation of the tree')
    cmds.separator(h=10, style='none')                              
    cmds.button(label='Randomize seed', command=changeTextFld, annotation='Changes seed value to a random value')
    cmds.setParent('..')
    cmds.rowColumnLayout(numberOfColumns=1, adj=True)
    cmds.separator(h=10, style='none')
    cmds.separator(h=10, style='none')

    cmds.button(label='Create tree', align='center', annotation='Create a tree using the above settings',
                command=functools.partial(pApplyCallBack,
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
                                          treeTypeSelect,
                                          branchingChance,
                                          branchAngleChance,
                                          branchTurnChance,
                                          branchTurnRAmount,
                                          branchAngleRAmount
                                          ))
    cmds.separator(h=10, style='none')
    cmds.separator(h=10, style='none')
    cmds.helpLine()

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
                    pBranchChance,
                    pAngleChance,
                    pTurnChance,
                    pTurnAmount,
                    pAngleAmount,
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
    branch_chance = cmds.floatSliderGrp(pBranchChance, query=True, value=True)
    angle_chance = cmds.floatSliderGrp(pAngleChance, query=True, value=True)
    turn_chance = cmds.floatSliderGrp(pTurnChance, query=True, value=True)
    turn_amount = cmds.floatSliderGrp(pTurnAmount, query=True, value=True)
    angle_amount = cmds.floatSliderGrp(pAngleAmount, query=True, value=True)

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
               foliage_s, foliage_r, 0.0, True, foliage_n, foliage_spread, first_segment_l,
               branch_chance, angle_chance, turn_chance, turn_amount, angle_amount
               )
    if tree_type == 2:
        createPine(tree_depth,
                   segment_length, length_dec, radius, radius_d,
                   [0.0, 1.0, 0.0],
                   [0.0, 0.0, 0.0],
                   0.0, 0.0,
                   polycount, branches, branches_a,
                   foliage_s, foliage_r, 0.0, True, foliage_n, foliage_spread, first_segment_l, 1, branch_chance,
                   angle_chance, turn_chance, turn_amount, angle_amount
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
           first_segment_l, branch_chance, angle_chance, turn_chance, turn_amount, angle_amount):
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

        c = 0
        if p_depth > 0:
            branch_turn = branch_ang
            turn = turn + math.pi / 2.0
            for i in range(0, num_branches):
                p_length = p_length + random.uniform(-0.5, 0.5)
                branch = True
                if random.uniform(0, 1) < turn_chance:
                    turn = turn + random.uniform(-turn_amount, turn_amount)
                if random.uniform(0, 1) < angle_chance:
                    branch_turn = branch_turn + random.uniform(-angle_amount, angle_amount)
                if random.uniform(0, 1) < 1.0 - branch_chance:
                    branch = False
                    c = c + 1
                if branch:
                    branch_shift = (i * ((math.pi * 2.0) / num_branches)) + turn
                    create(p_depth, p_length, p_length_inc, p_r, p_rate,
                           p_n,
                           p_l,
                           branch_turn, branch_shift,
                           polygons, num_branches, branch_ang,
                           foliage_sze, foliage_res, turn, branch, foliage_num, foliage_spr, 1, branch_chance,
                           angle_chance, turn_chance, turn_amount, angle_amount)

        if c == num_branches or p_depth <= 0:
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
               first_segment_l, pine_level, branch_chance, angle_chance, turn_chance, turn_amount, angle_amount):
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

        if pine_level == 3 or pine_level == 2:
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
                       foliage_sze, foliage_res, turn, branch, foliage_num, foliage_spr, 1, 1, branch_chance,
                       angle_chance, turn_chance, turn_amount, angle_amount)
        c = 0
        if p_depth > 0:
            branch_turn = branch_ang
            turn = turn + math.pi / 2.0
            for i in range(0, num_branches):
                branch = True
                p_length = p_length + random.uniform(-0.5, 0.5)
                if random.uniform(0, 1) < turn_chance:
                    turn = turn + random.uniform(-turn_amount, turn_amount)
                if random.uniform(0, 1) < angle_chance:
                    branch_turn = branch_turn + random.uniform(-angle_amount, angle_amount)
                if random.uniform(0, 1) < 1.0 - branch_chance:
                    branch = False
                    c = c + 1
                branch_shift = (i * ((math.pi * 2.0) / num_branches)) + turn
                if branch:
                    createPine(p_depth * 0.5, p_length * 0.7, p_length_inc, p_r, p_rate,
                               p_n,
                               p_l,
                               branch_turn, branch_shift,
                               polygons, num_branches, branch_ang,
                               foliage_sze, foliage_res, turn, branch, foliage_num, foliage_spr, 1, 2, branch_chance,
                               angle_chance, turn_chance, turn_amount, angle_amount)

        if c == num_branches or p_depth <= 0:
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

