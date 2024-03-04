import seaborn as sns
from matplotlib import pyplot as plt
import matplotlib as mpl
import pandas as pd
from tools.tools import (
    version,
    maxchannels,
    sample_id,
    vialnumber,
    Volume,
    time,
    sampling_rate,
    TotalDataPoints,
    units,
    multiplier_units,
    DF_DATA_POINTS,
    DF_TIME,
    DF_CHANNEL,
)


def plot_images(
        titles_of_image: str | list[str, ...],
        infos: None | dict | list[dict, ...] | None,
        dfs: pd.DataFrame | list[pd.DataFrame, ...] | None,
        channels_to_plot: int | list[int, ...] | None,
        names_of_channels: list[list[str | int, ...], ...] | list[str, ...] | None,
        plotting_dict: dict | None,
):
    if plotting_dict is None:
        # Convert to lists if no dict
        if not isinstance(titles_of_image, list):
            titles_of_image = [titles_of_image]

        if not isinstance(channels_to_plot[0], list):
            channels_to_plot = [channels_to_plot]
        if not isinstance(infos, list):
            infos = [infos]
        if not isinstance(dfs, list):
            dfs = [dfs]
        if not isinstance(names_of_channels[0], list):
            names_of_channels = [names_of_channels]
        plotting_dict = {}
        for title, names, df, info, channels in zip(titles_of_image, names_of_channels, dfs, infos, channels_to_plot):
            plotting_dict[title] = [names, df, info, channels]

    for name, (names, df, infos, channels) in plotting_dict.items():
        spacing = 1
        print(channels)
        while spacing ** 2 < len(channels):
            spacing += 1
        fig, ax = plt.subplots(spacing, spacing, sharex='all')
        sns.despine(fig)
        try:
            _ = ax[0]
            ax = ax.flatten()
        except TypeError:
            ax = [ax]

        for i, (n, channel) in enumerate(zip(names, channels)):
            print(i, n, channel)
            sns.lineplot(
                data=df.loc[df[DF_CHANNEL] == channel],
                x=DF_TIME,
                y=DF_DATA_POINTS,
                # hue=df_channel,
                ax=ax[i],
            )
            ax[i].set_title(n)
        plt.show()
        plt.close()
