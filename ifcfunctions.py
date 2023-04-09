
import ifcopenshell
import matplotlib.pyplot as plt
from matplotlib import collections as  mc
import numpy as np
import math
import trimesh

from datetime import datetime


def getunitfactor(ifc_file):

    project = ifc_file.by_type('IfcProject')

    units = project[0].UnitsInContext.Units

    length_unit = next(filter(lambda u: u.UnitType == "LENGTHUNIT", units))

    prefix = length_unit[2]

    if prefix == None:
        return 1
    if prefix == 'MILLI':
        return 1000




def meshfromshape(shape, color):

	verts = shape.geometry.verts
	edges = shape.geometry.edges 
	faces = shape.geometry.faces


	procverts = [verts[i:i+3] for i in range(0,len(verts), 3)]

	procedges = [edges[i : i + 2] for i in range(0, len(edges), 2)]

	procfaces = [tuple(faces[i : i + 3]) for i in range(0, len(faces), 3)]

	mesh = trimesh.Trimesh(vertices=procverts,faces=procfaces, edges=procedges, process = True)

	for facet in mesh.facets:
		mesh.visual.face_colors[facet] = color 

	return mesh



def sectionfromshape(shape,slice_height):

	verts = shape.geometry.verts
	edges = shape.geometry.edges 
	faces = shape.geometry.faces

	procverts = [verts[i:i+3] for i in range(0,len(verts), 3)]

	procedges = [edges[i : i + 2] for i in range(0, len(edges), 2)]

	procfaces = [tuple(faces[i : i + 3]) for i in range(0, len(faces), 3)]

	mesh = trimesh.Trimesh(vertices=procverts,faces=procfaces, edges=procedges, process = True)

	sliced = trimesh.intersections.slice_mesh_plane(mesh, plane_normal=[0, 0,-1], plane_origin=[0,0,slice_height])
	if sliced is None or len(sliced.vertices)==0:
		return None

	polygon = trimesh.path.polygons.projected(sliced,[0,0,1])

	return polygon


def rawmeshfromshape(shape):

	verts = shape.geometry.verts
	edges = shape.geometry.edges 
	faces = shape.geometry.faces




	procverts = [verts[i:i+3] for i in range(0,len(verts), 3)]

	procedges = [edges[i : i + 2] for i in range(0, len(edges), 2)]

	procfaces = [tuple(faces[i : i + 3]) for i in range(0, len(faces), 3)]

	

	return procverts,procedges,procfaces






def findwidth(element_quantity):

	for quantity in element_quantity.Quantities:
			if quantity.is_a('IfcQuantityLength'):
				if quantity.Name == 'Width':
					width = quantity.LengthValue
					return width

def get_width(item):
	for definition in item.IsDefinedBy:
		related_data = definition.RelatingPropertyDefinition
		if related_data.is_a('IfcElementQuantity'):
			
			data = findwidth(related_data)
			if data != None:
				width = data
				return width


def findheight(element_quantity):

	for quantity in element_quantity.Quantities:
			if quantity.is_a('IfcQuantityLength'):
				if quantity.Name == 'Height':
					height = quantity.LengthValue
					return height

def get_height(item):
	for definition in item.IsDefinedBy:
		related_data = definition.RelatingPropertyDefinition
		if related_data.is_a('IfcElementQuantity'):
			
			data = findheight(related_data)
			if data != None:
				height = data
				return height






def finddepth(element_quantity):

	for quantity in element_quantity.Quantities:
			if quantity.is_a('IfcQuantityLength'):
				if quantity.Name == 'Depth':
					length = quantity.LengthValue
					return length

def get_depth(item):
	for definition in item.IsDefinedBy:
		related_data = definition.RelatingPropertyDefinition
		if related_data.is_a('IfcElementQuantity'):
			
			data = finddepth(related_data)
			if data != None:
				length = data
				return length







def countitems(items):

    counted = []
    itemlist = []
    index = 0
    itemcounter = []

    for i in range(len(items)):
        itemcounter.append(0)

        
    for item in items:
        if item not in counted:
            itemlist.append(item)
            counted.append(item)
            index = index + 1
            for item2 in items:
                if item2 == item:
                    itemcounter[index-1] = itemcounter[index-1]+1


    for x in range(len(itemlist)):

        print (str(itemlist[x])+'::::'+str(itemcounter[x]))


def get_construction_date(ifcelement):
	psets = ifcopenshell.util.element.get_psets(ifcelement)
	if ifcelement.is_a('IfcWall'):
		schedule_key = 'Wall Schedule'
		date_key = 'ConstructionDate'
	elif ifcelement.is_a('IfcSpace'):
		schedule_key = 'Room Schedule'
		date_key = 'RoomDate'
	elif ifcelement.is_a('IfcDoor'):
		schedule_key = 'Door Schedule'
		date_key = 'DoorDate'
	else:
		return None

	schedule = psets.get(schedule_key)
	if schedule is None:
		return None
	date_text = schedule[date_key]
	date = datetime.strptime(date_text,"%d/%m/%Y")
	return date
