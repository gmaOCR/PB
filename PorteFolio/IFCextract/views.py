
from django.conf import settings
from django.http import FileResponse
from django.shortcuts import render
from .forms import IfcFileForm
from .ifc_class import *
from .extract import *


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
            element_entities_by_type = element_analyzer.get_entities_by_type(element_analyzer.filtered_entities)
            non_element_entities_by_type = non_element_analyzer.get_entities_by_type(non_element_analyzer.filtered_entities)

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
                zip_file = analyzer.export_ifc_to_csv()  # Ici on utilise la méthode export_ifc_to_csv()

                with delete_file_after_use(ifc_path):
                    pass  # Do nothing, file will be deleted after the context is closed

                # Send the zip file in response
                response = FileResponse(open(zip_file, 'rb'), content_type='application/zip')
                response['Content-Disposition'] = f'attachment; filename={os.path.basename(zip_file)}'
                with delete_file_after_use(zip_file):
                    return response
            except ValueError as e:
                return render(request, 'error_file.html', {'error_message': str(e)})

    return render(request, 'upload.html', {'form': form})


def preview_ifc(request):
    form = IfcFileForm()
    if request.method == 'POST':
        form = IfcFileForm(request.POST, request.FILES)
        if form.is_valid():
            ifc_file = form.save()
            ifc_path = ifc_file.file.path
            try:
                IFCObjectAnalyzer(ifc_path, is_element=True)
            except ValueError as e:
                return render(request, 'error_file.html', {'error_message': str(e)})
            ifc_url = os.path.relpath(ifc_path, settings.MEDIA_ROOT)
            return render(request, 'preview.html', {'ifc_url': ifc_url})
    else:
        return render(request, 'upload.html', {'form': form})


def test_thatopen(request):
    return render(request, 'thatopen.html')
