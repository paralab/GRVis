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
import argparse as argparse
from mpi4py import MPI

parser = argparse.ArgumentParser()
parser.add_argument("pvtu_name")
args = parser.parse_args()

def main():
    #comm = vtk.vtkMPIController()
    #c.SetGlobalController(None)
    #rank = comm.GetLocalProcessId()
    #npes = comm.GetNumberOfProcesses()
    #print ("rank %d of size %d" %(rank,npes))
    pvtu_reader=vtkio.readPVTUFile(args.pvtu_name)
    render.renderGeometry(pvtu_reader)

    


if __name__ == "__main__":
    main()



