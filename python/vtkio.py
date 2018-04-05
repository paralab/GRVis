#!/usr/bin/env python
#####
### CS6635 - Scientific Visualization Project. VTK based visualization framework for computational relativity. 
### Author: Milinda Fernando, Max Carlson
### School of Computing, University of Utah.
### Date: 04/02/2018
####

'''
IO related utilities needed for visualization. 

'''


import os
import vtk as vtk
from mpi4py import MPI

'''
@brief Reads the XML unstructed grid and retuns, vtkXMLUnstructuredGridReader (sequential)
'''
def ReadVTUFile(fname):
    reader = vtk.vtkXMLUnstructuredGridReader()
    reader.SetFileName(fname)
    reader.Update()
    return reader    
    #ugrid =vtk.vtkUnstructuredGrid()
    #ugrid.DeepCopy(reader.GetOutput())

    
'''
@brief Reads the XML partioned unstructed grid and retuns, vtkXMLPUnstructuredGridReader
'''
def ReadPVTUFile(fname):
    
    reader=vtk.vtkXMLPUnstructuredGridReader()
    reader.SetFileName(fname)
    reader.Update()
    #print reader.GetNumberOfPieces()
    return reader
    
    
