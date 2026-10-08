from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st


st.set_page_config(
    page_title="Global Relations Tracker",
    page_icon="🌍",
    layout="wide",
)


DATA_PATH = Path(__file__).parent / "data" / "foreign_policy_events.csv"
SIGNAL_SCORE = {"Cooperative": 1, "Neutral": 0, "Tense": -1}


@st.cache_data
def load_events(uploaded_file=None):
    if uploaded_file is not None:
        return pd.read_csv(uploaded_file)
    return pd.read_csv(DATA_PATH)


def clean_events(frame: pd.DataFrame) -> pd.DataFrame:
    required = {
        "date", "country_a", "country_b", "issue_area", "event_type",
        "headline", "summary", "relationship_signal", "source_url",
    }
    missing = required - set(frame.columns)
    if missing:
        raise ValueError(f"Missing columns: {', '.join(sorted(missing))}")
    result = frame.copy()
    result["date"] = pd.to_datetime(result["date"], errors="coerce")
    result["signal_score"] = result["relationship_signal"].map(SIGNAL_SCORE).fillna(0)
    result["relationship"] = result["country_a"] + " – " + result["country_b"]
    return result.dropna(subset=["date"])


st.title("🌍 Global Relations & Foreign Policy Tracker")
st.caption("A structured view of bilateral diplomatic events, issue areas, and relationship signals.")

with st.sidebar:
    st.header("Filters")
    uploaded = st.file_uploader("Upload an events CSV", type="csv")

try:
    events = clean_events(load_events(uploaded))
except Exception as exc:
    st.error(f"Could not load the dataset: {exc}")
    st.stop()

with st.sidebar:
    countries = sorted(set(events["country_a"]) | set(events["country_b"]))
    selected_countries = st.multiselect("Countries", countries, default=countries)
    issue_options = sorted(events["issue_area"].unique())
    selected_issues = st.multiselect("Issue areas", issue_options, default=issue_options)
    signal_options = sorted(events["relationship_signal"].unique())
    selected_signals = st.multiselect("Relationship signal", signal_options, default=signal_options)
    start_date = events["date"].min().date()
    end_date = events["date"].max().date()
    selected_dates = st.date_input("Date range", value=(start_date, end_date))

if isinstance(selected_dates, tuple) and len(selected_dates) == 2:
    date_start, date_end = selected_dates
else:
    date_start = date_end = selected_dates

filtered = events[
    events["country_a"].isin(selected_countries)
    & events["country_b"].isin(selected_countries)
    & events["issue_area"].isin(selected_issues)
    & events["relationship_signal"].isin(selected_signals)
    & events["date"].dt.date.between(date_start, date_end)
].copy()

metric_cols = st.columns(4)
metric_cols[0].metric("Events tracked", len(filtered))
metric_cols[1].metric("Country pairs", filtered["relationship"].nunique())
metric_cols[2].metric("Issue areas", filtered["issue_area"].nunique())
mean_signal = filtered["signal_score"].mean() if not filtered.empty else 0
metric_cols[3].metric("Average signal", f"{mean_signal:+.2f}")

if filtered.empty:
    st.warning("No events match the selected filters.")
    st.stop()

left, right = st.columns(2)
with left:
    st.subheader("Events by issue area")
    issue_counts = filtered["issue_area"].value_counts().rename_axis("issue_area").reset_index(name="events")
    st.plotly_chart(px.bar(issue_counts, x="issue_area", y="events", color="issue_area"), use_container_width=True)

with right:
    st.subheader("Relationship signals")
    signal_counts = filtered["relationship_signal"].value_counts().rename_axis("signal").reset_index(name="events")
    st.plotly_chart(px.pie(signal_counts, names="signal", values="events", hole=0.45), use_container_width=True)

st.subheader("Relationship overview")
relationship_summary = (
    filtered.groupby("relationship", as_index=False)
    .agg(events=("event_id", "count"), average_signal=("signal_score", "mean"))
    .sort_values(["average_signal", "events"], ascending=[False, False])
)
st.dataframe(relationship_summary, use_container_width=True, hide_index=True)

st.subheader("Foreign-policy timeline")
timeline = filtered.sort_values("date")
st.plotly_chart(
    px.scatter(
        timeline,
        x="date",
        y="relationship",
        color="relationship_signal",
        symbol="event_type",
        hover_data=["issue_area", "headline", "source_url"],
    ),
    use_container_width=True,
)

st.subheader("Event details")
for _, row in timeline.iloc[::-1].iterrows():
    with st.expander(f"{row['date'].date()} · {row['headline']}"):
        st.write(row["summary"])
        st.write(f"**Countries:** {row['country_a']} and {row['country_b']}")
        st.write(f"**Issue:** {row['issue_area']} · **Signal:** {row['relationship_signal']}")
        st.markdown(f"[Open source]({row['source_url']})")

st.info("Demo note: replace the illustrative records with verified events and official source links before presenting this project as research.")
