def filter_by_energy(df, energy_type):

    energy_map = {
        "diesel": "gazole",
        "gasoline": "essence",
        "electric": "elec",
    }

    energy_type = energy_type.lower()

    # conversion utilisateur -> dataset
    energy_type = energy_map.get(energy_type, energy_type)

    return df[df["energy"].str.lower().str.contains(energy_type)]