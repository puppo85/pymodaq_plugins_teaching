from pymodaq.extensions.data_mixer.model import DataMixerModel
from pymodaq_data.data import DataToExport
from pymodaq.utils.data import DataFromPlugins
from pymodaq_gui.parameter import Parameter
import laserbeamsize as lbs
import numpy as np

class DataMixerTraining(DataMixerModel):
    params = []

    def ini_model(self):
        pass

    def update_settings(self, param: Parameter):
        if param.name() == 'get_data':
            ...

    def process_dte(self, dte: DataToExport):
        #now we want to get a numpy array from the dte
        data2d=dte.get_data_from_name('BSCamera')[0]
        x, y, d_major, d_minor, phi = lbs.beam_size(data2d)
        dte= DataToExport('analyseddata', data=[DataFromPlugins(name='x', data=[np.atleast_1d(x),np.atleast_1d(y)],
                                                             label=['x','y']),
                                             DataFromPlugins(name='d_major', data=[np.atleast_1d(d_major)],
                                                            label='d_major'),
                                             DataFromPlugins(name='d_minor', data=[np.atleast_1d(d_minor)],
                                                             label='d_minor'),
                                             ])

        return dte