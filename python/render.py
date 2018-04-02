#!/usr/bin/env python
#####
### CS6635 - Scientific Visualization Project. VTK based visualization framework for computational relativity. 
### Author: Milinda Fernando, Max Carlson
### School of Computing, University of Utah.
### Date: 04/02/2018
####


'''
Contains the function utilities related to geometric rendering functions. 
'''


import os
import vtk as vtk
from mpi4py import MPI

'''
Generate a render window, for a given source, (uses parallel distributed memory rendering)
source: source of the geometry to do the rendering
height: height of the rendering window
width: width of the rendering window. 

'''
def renderGeometry(source,height=300,width=300,backgroundColor=[0,0,0]):
    
    rank = 0 
    npes = 1
    compManager = vtk.vtkCompositeRenderManager()
    if compManager.GetController():
        rank = compManager.GetController().GetLocalProcessId()
        npes = compManager.GetController().GetNumberOfProcesses()
    else:
        print("Error "+str(renderGeometry.__name__)+" in VTK composite manager")        
        sys.exit()
    
    surfaceFilter = vtk.vtkDataSetSurfaceFilter()
    surfaceFilter.SetInputConnection(source.GetOutputPort())
    
    mapper = vtk.vtkPolyDataMapper()
    mapper.SetInputConnection(surfaceFilter.GetOutputPort())
    #mapper.SetScalarRange(scalar_range)
    
    # Create the Actor
    actor = vtk.vtkActor()
    actor.SetMapper(mapper)

    # Create the Renderer
    renderer = vtk.vtkRenderer()
    renderer.AddActor(actor)
    renderer.SetBackground(backgroundColor[0], backgroundColor[1], backgroundColor[2]) # Set background to white
     
    # Create the RendererWindow
    renderer_window = vtk.vtkRenderWindow()
    renderer_window.AddRenderer(renderer)
    renderer_window.SetWindowName("render view of %d" % rank)

    if npes > 1:
        compManager.SetRenderWindow(renderer_window)
        compManager.InitializePieces()
    
    def ExitMaster(a, b):
        #print("ExitMaster; I am %d / %d" % ( myProcId, numProcs ))
        if npes > 1 and rank == 0:
            #print("Trigger exit RMI on all satellite nodes")
            for a in range(1, npes):
                #print("Trigger exit in satellite node %d" % a)
                contr = compManager.GetController()
                contr.TriggerRMI(a, contr.GetBreakRMITag())

    if rank == 0:
        iren = vtk.vtkRenderWindowInteractor()
        iren.SetRenderWindow(renderer_window)
        iren.AddObserver("ExitEvent", ExitMaster)
        iren.Initialize()
        iren.Start()
        #renderer_window.Render()
        #renderer_window.Render()
        #renderer_window.Render()
    else:
        print rank
        compManager.InitializeRMIs()
        compManager.GetController().ProcessRMIs()
        compManager.GetController().Finalize()
        #print "**********************************"
        #print "Done on the slave node"
        #print "**********************************"
        sys.exit()
    ExitMaster(0,0)
    return 

