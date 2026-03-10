import numpy as np
import matplotlib.pyplot as plt


def radar_chart(df):

    # critères
    features = [
        "vehicle_price_eur",
        "co2_mixed_g_km",
        "fuel_consumption_l_100km",
        "max_power_kw",
    ]

    labels = ["Price", "CO2", "Consumption", "Power"]

    # normalisation
    data = df[features]
    data = data / data.max()

    angles = np.linspace(0, 2 * np.pi, len(features), endpoint=False)
    angles = np.concatenate([angles, [angles[0]]])

    fig, ax = plt.subplots(subplot_kw={"polar": True})

    for i, row in data.iterrows():

        values = row.values
        values = np.concatenate([values, [values[0]]])

        ax.plot(angles, values, label=df.loc[i, "model"])
        ax.fill(angles, values, alpha=0.1)

    ax.set_thetagrids(angles[:-1] * 180 / np.pi, labels)

    plt.legend(loc="upper right")
    plt.title("Vehicle comparison radar")

    plt.show()