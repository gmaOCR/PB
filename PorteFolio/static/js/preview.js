import { IfcViewerAPI } from 'web-ifc-viewer';
import { handleObjectSelection } from './selection_logic.js';
import { setupPreselection } from './preselection_logic.js';

async function loadIfc(url, viewer) {
    console.log('Chargement de l\'IFC depuis:', url);
    const model = await viewer.IFC.loadIfcUrl(url);
    viewer.shadowDropper.renderShadow(model.modelID);
    console.log('IFC chargé avec succès');
}

function init() {
    const container = document.getElementById('three-container');
    const viewer = new IfcViewerAPI({ container: container });

    setupPreselection(viewer);

    if (!viewer.context || !viewer.context.renderer || !viewer.context.renderer.renderer.domElement) {
        console.error('Renderer ou domElement non défini !');
        return;
    }

    if (!viewer.context.ifcCamera.activeCamera) {
        console.error('Caméra non définie !');
        return;
    }

    viewer.context.scene.add(new THREE.GridHelper(100, 100));
    viewer.context.scene.add(new THREE.AxesHelper(5));

    const textField = document.getElementById('object_details');
    console.log(textField)
    if (textField) {
        container.addEventListener('click', (event) => handleObjectSelection(event, viewer, textField));
    } else {
        console.error('Erreur: l\'élément textarea n\'a pas été trouvé.');
    }

    const ifcUrl = document.getElementById('ifcUrl').value;
    const fullUrl = window.location.origin + '/media/' + ifcUrl;
    loadIfc(fullUrl, viewer);
}

document.addEventListener("DOMContentLoaded", init);
