import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import pandas as pd
import numpy as np

def set_default_style():
    plt.rcParams['font.size'] = 12
    plt.rcParams['axes.titlesize'] = 14
    plt.rcParams['axes.labelsize'] = 12
    plt.rcParams['xtick.labelsize'] = 10
    plt.rcParams['ytick.labelsize'] = 10
    plt.rcParams['lines.color'] = 'blue'
    plt.rcParams['axes.facecolor'] = 'white'

def create_matplotlib_line_graph(data, title='Line Graph', xlabel='X-axis', ylabel='Y-axis', columns=None):
    """Creates a line graph using Matplotlib."""
    set_default_style()
    if columns is None:
        columns = [data.columns[0]]  # Default to the first column if none provided
    for col in columns:
        plt.plot(data[col], label=col)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.legend()
    plt.show()

def create_seaborn_box_plot(data, title='Box Plot', columns=None):
    """Creates a box plot using Seaborn."""
    set_default_style()
    if columns is None:
        columns = [data.columns[0]]  # Default to the first column if none provided
    sns.boxplot(data=data[columns])
    plt.title(title)
    plt.show()

def create_plotly_scatter_plot(data, x_col, y_col, title='Scatter Plot'):
    """Creates an interactive scatter plot using Plotly."""
    fig = px.scatter(data, x=x_col, y=y_col, title=title)
    fig.show()

def create_plotly_bar_chart(data, x_col, y_col, title='Bar Chart'):
    """Creates an interactive bar chart using Plotly."""
    fig = px.bar(data, x=x_col, y=y_col, title=title)
    fig.show()

def create_histogram(data, column, title='Histogram', xlabel='Values', ylabel='Frequency'):
    """Creates a histogram using Matplotlib."""
    set_default_style()
    plt.hist(data[column], bins=30, alpha=0.7, label=column)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.legend()
    plt.show()

def create_heatmap(data, title='Heatmap'):
    """Creates a heatmap of the correlation matrix using Seaborn."""
    set_default_style()
    correlation_matrix = data.corr()
    sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt=".2f")
    plt.title(title)
    plt.show()

def create_pie_chart(data, column, title='Pie Chart'):
    """Creates a pie chart using Matplotlib."""
    set_default_style()
    counts = data[column].value_counts()
    plt.pie(counts, labels=counts.index, autopct='%1.1f%%', startangle=90)
    plt.title(title)
    plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    plt.show()

def create_violin_plot(data, columns, category, title='Violin Plot'):
    """Creates a violin plot using Seaborn."""
    set_default_style()
    for column in columns:
        sns.violinplot(x=category, y=column, data=data)
        plt.title(f'{title} - {column}')
        plt.show()

def create_time_series_plot(data, time_col, value_cols, title='Time Series Plot'):
    """Creates a time series plot using Matplotlib."""
    set_default_style()
    for value_col in value_cols:
        plt.plot(data[time_col], data[value_col], label=value_col)
    plt.title(title)
    plt.xlabel('Time')
    plt.ylabel('Values')
    plt.legend()
    plt.show()

def create_stacked_bar_chart(data, x_col, y_cols, title='Stacked Bar Chart'):
    """Creates a stacked bar chart using Matplotlib."""
    set_default_style()
    data.plot(kind='bar', stacked=True, x=x_col, y=y_cols)
    plt.title(title)
    plt.xlabel(x_col)
    plt.ylabel('Values')
    plt.show()

def create_bubble_chart(data, x_col, y_col, size_col, title='Bubble Chart'):
    """Creates a bubble chart using Matplotlib."""
    set_default_style()
    plt.scatter(data[x_col], data[y_col], s=data[size_col]*10, alpha=0.5)
    plt.title(title)
    plt.xlabel(x_col)
    plt.ylabel(y_col)
    plt.show()

def create_radar_chart(data, categories, title='Radar Chart'):
    """Creates a radar chart (spider chart) using Matplotlib."""
    set_default_style()
    angles = np.linspace(0, 2 * np.pi, len(categories), endpoint=False).tolist()
    data = data.append(data.iloc[0])  # Close the circle
    angles += angles[:1]
    
    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))
    ax.fill(angles, data, color='blue', alpha=0.25)
    ax.set_yticklabels([])
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(categories)
    plt.title(title)
    plt.show()

def create_annotated_heatmap(data, title='Annotated Heatmap'):
    """Creates an annotated heatmap using Seaborn."""
    set_default_style()
    plt.figure(figsize=(10, 8))
    sns.heatmap(data, annot=True, fmt=".2f", cmap='coolwarm')
    plt.title(title)
    plt.show()

def create_cdf_plot(data, column, title='CDF Plot'):
    """Creates a cumulative distribution function (CDF) plot."""
    sorted_data = np.sort(data[column])
    y = np.arange(1, len(sorted_data) + 1) / len(sorted_data)
    plt.plot(sorted_data, y)
    plt.title(title)
    plt.xlabel(column)
    plt.ylabel('CDF')
    plt.grid()
    plt.show()

def create_pair_plot(data, title='Pair Plot'):
    """Creates a pair plot using Seaborn."""
    set_default_style()
    sns.pairplot(data)
    plt.suptitle(title, y=1.02)
    plt.show()

def create_multi_time_series_plot(data, time_col, value_cols, category_col, title='Multi Time Series Plot'):
    """Creates a multi time series plot using Matplotlib."""
    set_default_style()
    for category in data[category_col].unique():
        subset = data[data[category_col] == category]
        for value_col in value_cols:
            plt.plot(subset[time_col], subset[value_col], label=f'{category} - {value_col}')
    plt.title(title)
    plt.xlabel('Time')
    plt.ylabel('Values')
    plt.legend()
    plt.show()


