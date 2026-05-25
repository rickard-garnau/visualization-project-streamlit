[← Back to Main Project Documentation](../../README.md)

# STHLMs PULS 🎭

A data-driven cultural guide for Stockholm — helping you discover events, plan around the weather, and explore the city's cultural scene.

## About

STHLMs PULS combines event data from multiple sources with real-time weather forecasts to help culturally curious Stockholmers find the best time to head out.
This streamlit dashboard is built as an extension of a group project that we did with UX.

## STHLMs PULS APP
[**Explore the Live App →**](https://sthlmpuls.streamlit.app/)

## Data Sources

| Source | Type |
|---|---|
| Ticketmaster API | Concerts, sports & entertainment |
| VisitStockholm | Cultural events & exhibitions |
| Fasching | Jazz & club events |
| Berns | Club & live events |
| Open-Meteo API | Weather forecast (no API key required) |

## Features

- 📅 **This Week** — daily event counts combined with a 7-day weather forecast, highlighting the warmest day of the week
- 📊 **Events** — browse and filter cultural events by genre, venue and date
- 🗃️ **Raw Data** — explore the underlying dataset
- 🗺️ **Venue Map** — explore where events are happening across Stockholm, filterable by genre, venue and date
- 📈 **Cultural Calendar** — see how events are distributed across segments throughout the year

## Project Structure
```
streamlit/sthlm_puls/src/sthlm_puls/
├── assets/             # Static files used in the app
│   ├── data/           # App-specific datasets
│   ├── image/          # Header & Footer images
│   └── markdown/       # Text content and documentation files
├── components/         # Reusable UI elements and logic
│   ├── map.py          # Interactive venue map (pydeck/Mapbox)
│   ├── charts.py       # Visualization functions (Matplotlib)
│   ├── filters.py      # Data filtering logic
│   ├── kpis.py         # Live Key Performance Indicator calculations
│   └── weather.py      # Weather-related components/API logic

├── pages/              # Multi-page app navigation
│   ├── events.py       # Detailed event views
│   ├── home.py         # Main dashboard landing page
│   └── raw_data.py     # Data inspection
├── utils/              # Utility functions and shared logic
│   ├── constants.py    # Fixed values (colors, categories, etc.)
│   └── helpers.py      # General support functions
└── app.py              # Main entry point for the Streamlit app
```

## Getting Started
**Clone repository**
```bash
git clone git@github.com:rickard-garnau/visualization-project-streamlit.git
cd visualization-project-streamlit
```

**Requirements:** Python 3.11+, [uv](https://github.com/astral-sh/uv)

**Install dependencies:**
```bash
uv sync
```

**Run the app:**
```bash
cd streamlit/sthlm_puls/src/sthlm_puls
uv run streamlit run app.py
```

## Contributors
- Lisa Yllander
- Rickard Garnau