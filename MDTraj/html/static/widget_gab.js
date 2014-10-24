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
    var HEIGHT = 600,
        WIDTH = 600,
        HEIGHT_PX = '600px',
        WIDTH_PX = '600px';

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
            var topology = this.model.get('topology');

            var buffer = decode(coords['data']);
            var view = new Float32Array(buffer);
 
            var rep = new PointLineRepresentation(view, topology.bonds);
            mv.addRepresentation(rep);

            this.update();
            
            this.pointRepresentation = rep;
            mv.zoomInto(view);
            mv.renderer.setSize(WIDTH, HEIGHT);

            // That was pretty hard.
            // The widget is added at THE VERY END, and this event gets called.
            this.model.on('displayed', function () {
                mv.animate();
                mv.controls.handleResize();
            });
            mv.render();
        },

        update : function () {

            console.log('MolecularView.update');
            mv.controls.handleResize();
            if (this.model.hasChanged('coordinates')) {

                var coords = this.model.get('coordinates');
            
                var buffer = decode(coords['data']);
                var view = new Float32Array(buffer);

                this.pointRepresentation.update({'coordinates': view});
                this.mv.render();
                console.log('Representation updated');
            }

            if (this.model.hasChanged('topology')) {
                var bonds = this.model.get('topology').bonds;
                this.pointRepresentation.update({'bonds': bonds});
            }

            return MolecularView.__super__.update.apply(this);
        },
    });


    WidgetManager.register_widget_view('MolecularView', MolecularView);
});