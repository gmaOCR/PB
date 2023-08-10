import { IfcViewerAPI } from 'web-ifc-viewer';
import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls';

function init() {
    const container = document.getElementById('three-container');

    // Créez une instance du viewer
    const viewer = new IfcViewerAPI({ container });

    // Configurez des axes et une grille pour le viewer
    viewer.axes.setAxes();
    viewer.grid.setGrid();

    // Ajout de contrôles d'orbite pour permettre la navigation
    const controls = new OrbitControls(viewer.camera, viewer.renderer.domElement);
    controls.update();

    // Chargement de l'IFC
    const input = document.getElementById("file-input");
    input.addEventListener("change", async (changed) => {
        const file = changed.target.files[0];
        const ifcURL = URL.createObjectURL(file);
        viewer.IFC.loadIfcUrl(ifcURL);
    }, false);
}

document.addEventListener("DOMContentLoaded", init);
