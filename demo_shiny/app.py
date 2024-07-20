from shiny import App, Inputs, Outputs, Session, render, ui, run_app, reactive
from shiny.types import FileInfo
import io
import pandas as pd
import numpy as np
import nest_asyncio

nest_asyncio.apply()

app_ui = ui.page_fluid(
    ui.input_dark_mode(),
    ui.card(
        ui.input_file("file_input", "Input", accept=[".xlsx"], multiple=False),
        ui.input_action_button("re_gen", "Random"),
        ui.download_button("download", "Download xlsx"),
    ),

    ui.card(
        ui.output_data_frame("df_render"),
    ),
    ui.card(
        ui.output_data_frame("df_file"),
    )
)

def server(input: Inputs, output: Outputs, session: Session):
    @reactive.calc
    def parse_file():
        file: list[FileInfo] | None = input.file_input()
        if file is None:
            return pd.DataFrame()
        return pd.read_excel(
            file[0]["datapath"]
        )

    df = reactive.value(pd.DataFrame())

    @reactive.effect
    @reactive.event(input.re_gen)
    def _():
        df.set(pd.DataFrame(np.random.randint(0,100,size=(100, 4)), columns=list('ABCD')))

    @render.download(filename='teste.xlsx')
    def download():
        with io.BytesIO() as buf:
            df.get().to_excel(buf, index = False)
            buf.seek(0)
            yield buf.getvalue()
    
    @render.data_frame
    def df_render():
        if df.get().empty:
            return pd.DataFrame()
        return render.DataTable(df.get())
    
    @render.data_frame
    def df_file():
        df_input = parse_file()
        if df_input.empty:
            return pd.DataFrame()
        return render.DataTable(df_input)

app = App(app_ui, server)

run_app(launch_browser=True)
