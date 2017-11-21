# Licensed under a 3-clause BSD style license - see LICENSE.rst

from glue.core import Hub, HubListener, Data, DataCollection
from glue.core.message import DataCollectionAddMessage
from .layout import CubeVizLayout, COLOR, FLUX, ERROR, MASK


CUBEVIZ_LAYOUT = 'cubeviz_layout'


class CubevizManager(HubListener):

    def __init__(self, session):
        self._session = session
        self._hub = session.hub
        self._app = session.application

        self._empty_layout = \
            self._app.add_fixed_layout_tab(CubeVizLayout)
        self._app.close_tab(0, warn=False)
        self.hide_sidebar()

        self._hub.subscribe(
            self, DataCollectionAddMessage, handler=self.receive_message)

    def receive_message(self, message):
        data = message.data
        if data.meta.get(CUBEVIZ_LAYOUT, ''):
            # Assume for now the data is not yet in any tab

            if self._empty_layout is not None:
                cubeviz_layout = self._empty_layout
            else:
                cubeviz_layout = self._app.add_fixed_layout_tab(CubeVizLayout)

            try:
                self.setup_data(cubeviz_layout, data)
            finally:
                self._empty_layout = None

    def hide_sidebar(self):
        self._app._ui.main_splitter.setSizes([0, 300])

    def setup_data(self, cubeviz_layout, data):
        # Automatically add data to viewers and set attribute for split viewers
        image_viewers = [cubeviz_layout.image1._widget,
                         cubeviz_layout.image2._widget,
                         cubeviz_layout.image3._widget,
                         cubeviz_layout.image4._widget]

        for i, attribute in enumerate([FLUX, ERROR, MASK]):

            image_viewers[0].add_data(data)
            image_viewers[0].state.aspect = 'auto'
            image_viewers[0].state.color_mode = 'One color per layer'
            image_viewers[0].state.layers[i].attribute = data.id[attribute]

            image_viewers[1 + i].add_data(data)
            image_viewers[1 + i].state.aspect = 'auto'
            image_viewers[1 + i].state.layers[0].attribute = data.id[attribute]

        image_viewers[0].state.layers[0].color = COLOR[FLUX]
        image_viewers[0].state.layers[1].color = COLOR[ERROR]
        image_viewers[0].state.layers[2].color = COLOR[MASK]

        cubeviz_layout.add_data(data)

        index = self._app.get_tab_index(cubeviz_layout)
        self._app.tab_bar.rename_tab(index, "CubeViz: {}".format(data.label))
