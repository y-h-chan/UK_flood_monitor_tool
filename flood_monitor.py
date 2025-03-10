from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from markupsafe import Markup
import requests
import pandas as pd
import io
from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import base64
from datetime import datetime, timedelta
from dateutil import parser


def fetch_stations():
    """Fetches the list of stations from the API synchronously."""
    try:
        response = requests.get(STATION_API_URL)
        response.raise_for_status()
        stations_data = response.json()["items"]
        stations = []
        for station in stations_data:
            if "notation" in station and "label" in station:
                label = station["label"]
                if isinstance(label, list):  # Handle case where label is a list
                    label_str = " ".join(
                        map(str, label)
                    )  # Convert list to space-separated string, or handle as needed
                else:
                    label_str = str(label)  # Ensure label is treated as a string
                stations.append((label_str, station["notation"]))
        stations.sort(key=lambda x: x[0].lower())
        return stations
    except requests.exceptions.RequestException as e:
        print(f"Error fetching stations: {e}")
        return []


def fetch_station_readings(
    station_id,
):  # Synchronous version (using requests - kept for comparison)
    """Fetches readings for a specific station for the last 24 hours synchronously."""
    now = datetime.utcnow()
    past_24h = now - timedelta(hours=24)
    start_date_str = str(past_24h.isoformat(timespec="seconds") + "Z")
    query_params = {
        "since": start_date_str,
    }
    api_url = f"{READINGS_API_URL}/id/measures/{station_id}/readings"
    try:
        response = requests.get(api_url, params=query_params)
        response.raise_for_status()
        readings_data = response.json()["items"]
        if not readings_data:
            return None, "No readings found for this station in the last 24 hours."

        df = pd.DataFrame(readings_data)
        if "dateTime" in df.columns and "value" in df.columns:
            df["dateTime"] = df["dateTime"].apply(parser.parse)
            df = df[["dateTime", "value", "measure"]]
            df = df.sort_values(by="dateTime")
            return df, None
        else:
            return None, "Data format from API is unexpected."

    except requests.exceptions.RequestException as e:
        error_message = f"Error fetching readings for station {station_id}: {e}"
        print(error_message)
        return None, error_message
    except ValueError as e:
        error_message = f"Error processing readings data for station {station_id}: {e}"
        print(error_message)
        return None, error_message


def create_plot_and_table(df, station_label):
    """Creates a Matplotlib plot and HTML table from the readings DataFrame."""
    if df is None:
        return None, None

    fig = Figure(figsize=(10, 6))
    ax = fig.add_subplot(111)
    df.filter(like=df["measure"].iloc[0])
    ax.plot(df["dateTime"], df["value"], marker="o", linestyle="-")
    ax.set_xlabel("Time")
    ax.set_ylabel(f"Reading Value ({df['measure'].iloc[0].split('/')[-1]})")
    ax.set_title(f"Station: {station_label} - Readings Last 24 Hours")
    fig.autofmt_xdate()

    png_image = io.BytesIO()
    FigureCanvas(fig).print_png(png_image)
    plot_base64_string = base64.b64encode(png_image.getvalue()).decode("utf-8")
    plot_url = f"data:image/png;base64,{plot_base64_string}"

    table_html = df.to_html(classes="table table-striped table-bordered", index=False)

    return plot_url, Markup(table_html)


app = FastAPI()

templates = Jinja2Templates(directory="templates")

STATION_API_URL = "https://environment.data.gov.uk/flood-monitoring/id/measures"
READINGS_API_URL = "https://environment.data.gov.uk/flood-monitoring/"

global stations
stations = fetch_stations()


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):  # Make route function async
    error_message = None
    plot_url = None
    table_html = None
    selected_station_label = None

    if not stations:
        error_message = "Failed to load station list from API."

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "stations": stations,
            "plot_url": plot_url,
            "table_html": table_html,
            "error_message": error_message,
            "selected_station_label": selected_station_label,
        },
    )


@app.post("/", response_class=HTMLResponse)
async def process_station(
    request: Request, station_id: str = Form(...), station_label: str = Form(...)
):  # Make route function async and use Form for data
    error_message = None
    plot_url = None
    table_html = None

    if station_id:
        readings_df, error_msg = fetch_station_readings(station_id)
        if readings_df is not None:
            plot_url, table_html = create_plot_and_table(readings_df, station_label)
        else:
            error_message = (
                error_msg
                or f"Could not retrieve readings for station ID: {station_id}."
            )
    else:
        error_message = "No station selected."

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "stations": stations,
            "plot_url": plot_url,
            "table_html": table_html,
            "error_message": error_message,
            "selected_station_label": station_label,
        },
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("flood_monitor:app", host="0.0.0.0", port=8000, reload=True)
