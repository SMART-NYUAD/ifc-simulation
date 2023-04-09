import ifcopenshell
import ifcopenshell.geom as geom
import trimesh
import matplotlib.pyplot as plt
from datetime import datetime

from shapely.geometry import Polygon, MultiPolygon


from ifcfunctions import meshfromshape, getunitfactor, sectionfromshape, get_construction_date

arsheight = 0.7

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


plt.figure()

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
      color = 'lime'
  elif ifc_entity.is_a('IfcStair'):
      color = 'yellow'
  else:
      color = 'black'
		
  multipoly = sectionfromshape(shape,arsheight) #creating mesh from shape, specifying color

  if multipoly is None:
    continue

  if isinstance(multipoly, Polygon):
    multipoly = MultiPolygon([multipoly])

  for polygon in multipoly.geoms:
    plt.fill(*polygon.exterior.xy, alpha=1, color = color)



centroid_list=[]

spaces = ifc_file.by_type('IfcSpace')

print(len(spaces))



for space in spaces: #iterating through every ifcelement
  
  shape = geom.create_shape(settings, space)

  multipoly = sectionfromshape(shape,arsheight) #creating mesh from shape, specifying color

  date = get_construction_date(space)

  if date < curr_date:
    color = 'blue'
  else:
    color = 'red'

  if multipoly is None:
    continue

  if isinstance(multipoly, Polygon):
    multipoly = MultiPolygon([multipoly])

  for polygon in multipoly.geoms:
    plt.fill(*polygon.exterior.xy, alpha=0.5, color = color)

  mesh = meshfromshape(shape,[0,0,0,100]) 
  centroid = mesh.centroid
  print(centroid)
  if round(centroid[2]) == round(levels[0]/unitfactor):
    centroid = centroid[0:2]
  centroid_list.append(centroid) #adding to list of meshes

for centroid in centroid_list:
  plt.scatter(centroid[0],centroid[1],color = 'pink', marker = 'x', linewidth=0.8,s=4)



plt.gca().set_aspect('equal')
plt.axis('off')
plt.savefig('SMART_map.png', bbox_inches='tight',dpi=400)


plt.show()






























  

