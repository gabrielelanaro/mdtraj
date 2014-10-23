import os
import warnings
from IPython.display import display, Javascript
from IPython.html.nbextensions import install_nbextension
with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    from pkg_resources import resource_filename

__all__ = ['enable_notebook']

_REQUIRE_CONFIG = Javascript('''
require.config({
    paths: {
        'three': '/nbextensions/three.min',
        'iview' : '/nbextensions/iview',
        'surface' : '/nbextensions/surface.min',
        'exporter' : '/nbextensions/objexporter',
        'filesaver' : '/nbextensions/filesaver',
        'base64-arraybuffer': '/nbextensions/base64-arraybuffer',
        'jqueryui': '/nbextensions/jquery-ui.min',
        'contextmenu': '/nbextensions/context',
        'TrackballControls' : '/nbextensions/TrackballControls',
        'molecularviewer': '/nbextensions/molecularviewer',

    },
    shim: {
        three: {
            exports: 'THREE'
        },
        iview: {
            deps: ['three', 'surface'],
            exports: 'iview'
        },

        molecularviewer: {
            deps: ['three', 'TrackballControls'],
            exports: 'MolecularViewer'
        },

        surface: {
            exports: 'ProteinSurface'
        },
        exporter: {
            deps: ['three'],
            exports: 'THREE.OBJExporter'
        },

        TrackballControls: {
            deps: ['three'],
            exports: 'THREE.TrackballControls',
        },

        jqueryui: {
            exports: "$"
        },
    },
});
''',
css  = ['//lab.jakiestfu.com/contextjs/context.standalone.css']
)

def enable_notebook():
    """Enable IPython notebook widgets to be displayed.

    This function should be called before using TrajectoryWidget.
    """
    libs = ['iview.js','surface.min.js','objexporter.js', 'TrackballControls.js', 'filesaver.js', 'base64-arraybuffer.js',
            'context.js', 'molecularviewer.js', 'three.min.js', 'jquery-ui.min.js']
    fns = [resource_filename('mdtraj', os.path.join('html', 'static', f)) for f in libs]
    install_nbextension(fns, verbose=0)
    display(_REQUIRE_CONFIG)

    widgets = ['widget_trajectory.js', 'widget_imagebutton.js', 'widget_gab.js']
    for fn in widgets:
        fn = resource_filename('mdtraj', os.path.join('html', 'static', fn))
        display(Javascript(filename=fn))
