def filter_by_energy(df, energy_type):

    return df[df["energy"].str.lower() == energy_type.lower()]