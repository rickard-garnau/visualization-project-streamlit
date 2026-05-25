import streamlit as st
import pandas as pd
from datetime import datetime
from streamlit_folium import st_folium
from sthlm_puls.utils.constants import DATA_PATH, MARKDOWN_PATH
from sthlm_puls.components.weather import fetch_weather_forecast
from sthlm_puls.components.charts import plot_events_weather, plot_events_weekday, plot_segment_over_time
from sthlm_puls.components.filters import venue_filter, genre_filter, date_filter
from sthlm_puls.components.kpis import total_events_kpi, unique_venues_kpi, total_events_this_month_kpi, total_events_today_kpi
from sthlm_puls.utils.helpers import read_textfile, get_events_df
from sthlm_puls.components.map import events_map

def events_layout():
    st.title("📅 This Week in Stockholm")
    st.markdown("Stockholm never stands still — there's always something going on.\n "
                "The **warmest day** of the week is highlighted to help you decide whether to catch an outdoor concert, "
                "visit a gallery, or explore the city.")

    # Load data
    weather = fetch_weather_forecast(days=7)
    events = get_events_df()

    # Count events per day
    events_per_day = (
        events[events["date"].dt.date.between(
            weather["date"].dt.date.min(),
            weather["date"].dt.date.max()
        )]
        .groupby(events["date"].dt.date)
        .size()
        .reset_index(name="num_events")
    )
    events_per_day["date"] = pd.to_datetime(events_per_day["date"])

    # Merge
    df_merged = weather.merge(events_per_day, on="date", how="left")
    df_merged["num_events"] = df_merged["num_events"].fillna(0).astype(int)

    # Plot
    emoji_html = "".join(
        f'<span style="display:inline-block;width:{100 / len(df_merged):.1f}%;text-align:center;font-size:1.2rem;">{row["icon"]}</span>'
        for _, row in df_merged.iterrows()
    )
    st.markdown(f'<div style="width:100%;display:flex;">{emoji_html}</div>', unsafe_allow_html=True)

    fig = plot_events_weather(df_merged)
    st.pyplot(fig)

    st.subheader("Explore to find what your next event will be")
    st.markdown("Filter by date, venue or genre to find exactly what you're looking for.")

    # Reset button
    if st.session_state.get("reset"):
        st.session_state["venue_filter"] = "All"
        st.session_state["genre_filter"] = "All"
        st.session_state["date_filter"] = (
            events["date"].min().date(),
            events["date"].max().date()
        )
        st.session_state["reset"] = False

    # Date, venue and genre filters
    col1,col2, col3, col4 = st.columns([3, 3, 3, 1])
    with col1:
        date_range = date_filter(events)
    with col2:
        venue = venue_filter(events)
    with col3:
        genre = genre_filter(events)
    with col4:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("Reset"):
            st.session_state["reset"] = True
            st.rerun()

    # Filter table
    filtered = events.copy()

    if venue != "All":
        filtered = filtered[filtered["venue_name"] == venue]

    if genre != "All":
        filtered = filtered[filtered["genre"] == genre]

    if len(date_range) == 2:
        filtered = filtered[
            (filtered["date"].dt.date >= date_range[0]) &
            (filtered["date"].dt.date <= date_range[1])
            ]

    st.dataframe(filtered[["name", "venue_name", "date", "genre"]]
                 .assign(date=filtered["date"].dt.strftime("%y-%m-%d"))
                 .rename(columns={
                    "name": "Event",
                    "venue_name": "Venue",
                    "date": "Date",
                    "genre": "Genre"})
                    .reset_index(drop=True))

    st.subheader("At a glance")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        count = total_events_kpi(filtered, genre)
        st.metric(label="Total events", value=count)
    with col2:
        count = unique_venues_kpi(filtered, venue)
        st.metric(label="Unique venues", value=count)
    with col3:
        month_name = datetime.today().strftime("%B")
        st.metric(label=f"Total events this month ({month_name})", value=total_events_this_month_kpi(filtered))
    with col4:
        day_today = datetime.today().strftime("%A")
        st.metric(label=f"Total events today ({day_today})", value=total_events_today_kpi(filtered))

    st.caption("Numbers reflect your current filter selection.")

    # map
    st.subheader("Where to go?")
    st.markdown("Events are concentrated in central Stockholm — zoom in to explore venues by neighbourhood.")

    m = events_map(filtered)
    st_folium(m, use_container_width=True, height=500)

    st.subheader("When to go out?")
    st.markdown("Stockholm's cultural life peaks on weekends — Saturday alone accounts for nearly a third of all weekly events."
                "If you prefer smaller crowds, mid-week offers a more low-key experience with fewer but often more intimate events.")


    fig = plot_events_weekday(events)
    st.pyplot(fig)

    st.subheader("How is the scene distributed over the year?")
    st.markdown("Arts & Theatre dominates Stockholm's cultural scene in spring, while Music maintains a steady presence through the year. "
                "July is the quietest month across all segments.")

    st.pyplot(plot_segment_over_time(events))
    st.markdown("Note: Event activity naturally dips during summer, picking up again in the fall as venues announce their autumn programmes.")


if __name__ == "__main__":
    events_layout()