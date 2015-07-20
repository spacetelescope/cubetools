from __future__ import print_function

from glue.core import Data, Component
from glue.config import data_factory
from glue.core.data_factories.helpers import has_extension

from cube_tools.core.data_objects import CubeData


@data_factory("STcube", has_extension("fits fit"))
def read_cube(filename, **kwargs):
    cube_data = CubeData.read(filename)

    data = Data()
    data.add_component(Component(cube_data), label="cube")
    print("Loaded successfully")

    return data
