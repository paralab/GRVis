#!/usr/bin/env python
#####
### CS6635 - Scientific Visualization Project. VTK based visualization framework for computational relativity. 
### Author: Milinda Fernando, Max Carlson
### School of Computing, University of Utah.
### Date: 04/02/2018
####

'''

All the filters, and filter helper functions. 

'''

import vtk as vtk
from mpi4py import MPI

'''
compute the slice of the octree. 
'''

def SliceFilter(source,genScalars=True,genTriangles=False):

    plane=vtk.vtkPlane()
    plane.SetOrigin(2048,2048,2048)
    plane.SetNormal(0,0,1)

    #create cutter
    cutter=vtk.vtkCutter()
    cutter.SetCutFunction(plane)
    cutter.SetInputConnection(source.GetOutputPort())
    # genScalars on computes the scalar values at the plane. 
    
    if genScalars:  
        cutter.GenerateCutScalarsOn()
    else:
        cutter.GenerateCutScalarsOff()
    
    #genTriangles on compute the triangular mesh on the slice
    '''
    if genTriangles:
        cutter.GenerateTrianglesOn()
    else:
        cutter.GenerateTrianglesOn()
    '''
    cutter.Update()
    
    return cutter


'''
color by a specific variable or a vector. 
'''
def ComputeScalarRange(source,varName):
    pointData=source.GetOutput().GetPointData()
    data=pointData.GetArray(varName)
    data_range=data.GetRange()
    return data_range


'''
warp by scalar
'''
def WarpByScalar(source,varName):
    warpByScalar=vtk.vtkWarpScalar()
    warpByScalar.SetInputConnection(source.GetOutputPort())
    warpByScalar.SetScaleFactor(100); #use the scalars themselves
    warpByScalar.UseNormalOn();
    warpByScalar.SetNormal(0, 0, 1);
    warpByScalar.Update()
    return warpByScalar


'''
Generate Diverging color scheme with RGB1 and RGB2.

'''

def GenerateDivergingColorMap(RGB1=[0,0,1],RGB2=[1,0,0],numColors=256):
    lut = vtk.vtkLookupTable()
    lut.SetNumberOfTableValues(numColors)
    ctf = vtk.vtkColorTransferFunction()
    ctf.SetColorSpaceToDiverging()
    ctf.AddRGBPoint(0,float(RGB1[0]),float(RGB1[1]),float(RGB1[2]))
    ctf.AddRGBPoint(1,float(RGB2[0]),float(RGB2[1]),float(RGB2[2]))
    #ctf.AddRGBPoint(0.0, 0, 0, 1.0)
    #ctf.AddRGBPoint(1.0, 1.0, 0, 0)
    for ii,ss in enumerate([float(xx)/float(numColors) for xx in range(numColors)]):
        cc = ctf.GetColor(ss)
        lut.SetTableValue(ii,cc[0],cc[1],cc[2],1.0)
    return lut




