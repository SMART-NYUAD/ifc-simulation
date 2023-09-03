# ifc-simulation
Parser that converts IFC files into formats that can be used for robotic simulations.

Pre-requisites are:
* IfcOpenShell
* Trimesh

The ifc_to_mesh.py script will take a scheduled IFC file as input and generate a 3D mesh that is schedule aware and that can be used in simulation environments.
The ifc_to_map.py script will generate a schedule-aware 2D map that can be used for autonomous navigation purposes.
