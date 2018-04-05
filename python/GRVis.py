#!/usr/bin/env python
#####
### CS6635 - Scientific Visualization Project. VTK based visualization framework for computational relativity. 
### Author: Milinda Fernando, Max Carlson
### School of Computing, University of Utah.
### Date: 04/02/2018
####

'''
main python file for GR Visualization. 

'''

import vtk as vtk
import vtkio as vtkio
import render as render
import filters as filters
import argparse as argparse
from mpi4py import MPI

parser = argparse.ArgumentParser()
parser.add_argument("pvtu_name")
args = parser.parse_args()

def main():
    comm = vtk.vtkMPIController()
    #c.SetGlobalController(None)
    rank = comm.GetLocalProcessId()
    npes = comm.GetNumberOfProcesses()
    print ("rank %d of size %d" %(rank,npes))
    pvtuReader=vtkio.readPVTUFile(args.pvtu_name)
    gridSlice=filters.SliceFilter(pvtuReader)
    #warpByScalar=filters.WarpByScalar(gridSlice,'U_CHI')
    render.renderGeometry(gridSlice,varName='U_CHI',colorbyScalar=True,scalarBar=True)
    #render.renderGeometry(gridSlice)
    


if __name__ == "__main__":
    main()



