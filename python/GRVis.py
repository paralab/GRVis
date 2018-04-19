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


def saveImgSlice(file_prefix,img_prefix,step,imgCount,window=[400,400]):
    filename=file_prefix+'_'+str(step)+'.pvtu'
    pvtuReader=vtkio.ReadPVTUFile(filename)
    pvtuReader.GetOutput().GetPointData().SetActiveAttribute("U_CHI", 0)
    gridSlice=filters.SliceFilter(pvtuReader)
    imgName=img_prefix+'_slice_'+str(imgCount).zfill(6)+'.png'
    render.ParallelRenderGeometry(gridSlice,windowSize=window,varName='U_CHI',colorbyScalar=True,scalarBar=True,saveImage=True,imageName=imgName,useParallelRendering=False)
    warpByScalar=filters.WarpByScalar(gridSlice,'U_CHI',scaleFactor=100)
    imgName=img_prefix+'_slice_wbs_'+str(imgCount).zfill(6)+'.png'
    render.ParallelRenderGeometry(warpByScalar,windowSize=window,varName='U_CHI',colorbyScalar=True,scalarBar=True,saveImage=True,imageName=imgName,useParallelRendering=False)
    #imgName=img_prefix+'_slice_level_wbs'+str(imgCount).zfill(6)+'.png'
    #render.ParallelRenderGeometry(warpByScalar,windowSize=window,varName='cell_level',colorbyScalar=True,scalarBar=True,saveImage=True,imageName=imgName,useParallelRendering=False)
    





def main():
    comm = vtk.vtkMPIController()
    #c.SetGlobalController(None)
    rank = comm.GetLocalProcessId()
    npes = comm.GetNumberOfProcesses()
    #print ("rank %d of size %d" %(rank,npes))


    parser = argparse.ArgumentParser()
    parser.add_argument('-b','--begin', help='begin step', required=True)
    parser.add_argument('-e','--end', help='end step', required=True)
    parser.add_argument('-f','--freq', help='io step frequency', required=True)
    parser.add_argument('-pvtu','--pvtu_prefix', help='pvtu prefix', required=True)
    parser.add_argument('-img','--img_prefix', help='image prefix ', required=True)
    args = vars(parser.parse_args())
    args = parser.parse_args()



    step_begin=int(args.begin)
    step_end=int(args.end)
    step_freq=int(args.freq)
    file_prefix=args.pvtu_prefix
    img_prefix=args.img_prefix

    '''step_begin=0
    step_end=20
    step_freq=10
    file_prefix='vtu/bssn_gr'
    img_prefix='img/img' 
    '''


    if(rank==0):
        print ("number of ranks: %d"%(npes))
    
    imgCount=step_begin/step_freq
    
    for step in range(step_begin,step_end,step_freq):
        # create a new 'XML Partitioned Unstructured Grid Reader'
        saveImgSlice(file_prefix,img_prefix,step,imgCount,window=[400,400])
        imgCount=imgCount+1

    '''
    pvtuReader=vtkio.ReadPVTUFile(args.pvtu_name)
    pvtuReader.GetOutput().GetPointData().SetActiveAttribute("U_CHI", 0)
    gridSlice=filters.SliceFilter(pvtuReader)
    warpByScalar=filters.WarpByScalar(gridSlice,'U_CHI',scaleFactor=100)
    #render.ParallelRenderGeometry(gridSlice,windowSize=[1000,1000],varName='U_CHI',colorbyScalar=True,scalarBar=True,saveImage=True,imageName='test.png',useParallelRendering=False)
    #render.VolumeRender(pvtuReader,windowSize=[300,300],varName="U_CHI")
    render.ParallelRenderGeometry(gridSlice,windowSize=[300,300],varName='U_CHI',colorbyScalar=True,scalarBar=True,saveImage=True,imageName='test.png',useParallelRendering=False)
    #render.VolumeRender(pvtuReader,windowSize=[300,300],varName="U_CHI")
    #render.renderGeometry(gridSlice)
    '''
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



