import os
from contextlib import contextmanager

from django.http import FileResponse
from django.shortcuts import render, redirect
from .forms import IfcFileForm
from .ifc_class import *
from .extract import *


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
                element_analyzer = IFCObjectAnalyzer(ifc_path, is_element=True)
                non_element_analyzer = IFCObjectAnalyzer(ifc_path, is_element=False)
            except ValueError as e:
                return render(request, 'error_file.html', {'error_message': str(e)})

            # Obtenir les entités triées par type pour les objets géométriques et non géométriques
            element_entities_by_type = get_entities_by_type(element_analyzer.filtered_entities)
            non_element_entities_by_type = get_entities_by_type(non_element_analyzer.filtered_entities)

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
                analyzer = IFCObjectAnalyzer(ifc_path, True)
                # Get all element types
                types_list = analyzer.get_all_element_types()
                csv_files = []
                for element_type in types_list:
                    # Extract data for each element type and write to CSV
                    data, _ = analyzer.extract_data(element_type)
                    csv_filename = f"{element_type}.csv"
                    df = pd.DataFrame(data)
                    df.to_csv(csv_filename)
                    csv_files.append(csv_filename)

                # Create a zip file containing all CSV files
                zip_file = "media/zip/output.zip"
                with zipfile.ZipFile(zip_file, 'w') as zipf:
                    for csv_file in csv_files:
                        zipf.write(csv_file)
                        os.remove(csv_file)  # Delete file after adding it to zip

                # Delete IFC file after use
                os.remove(ifc_path)

                # Send the zip file in response
                response = FileResponse(open(zip_file, 'rb'), content_type='application/zip')
                response['Content-Disposition'] = f'attachment; filename={os.path.basename(zip_file)}'
                return response
            except ValueError as e:
                return render(request, 'error_file.html', {'error_message': str(e)})

    return render(request, 'upload.html', {'form': form})
