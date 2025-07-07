#!/usr/bin/env python3
"""
Panel Material UI Plotly Dashboard

A comprehensive dashboard showcasing various Plotly chart types with
Material Design theming. Perfect for testing light/dark theme switching
and the enhanced colorscales implementation.

Run with: panel serve app.py --show --autoreload
"""

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import panel as pn
import panel_material_ui as pmui
from plotly.subplots import make_subplots

# Configure Panel
pn.extension('plotly')

primary_color = "#4099da"
primary_color_dark = "#644c76"

THEME_CONFIG = {
    "light": {
        "palette": {
            "primary": {
                "main": primary_color,
            },
        },
    },
    "dark": {
        "palette": {
            "primary": {
                "main": primary_color_dark,
            },
        }
    }
}

np.random.seed(42)

def create_sample_data():
    """Generate various sample datasets for different chart types."""

    # Basic data
    dates = pd.date_range('2024-01-01', periods=50, freq='D')
    categories = ['Product A', 'Product B', 'Product C', 'Product D', 'Product E']

    # Time series data
    time_series = pd.DataFrame({
        'date': dates,
        'sales': np.cumsum(np.random.randn(50)) + 100,
        'profit': np.cumsum(np.random.randn(50)) + 50,
        'customers': np.cumsum(np.random.randn(50)) + 200
    })

    # Categorical data
    categorical = pd.DataFrame({
        'category': categories,
        'value': np.random.randint(10, 100, 5),
        'value2': np.random.randint(5, 80, 5)
    })

    # Financial data
    stock_data = pd.DataFrame({
        'date': dates[:30],
        'open': 100 + np.cumsum(np.random.randn(30) * 0.5),
        'high': 100 + np.cumsum(np.random.randn(30) * 0.5) + 2,
        'low': 100 + np.cumsum(np.random.randn(30) * 0.5) - 2,
        'close': 100 + np.cumsum(np.random.randn(30) * 0.5),
        'volume': np.random.randint(1000, 10000, 30)
    })

    # 3D and heatmap data
    x = np.linspace(-2, 2, 20)
    y = np.linspace(-2, 2, 20)
    X, Y = np.meshgrid(x, y)
    Z = np.sin(X) * np.cos(Y)

    # Iris dataset for parallel coordinates
    iris = px.data.iris()

    return time_series, categorical, stock_data, X, Y, Z, iris

# Create datasets
time_series, categorical, stock_data, X, Y, Z, iris = create_sample_data()

def create_line_plot():
    """Create a line plot with multiple series."""
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=time_series['date'],
        y=time_series['sales'],
        mode='lines+markers',
        name='Sales',
        line=dict(width=3),
    ))

    fig.add_trace(go.Scatter(
        x=time_series['date'],
        y=time_series['profit'],
        mode='lines+markers',
        name='Profit',
        line=dict(width=3),
    ))

    fig.update_layout(
        title="📈 Sales & Profit Trends",
        xaxis_title="Date",
        yaxis_title="Amount ($)",
        hovermode='x unified',
    )

    return fig

def create_bar_chart():
    """Create a bar chart with grouped data."""
    fig = go.Figure()

    fig.add_trace(go.Bar(
        name='Current Year',
        x=categorical['category'],
        y=categorical['value'],
        text=categorical['value'],
        textposition='auto'
    ))

    fig.add_trace(go.Bar(
        name='Previous Year',
        x=categorical['category'],
        y=categorical['value2'],
        text=categorical['value2'],
        textposition='auto'
    ))

    fig.update_layout(
        title="📊 Product Performance Comparison",
        xaxis_title="Product Category",
        yaxis_title="Sales Volume",
        barmode='group'
    )

    return fig

def create_pie_chart():
    """Create a pie chart with Material Design colors."""
    fig = go.Figure(data=[go.Pie(
        labels=categorical['category'],
        values=categorical['value'],
        hole=0.3,
        textinfo='label+percent',
        textposition='outside'
    )])

    fig.update_layout(
        title="🥧 Market Share Distribution",
        showlegend=True
    )

    return fig

def create_heatmap():
    """Create a heatmap with enhanced Material Design colorscale."""
    fig = go.Figure(data=go.Heatmap(
        z=Z,
        x=np.linspace(-2, 2, 20),
        y=np.linspace(-2, 2, 20),
        colorbar=dict(title="Intensity")
    ))

    fig.update_layout(
        title="🔥 Heat Map with Material Design Colors",
        xaxis_title="X Coordinate",
        yaxis_title="Y Coordinate"
    )

    return fig

def create_surface_plot():
    """Create a 3D surface plot."""
    fig = go.Figure(data=[go.Surface(
        z=Z,
        x=np.linspace(-2, 2, 20),
        y=np.linspace(-2, 2, 20),
        colorbar=dict(title="Height")
    )])

    fig.update_layout(
        title="🏔️ 3D Surface Plot",
        scene=dict(
            xaxis_title="X",
            yaxis_title="Y",
            zaxis_title="Z"
        )
    )

    return fig

def create_candlestick():
    """Create a candlestick chart for financial data."""
    fig = go.Figure(data=[go.Candlestick(
        x=stock_data['date'],
        open=stock_data['open'],
        high=stock_data['high'],
        low=stock_data['low'],
        close=stock_data['close'],
        name="Stock Price"
    )])

    fig.update_layout(
        title="💹 Stock Price Candlestick Chart",
        xaxis_title="Date",
        yaxis_title="Price ($)",
        xaxis_rangeslider_visible=False
    )

    return fig

