import numpy as np

from pymodaq_utils.utils import ThreadCommand
from pymodaq_data.data import DataToExport, Axis
from pymodaq_gui.parameter import Parameter

from pymodaq.control_modules.viewer_utility_classes import DAQ_Viewer_base, comon_parameters, main
from pymodaq.utils.data import DataFromPlugins

from pymodaq_plugins_mockexamples.daq_viewer_plugins.plugins_2D.daq_2Dviewer_BSCamera import DAQ_2DViewer_BSCamera
import laserbeamsize as lbs


class DAQ_2DViewer_BSProfiler(DAQ_2DViewer_BSCamera):

    params = DAQ_2DViewer_BSCamera.params +  [
        {'title': 'plot x,y', 'name': 'plot1', 'type': 'bool', 'value': True},
        {'title': 'plot Dmajor', 'name': 'plot2', 'type': 'bool', 'value': True},
        {'title': 'plot Dminor', 'name': 'plot3', 'type': 'bool', 'value': True},
    ]
    def grab_data(self, Naverage=1, **kwargs):
        """Start a grab from the detector

        Parameters
        ----------
        Naverage: int
            Number of hardware averaging (if hardware averaging is possible, self.hardware_averaging should be set to
            True in class preamble and you should code this implementation)
        kwargs: dict
            others optionals arguments
        """
        ## TODO for your custom plugin: you should choose EITHER the synchrone or the asynchrone version following
        data=self.average_data(Naverage)  #if you do not redife you do not need super
        beam=data[0].data[0]
        x, y, d_major, d_minor, phi = lbs.beam_size(beam)
        #print(f"Beam center: ({x:.0f}, {y:.0f})")
        #print(f"Major axis:  {d_major:.0f} pixels")
        #print(f"Minor axis:  {d_minor:.0f} pixels")
        #print(f"Rotation:    {phi * 180 / 3.1416:.0f}° CCW")


        dte = DataToExport('dio_cane', data=[DataFromPlugins(name='beam', data=[beam]),
                                             DataFromPlugins(name='x', data=[np.atleast_1d(x),np.atleast_1d(y)],
                                                             label=['x','y'],do_plot=self.settings.child('plot1').value()),
                                             DataFromPlugins(name='d_major', data=[np.atleast_1d(d_major)],
                                                            label='d_major',do_plot=self.settings.child('plot2').value()),
                                             DataFromPlugins(name='d_minor', data=[np.atleast_1d(d_minor)],
                                                             label='d_minor',do_plot=self.settings.child('plot3').value()),
                                             ])



        self.dte_signal.emit(dte)



if __name__ == '__main__':
    main(__file__)
