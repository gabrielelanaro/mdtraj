

var MolecularViewer = function ($el) {
	/* A MolecularViewer displays and manages a set of representations for a chemical system.

	*/

	this.container = $el;
	this.container.widthInv  = 1 / this.container.width();
	this.container.heightInv = 1 / this.container.height();
	this.container.whratio = this.container.width() / this.container.height();
	this.container.hwratio = this.container.height() / this.container.width();
	this.renderer = new THREE.WebGLRenderer({
		canvas: this.container.get(0),
		antialias: true,
        preserveDrawingBuffer: true,
	});
	this.effects = {
        // 'anaglyph': new THREE.AnaglyphEffect(this.renderer),
        // 'parallax barrier': new THREE.ParallaxBarrierEffect(this.renderer),
        // 'oculus rift': new THREE.OculusRiftEffect(this.renderer),
        // 'stereo': new THREE.StereoEffect(this.renderer),
		'none': this.renderer,
	};

	this.camera_z = -150;
	this.perspectiveCamera = new THREE.PerspectiveCamera(20, this.container.whratio, 1, 800);
	this.perspectiveCamera.position.set(0, 0, this.camera_z);
	this.perspectiveCamera.lookAt(new THREE.Vector3(0, 0, 0));
	this.orthographicCamera = new THREE.OrthographicCamera();
	this.orthographicCamera.position.set(0, 0, this.camera_z);
	this.orthographicCamera.lookAt(new THREE.Vector3(0, 0, 0));
	this.cameras = {
		 perspective: this.perspectiveCamera,
		orthographic: this.orthographicCamera,
	};
	this.camera = this.perspectiveCamera;

	this.slabNear = -50; // relative to the center of rot
	this.slabFar  = +50;

	var background = 0x000000;
	this.renderer.setClearColor(background, 1);

	this.scene = new THREE.Scene();
	this.scene.fog = new THREE.Fog(background, 100, 200);

	var directionalLight = new THREE.DirectionalLight(0xFFFFFF, 1.2);
	directionalLight.position.set(0.2, 0.2, -1).normalize();
	var ambientLight = new THREE.AmbientLight(0x202020);
	
	this.scene.add(directionalLight);
	this.scene.add(ambientLight);
	//this.scene.add(this.camera);

	this.controls = new THREE.TrackballControls(this.camera, this.container);
	this.controls.rotateSpeed = 1.0;
	this.controls.zoomSpeed = 1.2;
	this.controls.panSpeed = 0.8;

	this.controls.noZoom = false;
	this.controls.noPan = false;
	this.controls.norRotate = false;

	this.controls.staticMoving = false;
	this.controls.dynamicDampingFactor = 0.2;

	this.controls.keys = [ 65, 83, 68 ];
	this.controls.addEventListener( 'change', this.render.bind(this));

	this.render();
};

MolecularViewer.prototype = {
    
    addRepresentation: function (representation) {
    	representation.addToScene(this.scene);
    },

    render: function () {
    	this.controls.handleResize();
    	this.renderer.render(this.scene, this.camera);
    },

    animate: function () {
    	//console.log(this);
		window.requestAnimationFrame(this.animate.bind(this));
		this.controls.update();
	}
};


var PointRepresentation = function (coordinates) {
	// We take Float32 arrays cuz they're faster

	var geo = new THREE.Geometry();
	var mat = new THREE.PointCloudMaterial({
      					color: 0xFFFFFF,
      					size: 0.1,
      					fog: true,
    				});


	for (var p = 0; p < coordinates.length/3; p++) {
		var particle = new THREE.Vector3(coordinates[3 * p + 0],
										 coordinates[3 * p + 1],
										 coordinates[3 * p + 2]);
		geo.vertices.push(particle);
	}

	this.geometry = geo;
	this.material = mat;

	this.particleSystem = new THREE.PointCloud(this.geometry, this.material);
};


PointRepresentation.prototype = {

    update: function (coordinates) {
    	for (var p=0; p < coordinates.length/3; p++) {
    		this.geometry.vertices[p].x = coordinates[3 * p + 0];
    		this.geometry.vertices[p].y = coordinates[3 * p + 1];
    		this.geometry.vertices[p].z = coordinates[3 * p + 2];
    	}

    	this.particleSystem.geometry.verticesNeedUpdate = true;
    },

   	addToScene: function(scene) {
   		scene.add(this.particleSystem);
   	}
};
