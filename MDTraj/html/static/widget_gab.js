require([
    "jquery",
    "widgets/js/widget",
    "molecularviewer",
    "exporter",
    "filesaver",
    "contextmenu",
    "base64-arraybuffer", // provides decode
    'jqueryui',
    'TrackballControls',
    ],
function($, WidgetManager) {
    var HEIGHT = 300,
        WIDTH = 300,
        HEIGHT_PX = '300px',
        WIDTH_PX = '300px';

    var MolecularView = IPython.DOMWidgetView.extend({

        render : function() {
            var canvas = $("<canvas/>").height(HEIGHT).width(WIDTH);
            var mv = new MolecularViewer(canvas);
            this.mv = mv;

            var container = $('<div/>').css({width: HEIGHT_PX, height: WIDTH_PX})
                .resizable({
                    aspectRatio: 1,
                    resize: function(event, ui) {
                        mv.renderer.setSize(ui.size.width, ui.size.height);
                        mv.controls.handleResize();
                    },
                    stop : function(event, ui) {
                        mv.render();
                    },
                });

            container.append(canvas);
            this.setElement(container);


            var coords = this.model.get('coordinates');
            
            var buffer = decode(coords['data']);
            var view = new Float32Array(buffer);
 
            var rep = new PointRepresentation(view);
            mv.addRepresentation(rep);

            this.update();
            
            this.pointRepresentation = rep;
            mv.animate();
        },

        update : function () {

            console.log('MolecularView.update');
            if (this.model.hasChanged('coordinates')) {

                var coords = this.model.get('coordinates');
            
                var buffer = decode(coords['data']);
                var view = new Float32Array(buffer);

                this.pointRepresentation.update(view);
                this.mv.render();
                console.log('Representation updated');
            }
            // // Transform the coordinates back to javascript TypedArray
            // //var buffer = decode(this.model.attributes._frameData.coordinates['data']);
            // //var view = new Float32Array(buffer);
            // //var coordinates = [];
            // //for (var i = 0; i < this.model.attributes._frameData.coordinates['shape'][0]; i++) {
            // //  coordinates[i] = view.subarray(i * 3, (i + 1)*3);
            // //}

            // //this.iv.loadCoordinates(coordinates);
            // //this.iv.loadAtomAttributes(this.model.attributes._frameData.secondaryStructure);

            // //var options = this.getOptions()
            // //this.iv.rebuildScene(options)
            // this.mv.render()

            return MolecularView.__super__.update.apply(this);
        },
    });


    WidgetManager.register_widget_view('MolecularView', MolecularView);
});