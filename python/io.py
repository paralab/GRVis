#!/usr/bin/env python
#####
### Author: Milinda Fernando
### School of Computing, University of Utah. 
### Example taken from :  https://raw.githubusercontent.com/Kitware/VTK/master/IO/XML/Testing/Python/TestXMLUnstructuredGridIO.py
####
import os
import vtk

def readPVTUFile(fname):
    reader = vtk.vtkXMLUnstructuredGridReader()
    reader.SetFileName(fname)
    reader.Update()
    ugrid = vtk.vtkUnstructuredGrid()
    ugrid.DeepCopy(reader.GetOutput())

    return ugrid    

