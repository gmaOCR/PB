import * as THREE from 'three';
//import { IFCLoader } from 'three/examples/jsm/loaders/IFCLoader';
import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls';
import { GridHelper } from 'three';
import { IFCLoader } from "web-ifc-three/IFCLoader";

function init() {

    // Initialisation
    var container = document.getElementById('three-container');
    var scene = new THREE.Scene();


    // Configuration de la caméra et du renderer
    var camera = new THREE.PerspectiveCamera(75, container.offsetWidth / container.offsetHeight, 0.1, 1000);
    var renderer = new THREE.WebGLRenderer({ antialias: true, canvas: container });
    renderer.setSize(container.offsetWidth, container.offsetHeight);

    //Initialisation des contrôles
    const controls = new OrbitControls(camera, renderer.domElement);
    controls.update();

    // Ajout de lumière
    var ambientLight = new THREE.AmbientLight(0xcccccc, 0.4);
    scene.add(ambientLight);
    var pointLight = new THREE.PointLight(0xffffff, 0.8);
    camera.add(pointLight);
    scene.add(camera);

    var renderer = new THREE.WebGLRenderer({ antialias: true, canvas: container });
    renderer.setSize(container.offsetWidth, container.offsetHeight);
    renderer.setClearColor(0xffffff);  // Optionnel : changer la couleur de fond


    // Grid helper:
    const size = 100; // Cela dépend de la taille de votre modèle IFC
    const divisions = 100;
    const gridHelper = new GridHelper(size, divisions);
    gridHelper.rotation.x = Math.PI / 2;  // Cela place la grille horizontalement, comme un plancher
    scene.add(gridHelper);

    // Ajout des axes helper:
    const axesHelper = new THREE.AxesHelper(5);  // 5 est la taille des axes
    scene.add(axesHelper);

    // Position de la caméra
    camera.position.z = 5;

    // Chargement de l'IFC
    var ifcUrl = document.getElementById('ifcUrl').value;
    ifcUrl = '/media/' + ifcUrl;
    const ifcLoader = new IFCLoader();
    ifcLoader.wasmPath = '/static/wasm/';
    ifcLoader.load(ifcUrl, (geometry) => {
        scene.add(geometry);
        // Ajuste la caméra pour voir l'ensemble du modèle
        const box = new THREE.Box3().setFromObject(geometry);
        const size = box.getSize(new THREE.Vector3()).length();
        const center = box.getCenter(new THREE.Vector3());
        camera.position.copy(center);
        camera.position.x += size / 2.0;
        camera.position.y += size / 5.0;
        camera.position.z += size / 2.0;
        camera.lookAt(center);
    });

    // Boucle d'animation
    function animate() {
        requestAnimationFrame(animate);
        renderer.render(scene, camera);
    }
    animate();
}
document.addEventListener("DOMContentLoaded", init);