import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.patches as mpatches
from matplotlib.lines import Line2D
def graph(data_csv='data//processed_data.csv'):
    df = pd.read_csv(data_csv)
    df['Date'] = pd.to_datetime(df['Date'])
    df = df.sort_values('Date')

    df['PR_30d_avg'] = df['PR'].rolling(window=30).mean()

    start_date = pd.to_datetime("2019-07-01")
    df['budget_pr'] = 73.9  # initial
    for i in range(1, 10):  # up to 10 years if needed
        drop_date = start_date + pd.DateOffset(years=i)
        df.loc[df['Date'] >= drop_date, 'budget_pr'] = 73.9 * (0.992 ** i)

    df['above_budget'] = df['PR'] > df['budget_pr']
    num_above = df['above_budget'].sum()
    total_points = len(df)

    def get_color(ghi):
        if ghi < 2:
            return 'navy'
        elif ghi < 4:
            return 'lightblue'
        elif ghi < 6:
            return 'orange'
        else:
            return 'brown'
    df['color'] = df['GHI'].apply(get_color)

    fig, ax = plt.subplots(figsize=(15, 9))

    ax.scatter(df['Date'], df['PR'], c=df['color'], s=10, label='PR')

    ax.plot(df['Date'], df['PR_30d_avg'], color='red', label='30-d moving average of PR', linewidth=2)

    ax.plot(df['Date'], df['budget_pr'], color='darkgreen', label='Target Budget Yield Performance Ratio', linewidth=2)

    ax.set_title("Performance Ratio Evolution\nFrom {} to {}".format(df['Date'].min().date(), df['Date'].max().date()), fontsize=16)
    ax.set_xlabel("")
    ax.set_ylabel("Performance Ratio [%]", fontsize=12)
    ax.grid(True)

    legend_patches = [
        mpatches.Patch(color='navy', label='< 2'),
        mpatches.Patch(color='lightblue', label='2 - 4'),
        mpatches.Patch(color='orange', label='4 - 6'),
        mpatches.Patch(color='brown', label='> 6'),
    ]
    custom_lines = [
    Line2D([0], [0], color='darkgreen', lw=2, label='Target Budget Yield Performance Ratio'),
    Line2D([0], [0], color='red', lw=2, label='30-d moving average of PR')
    ]

    legend_elements = legend_patches + custom_lines
    ax.legend(handles=legend_elements, loc='upper left')

    right_text = ""
    for days in [7, 30, 60, 90, 365]:
        recent_avg = df.tail(days)['PR'].mean()
        right_text += f"Average PR last {days}-d: {recent_avg:.1f} %\n"
    lifetime_avg = df['PR'].mean()
    right_text += f"\nAverage PR Lifetime: {lifetime_avg:.1f} %"

    ax.text(df['Date'].max(), 25, right_text, ha='right', fontsize=10)

    ax.text(df['Date'].min(), 25, f"Points above Target Budget PR = {num_above}/{total_points} = {100*num_above/total_points:.1f}%", fontsize=12)

    ax.xaxis.set_major_locator(mdates.MonthLocator(interval=3))
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%b\n%y'))

    plt.tight_layout()
    plt.show()


graph()