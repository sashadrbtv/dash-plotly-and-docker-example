"""Chart helpers"""

import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import statsmodels.api as sm


def plot_time_series(df):
    """Plotting claims as time series with 6 month forecast """
    ts = df.groupby('MONTH', as_index=False)['PAID_AMOUNT'].sum()
    ts['MONTH'] = ts['MONTH'].astype(str)

    # Forecast
    periods = pd.to_datetime(df['MONTH'].unique(), format='%Y%m')
    projection = pd.date_range(
        start=periods[-1],
        end=periods[-1] + pd.DateOffset(months=6),
        freq='M') + pd.DateOffset(days=1)
    periods = periods.union(projection)

    real_size = ts.shape[0]
    adj_size = real_size - 1
    predict_size = real_size + 6  # add number of months for projection

    Y = ts.loc[:adj_size, 'PAID_AMOUNT'].tolist()
    X = list(range(1, adj_size + 2))
    X = sm.add_constant(X)
    model = sm.OLS(Y, X)
    results = model.fit()

    y_prediction = results.predict(
        np.column_stack((np.ones(predict_size), list(range(1, predict_size + 1)))))

    # Plot
    fig = go.Figure()
    fig.add_trace(go.Line(x=periods, y=ts['PAID_AMOUNT'].tolist(), name='total'))
    fig.add_trace(go.Line(x=periods, y=y_prediction, name='trend', line=dict(color='grey', dash='dash')))

    fig.update_layout(
        title='Total paid amount dynamics & projection',
        paper_bgcolor="white",
        plot_bgcolor="white",
        showlegend=True)

    return fig


def plot_stacked_area(df):
    """Plotting payers distribution in dynamics """

    payers_by_months = df.groupby(['PAYER', 'MONTH'], as_index=False)['PAID_AMOUNT'].sum()
    x_labels = pd.to_datetime(df['MONTH'].unique(), format='%Y%m').date
    y_labels = payers_by_months['PAYER'].unique().tolist()
    fig = go.Figure()

    for payer in y_labels:

        fig.add_trace(go.Scatter(
            x=x_labels,
            y=payers_by_months[payers_by_months['PAYER'] == payer].sort_values(by='MONTH')['PAID_AMOUNT'].tolist(),
            mode='lines',
            name=payer,
            stackgroup='one',
            groupnorm='percent'  # sets the normalization for the sum of the stack group
        ))

    fig.update_layout(
        title='Payers paid amount dynamics, %',
        paper_bgcolor="white",
        plot_bgcolor="white",
        showlegend=True,
        xaxis_type='category',
        yaxis=dict(
            type='linear',
            range=[1, 100],
            ticksuffix='%'))

    return fig


def plot_bar(df, last_year=2020, last_months=6):
    """Plotting top 10 CLAIM_SPECIALTY for last 2 years. """

    # preprocessing
    df_slice = df[
        (df['MONTH'].apply(lambda x: x.year) >= last_year - 1) &
        (df['MONTH'].apply(lambda x: x.month) <= last_months)]
    df_slice['YEAR'] = df['MONTH'].apply(lambda x: x.year).astype(int)

    top_10_in_last_year = df_slice.loc[df_slice['YEAR'] == last_year].groupby(
        ['CLAIM_SPECIALTY'], as_index=False)['PAID_AMOUNT'].sum().sort_values(by='PAID_AMOUNT', ascending=False)[:10]

    df_slice = df_slice.loc[
        df_slice['CLAIM_SPECIALTY'].isin(
            top_10_in_last_year['CLAIM_SPECIALTY'].tolist())].groupby(
        ['YEAR', 'CLAIM_SPECIALTY'], as_index=False)['PAID_AMOUNT'].sum().sort_values(by='PAID_AMOUNT', ascending=False)

    # fig
    fig = px.bar(df_slice, x='YEAR', y='PAID_AMOUNT',
                 hover_data=['PAID_AMOUNT'], color='CLAIM_SPECIALTY',
                 labels={'PAID_AMOUNT': 'PAID AMOUNT'}, text_auto=True)

    fig.update_layout(
        title=f'Top 10 claims specialties, {last_year} vs {last_year - 1} ({last_months} months only)',
        paper_bgcolor="white",
        plot_bgcolor="white",
        showlegend=True)

    return fig