def create_scatter_3d():
    """Create a 3D scatter plot."""
    fig = go.Figure(data=[go.Scatter3d(
        x=iris['sepal_length'],
        y=iris['sepal_width'],
        z=iris['petal_length'],
        mode='markers',
        marker=dict(
            size=8,
            color=iris['petal_width'],
            colorscale='Viridis',
            showscale=True,
            colorbar=dict(title="Petal Width")
        ),
        text=iris['species'],
        hovertemplate='<b>%{text}</b><br>' +
                      'Sepal Length: %{x}<br>' +
                      'Sepal Width: %{y}<br>' +
                      'Petal Length: %{z}<extra></extra>'
    )])

    fig.update_layout(
        title="🌸 3D Iris Dataset Visualization",
        scene=dict(
            xaxis_title="Sepal Length",
            yaxis_title="Sepal Width",
            zaxis_title="Petal Length"
        )
    )

    return fig

def create_parallel_coordinates():
    """Create a parallel coordinates plot."""
    fig = go.Figure(data=go.Parcoords(
        line=dict(color=iris['petal_width'], showscale=True),
        dimensions=list([
            dict(range=[4, 8], label="Sepal Length", values=iris['sepal_length']),
            dict(range=[2, 4.5], label="Sepal Width", values=iris['sepal_width']),
            dict(range=[1, 7], label="Petal Length", values=iris['petal_length']),
            dict(range=[0, 2.5], label="Petal Width", values=iris['petal_width'])
        ])
    ))

    fig.update_layout(
        title="📊 Parallel Coordinates - Iris Dataset"
    )

    return fig

def create_contour_plot():
    """Create a contour plot."""
    fig = go.Figure(data=go.Contour(
        z=Z,
        x=np.linspace(-2, 2, 20),
        y=np.linspace(-2, 2, 20),
        colorbar=dict(title="Value"),
        contours=dict(
            showlabels=True,
            labelfont=dict(size=12, color='white')
        )
    ))

    fig.update_layout(
        title="🗺️ Contour Plot with Material Design Colors",
        xaxis_title="X Coordinate",
        yaxis_title="Y Coordinate"
    )

    return fig

def create_box_plot():
    """Create a box plot."""
    fig = go.Figure()

    for species in iris['species'].unique():
        fig.add_trace(go.Box(
            y=iris[iris['species'] == species]['sepal_length'],
            name=species,
            boxpoints='outliers'
        ))

    fig.update_layout(
        title="📦 Box Plot - Sepal Length by Species",
        yaxis_title="Sepal Length",
        xaxis_title="Species"
    )

    return fig

def create_histogram():
    """Create a histogram with overlaid distributions."""
    fig = go.Figure()

    for species in iris['species'].unique():
        fig.add_trace(go.Histogram(
            x=iris[iris['species'] == species]['petal_length'],
            name=species,
            opacity=0.7,
            nbinsx=15
        ))

    fig.update_layout(
        title="📊 Histogram - Petal Length Distribution",
        xaxis_title="Petal Length",
        yaxis_title="Frequency",
        barmode='overlay'
    )

    return fig

def create_sunburst():
    """Create a sunburst chart."""
    # Create hierarchical data
    df = pd.DataFrame({
        'ids': ['A', 'B', 'C', 'A1', 'A2', 'B1', 'B2', 'C1'],
        'labels': ['Category A', 'Category B', 'Category C',
                   'Sub A1', 'Sub A2', 'Sub B1', 'Sub B2', 'Sub C1'],
        'parents': ['', '', '', 'A', 'A', 'B', 'B', 'C'],
        'values': [40, 30, 30, 15, 25, 20, 10, 30]
    })

    fig = go.Figure(go.Sunburst(
        ids=df['ids'],
        labels=df['labels'],
        parents=df['parents'],
        values=df['values'],
        branchvalues="total"
    ))

    fig.update_layout(
        title="☀️ Sunburst Chart - Hierarchical Data",
        font_size=12
    )

    return fig

# Create the main dashboard function
def create_dashboard():
    """Create the main dashboard with Page component."""

    # Create title and description
    title = pmui.Typography("🎨 Panel Material UI Plotly Dashboard", variant="h3", sx={"mb": 2})
    description = pmui.Typography(
        "A comprehensive showcase of Plotly charts with Material Design theming. "
        "Toggle between light and dark themes using the theme switcher in the header.",
        variant="body1",
        sx={"mb": 3, "color": "text.secondary"}
    )

    updated_plots = [
        create_line_plot(),
        create_bar_chart(),
        create_pie_chart(),
        create_heatmap(),
        create_surface_plot(),
        create_candlestick(),
        create_scatter_3d(),
        create_parallel_coordinates(),
        create_contour_plot(),
        create_box_plot(),
        create_histogram(),
        create_sunburst()
    ]

    # Create grid layout with plots
    plot_cards = []
    for i, plot in enumerate(updated_plots):
        card = pmui.Card(
            pn.pane.Plotly(plot, sizing_mode='stretch_width', height=400),
            sx={"mb": 2}
        )
        plot_cards.append(card)

    # Arrange plots in a responsive grid
    container = pmui.Container(*[
        pmui.Grid(*[
            pmui.Grid(card, size={'xs': 12, 'md': 6, 'lg': 6}) for card in plot_cards
        ], container=True, spacing=2, sx={"mb": 3}),
    ])

    page = pmui.Page(
        title="Plotly Dashboard - Panel Material UI",
        theme_toggle=True,
        sx={
            "& .main": {
                "padding": "24px"
            },
            "& .sidebar": {
                "padding": "24px"
            }
        },
        theme_config=THEME_CONFIG,
    )

    page.main = [
        title,
        description,
        container
    ]

    return page

if pn.state.served:
    dashboard = create_dashboard()
    dashboard.servable()
