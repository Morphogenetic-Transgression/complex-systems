// scene setup goes here (Tree.js scene)
var WIDTH = window.innerWidth;
var HEIGHT = window.innerHeight;

var renderer = new THREE.WebGLRenderer({antialias:true});
renderer.setSize(WIDTH, HEIGHT);
renderer.setClearColor(0xDDDDDD, 1);
document.body.appendChild(renderer.domElement);

var scene = new THREE.Scene();

var camera = new THREE.PerspectiveCamera(70, WIDTH/HEIGHT);
camera.position.z = 50;
scene.add(camera);

var boxGeometry = new THREE.BoxGeometry(10, 10, 10);

// var basicMaterial = new THREE.MeshBasicMaterial({color: 0x0095DD});
const shaderMaterial = new THREE.ShaderMaterial({
     vertexShader: document.getElementById("vertexShader").textContent,
     fragmentShader: document.getElementById("fragmentShader").textContent,
   });

// var cube = new THREE.Mesh(boxGeometry, basicMaterial);
const cube = new THREE.Mesh(boxGeometry, shaderMaterial);

scene.add(cube);
cube.rotation.set(0.4, 0.2, 0);

function render() {
 requestAnimationFrame(render);
 
 cube.rotation.y += 0.01;
 
 renderer.render(scene, camera);
}
render();