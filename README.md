# Global Relations & Foreign Policy Tracker

An interview-ready political-science data project that organizes bilateral foreign-policy events into a searchable dashboard.

## Problem

Foreign-policy developments are scattered across statements, agreements, negotiations, and news reports. This project creates a structured way to explore how country relationships evolve across issue areas such as trade, defence, technology, climate, energy, and security.

## Features

- Filter by country, issue area, relationship signal, and date range
- Track cooperative, neutral, and tense events
- Summarize country pairs and average relationship signals
- Visualize issue distribution and relationship signals
- Explore a chronological foreign-policy timeline
- Upload a replacement CSV without changing the application code
- Open the source link for each event

## Technology

- Python
- Streamlit
- Pandas
- Plotly
- CSV data modeling

This is an analytical dashboard rather than a predictive political model. It does not claim to objectively measure international relations; the relationship signal is a transparent human-coded field that should be supported by the cited source.

## Run locally

From this folder:

    python -m venv .venv
    .venv\\Scripts\\Activate.ps1
    python -m pip install -r requirements.txt
    streamlit run app.py

The dashboard opens at the local Streamlit URL shown in the terminal.

## Dataset format

The CSV must contain these columns:

    event_id,date,country_a,country_b,issue_area,event_type,headline,summary,relationship_signal,source_url

Allowed relationship signals are:

- Cooperative: an event indicates collaboration or agreement
- Neutral: an event is consultative or mixed without a clear positive/negative signal
- Tense: an event indicates disagreement, dispute, or escalation

The included data is illustrative demo data. Before using the project for research or an interview submission, replace it with verified events and official source links.

## Interview explanation

I built a foreign-policy event tracker to turn scattered diplomatic developments into a structured analytical dataset. I designed the data schema around country pairs, issue areas, event types, dates, source links, and transparent relationship signals. I then used Pandas for filtering and aggregation and Streamlit/Plotly to create an interactive dashboard showing trends and timelines. The project demonstrates policy research, data modeling, source discipline, and communication of analysis through a simple user-facing tool.

## Possible extensions

- Add UN voting-alignment scores
- Add a source-verification workflow
- Add a map view of country relationships
- Add sentiment analysis only as a supplementary signal, not as the final policy judgment
- Store records in SQLite or PostgreSQL instead of CSV
