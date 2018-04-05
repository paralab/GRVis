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
import sys
import vtk as vtk
import filters as filters
from mpi4py import MPI

'''
Writes a screen shot to a file. 
'''
def SaveScreenShot(renderWindow,fileName):
    windowToImageFilter=vtk.vtkWindowToImageFilter()
    windowToImageFilter.SetInput(renderWindow)
    #windowToImageFilter.SetMagnification(1); #set the resolution of the output image (3 times the current resolution of vtk render window)
    windowToImageFilter.SetInputBufferTypeToRGBA(); #also record the alpha (transparency) channel
    windowToImageFilter.ReadFrontBufferOff(); # read from the back buffer
    windowToImageFilter.Update()
       
    pngWriter=vtk.vtkPNGWriter()
    pngWriter.SetFileName(fileName)
    pngWriter.SetInputConnection(windowToImageFilter.GetOutputPort())
    pngWriter.Write()
    print "image written"



'''
Generate a render window, for a given source, (uses parallel distributed memory rendering)
source: source of the geometry to do the rendering
height: height of the rendering window
width: width of the rendering window. 
'''
def ParallelRenderGeometry(source,windowSize=[300,300],backgroundColor=[0,0,0],varName='',colorbyScalar=False,scalarBar=True,useParallelRendering=False,saveImage=False,imageName=''):
    
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


    # create custom light 
    lightPosition=[0,0,1]
    lightFocalPoint=[0,0,0]

    light=vtk.vtkLight()
    light.SetLightTypeToSceneLight()
    light.SetPosition(lightPosition)
    light.SetPositional(True)
    light.SetConeAngle(10)
    light.SetFocalPoint(lightFocalPoint)
    light.SetDiffuseColor(1,0,0)
    light.SetAmbientColor(0,1,0)
    light.SetSpecularColor(0,0,1)

    lightActor=vtk.vtkLightActor()
    lightActor.SetLight(light)

    # create camera
    camera =vtk.vtkCamera()
    camera.SetPosition(2048,2048,1048)
    camera.SetFocalPoint(2048,2048,2048)


    # Create the Renderer
    renderer = vtk.vtkRenderer()
    renderer.AddViewProp(lightActor) # add light
    renderer.SetActiveCamera(camera) # set the camera
    
    
    mapper = vtk.vtkPolyDataMapper()
    mapper.SetInputConnection(surfaceFilter.GetOutputPort())
    
    if colorbyScalar:
        scalarRange=filters.ComputeScalarRange(source,varName)
        mapper.ScalarVisibilityOn()
        mapper.SetScalarRange(scalarRange)
        mapper.SetScalarModeToUsePointFieldData()
        
        cMap=filters.GenerateDivergingColorMap()
        mapper.SetLookupTable( cMap )
        mapper.ColorByArrayComponent(varName,0)
        

        if scalarBar:
            colorBar=vtk.vtkScalarBarActor()
            colorBar.SetLookupTable(mapper.GetLookupTable())
            colorBar.SetTitle(varName)
            colorBar.SetNumberOfLabels(8)
            #colorBar.GetLabelTextProperty().SetFontSize(3)
            #colorBar.GetTitleTextProperty().SetFontSize(3)
            #colorBar.SetBarRatio (0.4)
            #colorBar.GetAnnotationTextProperty().SetFontSize(3)
            #print colorBar.GetMaximumHeightInPixels()
            #colorBar.SetOrientationToHorizontal()
            #colorBar.Update()
            #Create a lookup table to share between the mapper and the scalarbar
            #colorBar.SetLookupTable( hueLut )
            renderer.AddActor2D(colorBar)

                       


    
    # Create the Actor
    actor = vtk.vtkActor()
    actor.SetMapper(mapper)
    
    renderer.AddActor(actor)
    #renderer.AddActor2D(colormap)
    renderer.SetBackground(backgroundColor[0], backgroundColor[1], backgroundColor[2]) # Set background to white
    
     
    # Create the RendererWindow
    renderer_window = vtk.vtkRenderWindow()
    renderer_window.AddRenderer(renderer)
    renderer_window.SetWindowName("render view of %d" % rank)
    renderer_window.SetSize(windowSize)
    
    if npes > 1 and useParallelRendering:
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
        if saveImage:
            renderer_window.Render()
            SaveScreenShot(renderer_window,imageName)
        else:
            iren = vtk.vtkRenderWindowInteractor()
            iren.SetRenderWindow(renderer_window)
            iren.AddObserver("ExitEvent", ExitMaster)
            iren.Initialize()
            iren.Start()
        
        #renderer_window.Render()
        #renderer_window.Render()
        #renderer_window.Render()
    else:
        #print rank
        compManager.InitializeRMIs()
        compManager.GetController().ProcessRMIs()
        compManager.GetController().Finalize()
        #print "**********************************"
        #print "Done on the slave node"
        #print "**********************************"
        sys.exit()
    ExitMaster(0,0)
    return 

