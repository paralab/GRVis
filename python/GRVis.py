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
import utils as utils

parser = argparse.ArgumentParser()
parser.add_argument("pvtu_name")
args = parser.parse_args()

def main():
    comm = vtk.vtkMPIController()
    #c.SetGlobalController(None)
    rank = comm.GetLocalProcessId()
    npes = comm.GetNumberOfProcesses()
    print ("rank %d of size %d" %(rank,npes))
    pvtuReader=vtkio.ReadPVTUFile(args.pvtu_name)
    pvtuReader.GetOutput().GetPointData().SetActiveAttribute("U_CHI", 0)
    #gridSlice=filters.SliceFilter(pvtuReader)
    #warpByScalar=filters.WarpByScalar(gridSlice,'U_CHI')
    #render.ParallelRenderGeometry(gridSlice,windowSize=[1000,1000],varName='U_CHI',colorbyScalar=True,scalarBar=True,saveImage=True,imageName='test.png',useParallelRendering=False)
    #render.VolumeRender(pvtuReader,windowSize=[300,300],varName="U_CHI")
    #render.ParallelRenderGeometry(warpByScalar,windowSize=[1000,1000],varName='U_CHI',colorbyScalar=True,scalarBar=True,saveImage=False,imageName='test.png',useParallelRendering=False)
    render.VolumeRender(pvtuReader,windowSize=[300,300],varName="U_CHI")
    #render.renderGeometry(gridSlice)
    '''
    BH1InitalLoc=utils.BHCoordsToOctree(BHCoords=[-4.0,0,0],maxDepth=12,BHBounds=[-200.0,200.0])
    BH2InitalLoc=utils.BHCoordsToOctree(BHCoords=[4.0,0,0],maxDepth=12,BHBounds=[-200.0,200.0])
    if(rank==0):
        print [BH1InitalLoc,BH2InitalLoc]
    BH_Loc=filters.ExtractBHLocations(pvtuReader,BH1PrevLoc=BH1InitalLoc,BH2PrevLoc=BH2InitalLoc)
    if(rank==0):
         print (BH_Loc)
    '''

if __name__ == "__main__":
    main()



