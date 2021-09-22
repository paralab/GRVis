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
#import utils as utils


def render_pvtu(file_prefix,img_prefix,step,imgCount,window=[400,400]):
    filename=file_prefix+'_'+str(step)+'.pvtu'
    pvtuReader=vtkio.ReadPVTUFile(filename)
    pvtuReader.GetOutput().GetPointData().SetActiveAttribute("U_CHI", 0)

    colors = vtk.vtkNamedColors()
    output = pvtuReader.GetOutput()
    # Create the mapper that corresponds the objects of the vtk.vtk file
    # into graphics elements
    mapper = vtk.vtkDataSetMapper()
    mapper.SetInputData(output)
    # mapper.SetScalarRange(scalar_range)
    mapper.ScalarVisibilityOff()

    # Create the Actor
    actor = vtk.vtkActor()
    actor.SetMapper(mapper)
    actor.GetProperty().EdgeVisibilityOn()
    actor.GetProperty().SetLineWidth(2.0)
    actor.GetProperty().SetColor(colors.GetColor3d("MistyRose"))

    backface = vtk.vtkProperty()
    backface.SetColor(colors.GetColor3d('Tomato'))
    actor.SetBackfaceProperty(backface)

    # Create the Renderer
    renderer = vtk.vtkRenderer()
    renderer.AddActor(actor)
    renderer.SetBackground(colors.GetColor3d('Wheat'))

    # Create the RendererWindow
    renderer_window = vtk.vtkRenderWindow()
    renderer_window.SetSize(640, 480)
    renderer_window.AddRenderer(renderer)
    renderer_window.SetWindowName('ReadUnstructuredGrid')

    # Create the RendererWindowInteractor and display the vtk_file
    interactor = vtk.vtkRenderWindowInteractor()
    interactor.SetRenderWindow(renderer_window)
    interactor.Initialize()
    interactor.Start()
    

def main():
    
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

    imgCount=step_begin/step_freq
    
    for step in range(step_begin,step_end,step_freq):
        # create a new 'XML Partitioned Unstructured Grid Reader'
        render_pvtu(file_prefix,img_prefix,step,imgCount,window=[400,400])
        imgCount=imgCount+1

    

if __name__ == "__main__":
    main()



