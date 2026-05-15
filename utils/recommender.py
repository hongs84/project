import pandas as pd
from utils.scoring import calculate_score

def recommend_schools(student_data, schools_df):
    schools_df["score"] = schools_df.apply(
        lambda row: calculate_score(student_data, row), axis=1
    )

    return schools_df.sort_values(by="score", ascending=False).head(3)