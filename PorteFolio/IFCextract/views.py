import os
from contextlib import contextmanager

from django.http import FileResponse
from django.shortcuts import render, redirect
from .forms import IfcFileForm
from .ifc_class import *

import ifcopenshell


@contextmanager
def delete_file_after_use(file_path):
    try:
        yield file_path
    finally:
        # Supprimer le fichier après avoir quitté le contexte
        os.remove(file_path)


def read_ifc(request):
    form = IfcFileForm()
    if request.method == 'POST':
        form = IfcFileForm(request.POST, request.FILES)
        if form.is_valid():
            ifc_file = form.save()
            ifc_path = ifc_file.file.path
            try:
                analyzer = IFCObjectAnalyzer(ifc_path)
            except ValueError as e:
                return render(request, 'error_file.html', {'error_message': str(e)})

            # Obtenir les entités triées par type pour les objets géométriques et non géométriques
            element_entities_by_type = get_entities_by_type(analyzer.element_obj)
            non_element_entities_by_type = get_entities_by_type(analyzer.non_element_obj)

            # Créer les données pour le contexte
            element_entity_data = [{'type': entity_type, 'entities': entities} for entity_type, entities in
                                   element_entities_by_type.items()]
            non_element_entity_data = [{'type': entity_type, 'entities': entities} for entity_type, entities in
                                       non_element_entities_by_type.items()]

            with delete_file_after_use(ifc_path):
                context = {
                    'element_entity_data': element_entity_data,
                    'non_element_entity_data': non_element_entity_data,
                }
                return render(request, 'result.html', context=context)

    return render(request, 'upload.html', {'form': form})


def extract_geometry(request):
    form = IfcFileForm()
    if request.method == 'POST':
        form = IfcFileForm(request.POST, request.FILES)
        if form.is_valid():
            ifc_file = form.save()
            ifc_path = ifc_file.file.path
            try:
                analyzer = IFCObjectAnalyzer(ifc_path)
                # Extract geometry from elements and export data to CSV files
                csv_files = analyzer.export_all_to_csv()
                # Create a zip file containing all CSV files
                zip_file = "zip/output.zip"
                analyzer.compress_files(csv_files, zip_file)
                # Delete CSV files after zipping
                for file in csv_files:
                    with delete_file_after_use(file):
                        if os.path.exists(file):
                            pass
                # Send the zip file in response
                response = FileResponse(open(zip_file, 'rb'), content_type='application/zip')
                response['Content-Disposition'] = f'attachment; filename={os.path.basename(zip_file)}'
                return response  # Change redirect to response here
            except ValueError as e:
                return render(request, 'error_file.html', {'error_message': str(e)})

    return render(request, 'upload.html', {'form': form})


