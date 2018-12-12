import maya.cmds as cmds
import math
import random


def get_rotations(px, py, pz, pax, pay, paz):
    x = px
    y = py
    z = pz

    x1 = x * math.cos(paz) - y * math.sin(paz)
    y1 = x * math.sin(paz) + y * math.cos(paz)
    z1 = z

    z11 = z1 * math.cos(pay) - x1 * math.sin(pay)
    x11 = z1 * math.sin(pay) + x1 * math.cos(pay)
    y11 = y1

    y111 = y11 * math.cos(pax) - z11 * math.sin(pax)
    z111 = y11 * math.sin(pax) + z11 * math.cos(pax)
    x111 = x11

    final = [x111, y111, z111]
    return final


def polytube(p1_x, p1_y, p1_z, p2_x, p2_y, p2_z, p1_r, p2_r, a1_x, a1_y, a1_z, a2_x, a2_y, a2_z, subdivisions):
    for i in range(0, subdivisions):
        inc = math.pi * 2 / subdivisions
        point1 = get_rotations(p1_x + p1_r * math.cos(inc * i),
                               p1_y,
                               p1_z + p1_r * math.sin(inc * i),
                               a1_x, a1_y, a1_z)
        point2 = get_rotations(p1_x + p1_r * math.cos(inc * i + inc),
                               p1_y,
                               p1_z + p1_r * math.sin(inc * i + inc),
                               a1_x, a1_y, a1_z)
        point3 = get_rotations(p2_x + p2_r * math.cos(inc * i),
                               p2_y,
                               p2_z + p2_r * math.sin(inc * i),
                               a2_x, a2_y, a2_z)
        point4 = get_rotations(p2_x + p2_r * math.cos(inc * i + inc),
                               p2_y,
                               p2_z + p2_r * math.sin(inc * i + inc),
                               a2_x, a2_y, a2_z)

        cmds.polyCreateFacet(p=[point2,
                                point1,
                                point3,
                                point4])


def create(p_r, p_rate, p_lx, p_ly, p_lz, p_nx, p_ny, p_nz):
    for i in range(1, 4):  # counting layers of tree
        p_nx = p_lx
        p_ny = p_ly + i
        p_nz = p_lz
        polytube(p_lx, p_ly, p_lz,
                 p_nx, p_ny, p_nz,
                 p_r, p_r - p_rate,
                 math.pi + math.pi / 2, math.pi / 2, math.pi / 2,
                 math.pi + math.pi / 2, math.pi / 2, math.pi / 2,
                 4)
        p_r = p_r - p_rate
        p_lx = p_nx
        p_ly = p_ny
        p_lz = p_nz


create(1, 0.1,
       0, 0, 0,
       0, 0, 0)
