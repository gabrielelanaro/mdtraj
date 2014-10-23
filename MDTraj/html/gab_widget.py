from __future__ import absolute_import
import base64
from itertools import groupby

import mdtraj as md

from IPython.display import display, Javascript
from IPython.html.widgets import DOMWidget, IntSliderWidget, ContainerWidget
from IPython.utils.traitlets import (Unicode, Bool, Bytes, CInt, Any,
                                     Dict, Enum)

__all__ = ['MolecularViewer']


class MolecularViewer(DOMWidget):

    # Name of the javascript class which this widget syncs against on the
    # browser side. To work correctly, this javascript class has to be
    # registered and loaded in the browser before this widget is constructed
    # (that's what enable_notebook() does)
    _view_name = Unicode('MolecularView', sync=True)

    frame = CInt(0, help='Which frame from the trajectory to display')
    trajectory = Any()

    # The essence of the IPython interactive widget API on the python side is
    # that by declaring traitlets with sync=True, these variables are
    # automatically synced by the IPython runtime between this class in Python
    # and the browser-side model. Changes to these attributes are propagated
    # automatically to the browser (and changes on the browser side can trigger
    # events on this class too, although we're not using that feature).
    coordinates = Dict(sync=True)

    def __init__(self, trajectory, frame=0, **kwargs):
        super(MolecularViewer, self).__init__(**kwargs)
        self.trajectory = trajectory
        self.frame = frame
        self.coordinates = encode_numpy(self.trajectory.xyz[self.frame])

    def _frame_changed(self, name, old, new):
        """Automatically called by the traitlet system when self.frame is modified"""
        self.coordinates = encode_numpy(self.trajectory.xyz[self.frame])

    def _trajectory_changed(self, name, old, new):
        """Automatically called by the traitlet system when self.trajectory is modified"""
        self.trajectory = new
        self.frame = 0


# Utility functions

def encode_numpy(array):
    '''Encode a numpy array as a base64 encoded string. Returns a dictionary containing the fields:

    - *data*: the base64 string
    - *type*: the array type
    - *shape*: the array shape

    '''
    return {'data' : base64.b64encode(array.data),
            'type' : array.dtype.name,
            'shape': array.shape}
