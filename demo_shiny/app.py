from shiny import App, Inputs, Outputs, Session, render, ui, run_app
import io
import pandas as pd
import numpy as np
import nest_asyncio

nest_asyncio.apply()

app_ui = ui.page_fluid(
    ui.download_button("download", "Download xlsx")
)
df = pd.DataFrame(np.random.randint(0,100,size=(100, 4)), columns=list('ABCD'))
def server(input: Inputs, output: Outputs, session: Session):
    @render.download(filename='teste.xlsx')
    def download():
        with io.BytesIO() as buf:
            df.to_excel(buf)
            buf.seek(0)
            yield buf.getvalue()

app = App(app_ui, server)

run_app()
