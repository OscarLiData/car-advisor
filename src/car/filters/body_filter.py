def filter_by_body(df, body_type):

    return df[df["body_type"].str.lower() == body_type.lower()]