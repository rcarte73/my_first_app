import plotly
import plotly.graph_objects as go
import plotly.subplots

default_layout = dict(
    title=dict(
        font=dict(
            size=20,  # Font size of title
            color="black",  # Font color of title
            family="Arial",  # Font family of title
        ),
        x=0.5,  # Center the title
    ),
    xaxis=dict(
        showline=True,  # Show X-axis line
        mirror=True,
        linecolor="black",  # Color of X-axis line
        linewidth=2,
        ticks="outside",  # Show ticks outside the plot on the X-axis
        ticklen=10,  # Length of X-axis ticks
        tickwidth=2,  # Width of X-axis ticks
        tickcolor="black",  # Color of X-axis ticks
        title_font=dict(size=20),
        tickfont=dict(size=20),
        gridcolor="lightgray",  # Set grid color to a faint color
        gridwidth=0.5,  # Set grid line width to a thin value
        showspikes=True,  # Enable vertical spikeline
        spikemode="across",  # Show spike line across all subplots/traces
        spikesnap="cursor",  # Snap spike to cursor position
    ),
    yaxis=dict(
        showline=True,  # Show X-axis line
        mirror=True,
        linecolor="black",  # Color of X-axis line
        linewidth=2,
        ticks="outside",  # Show ticks outside the plot on the X-axis
        ticklen=10,  # Length of X-axis ticks
        tickwidth=2,  # Width of X-axis ticks
        tickcolor="black",  # Color of X-axis ticks
        title_font=dict(size=20),
        tickfont=dict(size=20),
        gridcolor="lightgray",  # Set grid color to a faint color
        gridwidth=0.5,  # Set grid line width to a thin value
    ),
    yaxis2=dict(  # Y-axis for the error bar subplot
        title_font=dict(size=20, family="Arial"),
        showline=True,
        linecolor="black",
        linewidth=2,
        mirror=True,
        ticks="outside",
        tickfont=dict(size=20),
        tickcolor="black",
        gridcolor="lightgray",  # Set grid color to a faint color
        gridwidth=0.5,
    ),
    legend=dict(
        font=dict(
            size=15,  # Font size of legend
            color="black",  # Font color of legend
            family="Arial",  # Font family of legend
        ),
    ),
    plot_bgcolor="rgba(0,0,0,0)",
    hovermode="x unified",  # Show one tooltip box for all traces at a given x
    spikedistance=-1,  # Always show spikes regardless of distance
)


class Figure(plotly.graph_objects.Figure):
    def __init__(
        self, data=None, layout={}, frames=None, skip_invalid=False, **kwargs
    ):
        layout.update(default_layout)
        super(Figure, self).__init__(
            data, layout, frames, skip_invalid, **kwargs
        )

    def add_plot(self, x=[], y=[], name=None):
        self.add_trace(go.Scatter(x=x, y=y, name=name))


def make_subplots(
    rows=1,
    cols=1,
    shared_xaxes=False,
    shared_yaxes=False,
    start_cell="top-left",
    print_grid=False,
    horizontal_spacing=None,
    vertical_spacing=None,
    subplot_titles=None,
    column_widths=None,
    row_heights=None,
    specs=None,
    insets=None,
    column_titles=None,
    row_titles=None,
    x_title=None,
    y_title=None,
    figure=None,
    **kwargs,
) -> go.Figure:
    """
    Makes a subplot with custom Figure object as input
    """
    figure = figure if figure else Figure()
    return plotly.subplots.make_subplots(
        rows=rows,
        cols=cols,
        shared_xaxes=shared_xaxes,
        shared_yaxes=shared_yaxes,
        start_cell=start_cell,
        print_grid=print_grid,
        horizontal_spacing=horizontal_spacing,
        vertical_spacing=vertical_spacing,
        subplot_titles=subplot_titles,
        column_widths=column_widths,
        row_heights=row_heights,
        specs=specs,
        insets=insets,
        column_titles=column_titles,
        row_titles=row_titles,
        x_title=x_title,
        y_title=y_title,
        figure=figure,
        **kwargs,
    )


def make_errorplot(
    xaxis_title="X-axis title",
    yaxis1_title="Y-axis title",
    yaxis2_title="Error",
):
    """
    Make error plot
    """
    # Create a subplot layout with 2 rows and shared x-axis
    fig = make_subplots(
        rows=2,
        cols=1,
        shared_xaxes=True,
        row_heights=[0.7, 0.3],  # Adjust relative heights
        vertical_spacing=0.03,  # Space between subplots
    )
    fig.update_layout(
        dict(
            xaxis=dict(
                showticklabels=False,
                ticks="",
            ),
            yaxis=dict(
                title=yaxis1_title,
                title_font=dict(size=20, family="Arial"),
            ),
            xaxis2=dict(  # X-axis for the bottom subplot (shared x-axis properties)
                title=xaxis_title,
                title_font=dict(size=20, family="Arial"),
                showline=True,
                linecolor="black",
                linewidth=2,
                mirror=True,
                ticks="outside",
                ticklen=10,
                tickwidth=2,
                tickfont=dict(size=20),
                tickcolor="black",
                gridcolor="lightgray",  # Set grid color to a faint color
                gridwidth=0.5,
            ),
            yaxis2=dict(  # Y-axis for the error bar subplot
                title=yaxis2_title,
                title_font=dict(size=20, family="Arial"),
                showline=True,
                linecolor="black",
                linewidth=2,
                mirror=True,
                ticks="outside",
                ticklen=10,
                tickwidth=2,
                tickfont=dict(size=20),
                tickcolor="black",
                gridcolor="lightgray",  # Set grid color to a faint color
                gridwidth=0.5,
            ),
        )
    )

    return fig
