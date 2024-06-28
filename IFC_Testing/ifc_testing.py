import os
import subprocess
import pyvista as pv

import ifcopenshell.geom

IFC_PATH = 'ifc/AC20-Institute-Var-2.ifc'
XLSX_PATH = 'xlsx'
file_path = IFC_PATH
model = ifcopenshell.open(file_path)


def convert_ifc_to_obj(ifc_path, obj_path):
    # Obtenez le chemin du répertoire dans lequel se trouve ce script
    dir_path = os.path.dirname(os.path.realpath(__file__))

    # Construisez le chemin vers IfcConvert
    ifc_convert_path = os.path.join(dir_path, 'IfcConvert')

    command = f"{ifc_convert_path} {ifc_path} {obj_path}"
    print(command)
    process = subprocess.Popen(command, shell=True)
    process.wait()


obj_file_path = 'file.obj'
convert_ifc_to_obj(IFC_PATH, obj_file_path)

mesh = pv.read(obj_file_path)

plotter = pv.Plotter()
plotter.add_mesh(mesh)
plotter.show()
