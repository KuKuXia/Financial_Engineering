import os
import pandas as pd
import matplotlib.pyplot as plt


def symbol_to_path(symbol, base_dir='Data'):
    """Return CSV file path given ticker symbol."""
    return os.path.join(base_dir, "{}.csv".format(str(symbol)))


def get_data(symbols, dates):
    """Read stock data (adjusted close) for given symbols from CSV files."""
    df = pd.DataFrame(index=dates)
    if 'SPY' not in symbols:  # add SPY for reference. if absent
        symbols.insert(0, 'SPY')

    for symbol in symbols:
        df_temp = pd.read_csv(symbol_to_path(symbol), index_col='Date', parse_dates=True, usecols=['Date', 'Close'],
                              na_values=['nan'])
        df_temp = df_temp.rename(columns={'Close': symbol})
        df = df.join(df_temp)
        if symbol == 'SPY':
            df = df.dropna(subset=['SPY'])
    return df


def plot_data(df, title="Stock Prices", x_label="Date", y_label="Price"):
    """Plot stock prices with a custom title and meaningful axis labels."""
    ax = df.plot(title=title, fontsize=12)
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    plt.show()


def plot_selected(df, columns, start_index, end_index):
    """Plot the desired columns over index values in the given range."""
    # Note: DO NOT modify anything else!
    plot_data(df.loc[start_index:end_index, columns], title="Selected Data")


def normalize_data(df):
    return df / df.iloc[0, :]


def compute_daily_returns(df):
    """Compute and return the daily return values."""
    # Note: Returned DataFrame must have the same number of rows
    # Method 1
    dr = df.copy()
    daily_return_1 = (dr[1:] / df[:-1].values) - 1

    # Method 2
    daily_return_2 = (df / df.shift(1)) - 1

    # Assign the first row to 0
    daily_return_2.iloc[0, :] = 0
    return daily_return_2


def compute_cumulative_returns(df):
    """Compute and return the daily return values."""
    # Note: Returned DataFrame must have the same number of rows
    # Method 1
    print(df.iloc[0, :])
    cumulative_return = (df[:] / df.iloc[0, :].values) - 1
    return cumulative_return


# Bollinger Bands
def get_rolling_mean(values, window):
    """Return rolling mean of given values, using specified window size."""
    return values.rolling(window=window).mean()


def get_rolling_std(values, window):
    """Return rolling standard deviation of given values, using specified window size."""
    return values.rolling(window=20).std()


def get_bollinger_bands(rm, rstd):
    """Return upper and lower Bollinger Bands."""
    upper_band = rm + rstd * 2
    lower_band = rm - rstd * 2
    return upper_band, lower_band


def fill_missing_values(df_data):
    """Fill missing values in data frame, in place."""
    ##########################################################
    df_data.fillna(method="ffill", inplace=True)
    df_data.fillna(method="bfill", inplace=True)
