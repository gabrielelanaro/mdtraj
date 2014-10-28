from __future__ import absolute_import
import base64
from itertools import groupby

import mdtraj as md

from IPython.display import display, Javascript
from IPython.html.widgets import DOMWidget, IntSliderWidget, ContainerWidget
from IPython.utils.traitlets import (Unicode, Bool, Bytes, CInt, Any,
                                     Dict, Enum, CFloat)

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
    topology = Dict(sync=True)
    point_size = CFloat(sync=True)

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

        # The topology gets changed immediately
        top = {}

        bondIndices = []
        for ai, aj in self.trajectory.topology.bonds:
            bondIndices.append((ai.index, aj.index))
        
        top['bonds'] = bondIndices
        top['atom_colors'] = [get_atom_color(a.element.symbol) for a in self.trajectory.topology.atoms]
        self.topology = top


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

def get_atom_color(atom_name):
    atomColors = {
        "H": 0xFFFFFF,
        "HE": 0xD9FFFF,
        "LI": 0xCC80FF,
        "BE": 0xC2FF00,
        "B": 0xFFB5B5,
        "C": 0x909090,
        "N": 0x3050F8,
        "O": 0xFF0D0D,
        "F": 0x90E050,
        "NE": 0xB3E3F5,
        "NA": 0xAB5CF2,
        "MG": 0x8AFF00,
        "AL": 0xBFA6A6,
        "SI": 0xF0C8A0,
        "P": 0xFF8000,
        "S": 0xFFFF30,
        "CL": 0x1FF01F,
        "AR": 0x80D1E3,
        "K": 0x8F40D4,
        "CA": 0x3DFF00,
        "SC": 0xE6E6E6,
        "TI": 0xBFC2C7,
        "V": 0xA6A6AB,
        "CR": 0x8A99C7,
        "MN": 0x9C7AC7,
        "FE": 0xE06633,
        "CO": 0xF090A0,
        "NI": 0x50D050,
        "CU": 0xC88033,
        "ZN": 0x7D80B0,
        "GA": 0xC28F8F,
        "GE": 0x668F8F,
        "AS": 0xBD80E3,
        "SE": 0xFFA100,
        "BR": 0xA62929,
        "KR": 0x5CB8D1,
        "RB": 0x702EB0,
        "SR": 0x00FF00,
        "Y": 0x94FFFF,
        "ZR": 0x94E0E0,
        "NB": 0x73C2C9,
        "MO": 0x54B5B5,
        "TC": 0x3B9E9E,
        "RU": 0x248F8F,
        "RH": 0x0A7D8C,
        "PD": 0x006985,
        "AG": 0xC0C0C0,
        "CD": 0xFFD98F,
        "IN": 0xA67573,
        "SN": 0x668080,
        "SB": 0x9E63B5,
        "TE": 0xD47A00,
        "I": 0x940094,
        "XE": 0x429EB0,
        "CS": 0x57178F,
        "BA": 0x00C900,
        "LA": 0x70D4FF,
        "CE": 0xFFFFC7,
        "PR": 0xD9FFC7,
        "ND": 0xC7FFC7,
        "PM": 0xA3FFC7,
        "SM": 0x8FFFC7,
        "EU": 0x61FFC7,
        "GD": 0x45FFC7,
        "TB": 0x30FFC7,
        "DY": 0x1FFFC7,
        "HO": 0x00FF9C,
        "ER": 0x00E675,
        "TM": 0x00D452,
        "YB": 0x00BF38,
        "LU": 0x00AB24,
        "HF": 0x4DC2FF,
        "TA": 0x4DA6FF,
        "W": 0x2194D6,
        "RE": 0x267DAB,
        "OS": 0x266696,
        "IR": 0x175487,
        "PT": 0xD0D0E0,
        "AU": 0xFFD123,
        "HG": 0xB8B8D0,
        "TL": 0xA6544D,
        "PB": 0x575961,
        "BI": 0x9E4FB5,
        "PO": 0xAB5C00,
        "AT": 0x754F45,
        "RN": 0x428296,
        "FR": 0x420066,
        "RA": 0x007D00,
        "AC": 0x70ABFA,
        "TH": 0x00BAFF,
        "PA": 0x00A1FF,
        "U": 0x008FFF,
        "NP": 0x0080FF,
        "PU": 0x006BFF,
        "AM": 0x545CF2,
        "CM": 0x785CE3,
        "BK": 0x8A4FE3,
        "CF": 0xA136D4,
        "ES": 0xB31FD4,
        "FM": 0xB31FBA,
    }

    return atomColors[atom_name.upper()]
