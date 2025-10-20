import streamlit as st
import json
from agents.metrics.recorder import snapshot
from datetime import datetime

st.title('VoyageVerse Metrics Dashboard')

data = snapshot()
st.metric('Sessions', data.get('sessions', 0))
st.metric('Total Planning Time (s)', data.get('total_planning_time_seconds', 0.0))
st.metric('Total Savings', data.get('total_savings', 0.0))
st.metric('Avg Satisfaction', data.get('avg_satisfaction', 'N/A'))

st.write('Full snapshot:')
st.json(data)

if st.button('Export snapshot for CI'):
    fname = f'metrics_snapshot_{datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")}.json'
    with open(fname, 'w', encoding='utf-8') as f:
        json.dump(data, f)
    st.success(f'Wrote {fname}')
