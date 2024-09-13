import os

import dash_split_pane
import folium
import geopandas
from dash import html, Output, Input, State
from folium.plugins import MarkerCluster

from src.app.abstract_app import AbstractApp
from src.app.components import BaseComponent
from src.app.components.choose_form.choose_form import ChooseForm
from src.app.components.input.input_projection_form import ProjectionToForm
from src.app.components.output.output_form import OutputForm
from src.app.components.tabs.tabs import Tabs


class SplitPane(BaseComponent):
    def __init__(self, app: AbstractApp):
        super().__init__(app)
        split_pane = dash_split_pane.DashSplitPane(
            children=[
                html.Div(
                    children=[
                        ChooseForm(self.app).get_layout(),
                        Tabs(self.app).get_layout(),
                        ProjectionToForm(self.app).get_layout(),
                        OutputForm(self.app).get_layout()
                    ],
                    className='column-gap small-padding'
                ),
                html.Iframe(
                    id="map", height="100%", width='100%',
                    style={'padding-left': "10px"}
                )
            ],
            id="splitter",
            split="vertical",
            minSize=400,
            size=600,
            maxSize=800,
            style={'padding': "5px"}
        )
        self.layout = split_pane
        self.init_callbacks()

    def init_callbacks(self):

        @self.dash_app.callback(
            Output('map', 'srcDoc'),
            Input('points', 'data'),
            Input('shape_files', 'data'),
            State('tabs_select', 'active_tab')
        )
        def set_map(points, shape_files, active_tab):
            if points is None:
                points = []
            map_frame = folium.Map(location=[62, 75], zoom_start=4)
            if active_tab == 'shape_tab' and shape_files is not None:
                for file in shape_files:
                    geo_file = geopandas.read_file(file)
                    folium.GeoJson(geo_file, popup=os.path.basename(file)).add_to(map_frame)
            else:
                marker_cluster = MarkerCluster().add_to(map_frame)
                for point in points:
                    folium.Marker(
                        location=[point['latitude'], point['longitude']],
                        popup=f'{point["id"]}',
                        icon=folium.Icon(color="blue")
                    ).add_to(marker_cluster)
            return map_frame.get_root().render()

        @self.dash_app.callback(
            Output('points', 'data'),
            Input('manual_points', 'data'),
            Input('excel_points', 'data'),
            State('tabs_select', 'active_tab')
        )
        def set_points(manual_points, excel_points, selected_tab):
            if selected_tab == 'manual_tab':
                return manual_points
            if selected_tab == 'excel_tab':
                return excel_points
            return []
