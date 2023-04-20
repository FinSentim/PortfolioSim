from dash import html, dcc, callback, Input, Output
from . import ids
from datetime import date


date_selector = html.Div([
        dcc.Store(id=ids.SELECTED_DATE, data={}),
        dcc.DatePickerRange(
            start_date_placeholder_text="Start Period",
            end_date_placeholder_text="End Period",
            calendar_orientation='horizontal',
            id=ids.DATE_SELECT,
        ),
    ],
)


@callback(
    Output(ids.SELECTED_DATE, "data"),
    Input(ids.DATE_SELECT, "start_date"),
    Input(ids.DATE_SELECT, "end_date")
)
def update_selected_date(start_date, end_date):
    if start_date is not None and end_date is not None:
        start_date_object = date.fromisoformat(start_date)
        end_date_object = date.fromisoformat(end_date)
        x = {"start_date": start_date_object, "end_date": end_date_object}
        print(x)
        return x
    else:
        return {}
