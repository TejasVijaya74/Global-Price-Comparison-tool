import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np

# Create the architecture diagram data
components_data = {
    'Component': [
        'FastAPI App', 'REST Endpoints', 'Request/Response',
        'Scraping Engine', 'Product Matcher', 'Rate Limiter', 'Background Tasks',
        'MySQL Database', 'Redis Cache', 'File Storage',
        'E-commerce Sites', 'Countries', 'Docker', 'Vercel', 'Heroku'
    ],
    'Layer': [
        'API', 'API', 'API',
        'Services', 'Services', 'Services', 'Services', 
        'Data', 'Data', 'Data',
        'External', 'External', 'Deployment', 'Deployment', 'Deployment'
    ],
    'X_Position': [
        2, 1, 3,  # API layer
        1, 2, 3, 4,  # Services layer
        1, 2, 3,  # Data layer
        0, 5, 1, 2, 3  # External and Deployment
    ],
    'Y_Position': [
        4, 4, 4,  # API layer at top
        3, 3, 3, 3,  # Services layer in middle
        2, 2, 2,  # Data layer
        3, 3, 1, 1, 1  # External (sides) and Deployment (bottom)
    ],
    'Size': [
        30, 25, 25,  # API
        28, 28, 28, 28,  # Services
        30, 30, 25,  # Data
        25, 20, 20, 20, 20  # External and Deployment
    ]
}

df = pd.DataFrame(components_data)

# Define colors for each layer using the brand colors
layer_colors = {
    'API': '#1FB8CD',      # Strong cyan
    'Services': '#FFC185',  # Light orange
    'Data': '#ECEBD5',     # Light green
    'External': '#5D878F',  # Cyan
    'Deployment': '#D2BA4C' # Moderate yellow
}

# Create the figure
fig = go.Figure()

# Add components for each layer
for layer in ['API', 'Services', 'Data', 'External', 'Deployment']:
    layer_data = df[df['Layer'] == layer]
    
    fig.add_trace(go.Scatter(
        x=layer_data['X_Position'],
        y=layer_data['Y_Position'],
        mode='markers+text',
        marker=dict(
            size=layer_data['Size'],
            color=layer_colors[layer],
            symbol='square',
            line=dict(width=2, color='white')
        ),
        text=layer_data['Component'],
        textposition='middle center',
        textfont=dict(size=10, color='black'),
        name=layer,
        showlegend=True,
        cliponaxis=False
    ))

# Add connecting arrows using shapes (simplified flow)
arrows = [
    # API to Services
    {'x0': 2, 'y0': 3.7, 'x1': 2, 'y1': 3.3},
    # Services to Data
    {'x0': 2, 'y0': 2.7, 'x1': 2, 'y1': 2.3},
    # External to Services
    {'x0': 0.3, 'y0': 3, 'x1': 0.7, 'y1': 3},
    # Services to External (right side)
    {'x0': 4.3, 'y0': 3, 'x1': 4.7, 'y1': 3},
    # Data to Deployment
    {'x0': 2, 'y0': 1.7, 'x1': 2, 'y1': 1.3}
]

for arrow in arrows:
    fig.add_annotation(
        x=arrow['x1'], y=arrow['y1'],
        ax=arrow['x0'], ay=arrow['y0'],
        xref='x', yref='y',
        axref='x', ayref='y',
        showarrow=True,
        arrowhead=2,
        arrowsize=1,
        arrowwidth=2,
        arrowcolor='gray',
        opacity=0.6
    )

# Update layout
fig.update_layout(
    title='Price Comparison System Architecture',
    xaxis=dict(
        showgrid=False,
        showticklabels=False,
        zeroline=False,
        range=[-0.5, 5.5]
    ),
    yaxis=dict(
        showgrid=False,
        showticklabels=False,
        zeroline=False,
        range=[0.5, 4.5]
    ),
    legend=dict(
        orientation='h',
        yanchor='bottom',
        y=1.05,
        xanchor='center',
        x=0.5
    ),
    plot_bgcolor='white',
    paper_bgcolor='white',
    font=dict(family='Arial', size=12)
)

# Save the chart
fig.write_image('system_architecture.png', width=1200, height=800, scale=2)
fig.show()