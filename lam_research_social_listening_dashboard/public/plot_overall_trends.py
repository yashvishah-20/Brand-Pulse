import json
import plotly.graph_objs as go
import os

# Path setup
base_dir = os.path.dirname(os.path.abspath(__file__))
json_path = os.path.join(base_dir, 'overall_trends.json')

# Load data
with open(json_path, 'r') as f:
    data = json.load(f)

labels = data['labels']
positive = data['positive']
neutral = data['neutral']
negative = data['negative']

# Create smooth, filled area traces with rounded markers
trace_pos = go.Scatter(
    x=labels, y=positive, mode='lines+markers', name='Positive',
    line=dict(color='#27ae60', width=4, shape='spline'),
    marker=dict(size=8, color='#27ae60', line=dict(width=2, color='white')),
    fill='tozeroy', fillcolor='rgba(39, 174, 96, 0.08)'
)
trace_neu = go.Scatter(
    x=labels, y=neutral, mode='lines+markers', name='Neutral',
    line=dict(color='#f39c12', width=4, shape='spline'),
    marker=dict(size=8, color='#f39c12', line=dict(width=2, color='white')),
    fill='tozeroy', fillcolor='rgba(243, 156, 18, 0.08)'
)
trace_neg = go.Scatter(
    x=labels, y=negative, mode='lines+markers', name='Negative',
    line=dict(color='#e74c3c', width=4, shape='spline'),
    marker=dict(size=8, color='#e74c3c', line=dict(width=2, color='white')),
    fill='tozeroy', fillcolor='rgba(231, 76, 60, 0.08)'
)

layout = go.Layout(
    title='',
    xaxis=dict(title='', tickangle=-30, showgrid=True, gridcolor='rgba(0,0,0,0.04)', tickfont=dict(size=14)),
    yaxis=dict(title='', range=[0, 100], showgrid=True, gridcolor='rgba(0,0,0,0.04)', tickfont=dict(size=14)),
    legend=dict(x=0.98, y=0.02, xanchor='right', yanchor='bottom', orientation='h', font=dict(size=16)),
    hovermode='x unified',
    template='plotly_white',
    font=dict(family='Inter, Arial, sans-serif', size=18, color='#34495e'),
    margin=dict(l=40, r=40, t=40, b=100),
    autosize=True,
    height=500
)

fig = go.Figure(data=[trace_pos, trace_neu, trace_neg], layout=layout)

# Show the interactive chart in a new browser tab
fig.show() 