import ifcopenshell
import ifcopenshell.geom as geom
import trimesh
import matplotlib.pyplot as plt
import numpy as np

from datetime import datetime

from ifcfunctions import meshfromshape, getunitfactor, sectionfromshape, get_construction_date

date_input = input('Enter current date: ')

curr_date = datetime.strptime(date_input,"%d/%m/%Y")


ifc_file = ifcopenshell.open('SMART_scheduled.ifc')

settings = ifcopenshell.geom.settings()
settings.set(settings.USE_WORLD_COORDS, True)

meshlist=[]
levels=[]

unitfactor = getunitfactor(ifc_file)

storeys = ifc_file.by_type('IfcBuildingStorey')

elements = ifc_file.by_type('IfcElement')

for storey in storeys:
  levels.append(storey.ObjectPlacement.RelativePlacement.Location[0][2])

print(levels)





for ifc_entity in ifc_file.by_type('IfcElement'): #iterating through every ifcelement
  if ifc_entity.is_a('IfcOpeningElement'):
		  continue #skipping IfcOpeningElement because its not useful to obstacle map?
  if ifc_entity.is_a('IfcSlab'):
      continue #skipping IfcSlab because its not useful to obstacle map
  if ifc_entity.Representation is None: #skipping elements that have no representation
      continue 

  date = get_construction_date(ifc_entity)
  if date is None or date>=curr_date:
    continue

  shape = geom.create_shape(settings, ifc_entity)
    
  if ifc_entity.is_a('IfcDoor'):
      meshcolor = [0,255,0,170]
  elif ifc_entity.is_a('IfcStair'):
      meshcolor = [255,255,0,255]
  else:
      meshcolor = [100,100,100,255]



		
  mesh = meshfromshape(shape,meshcolor) #creating mesh from shape, specifying color
  meshlist.append(mesh) #adding to list of meshes
  


combined = trimesh.util.concatenate(meshlist)

combined.export('SMART.obj')
combined.show()



























  

