import pandas as pd
from typing import List, Tuple



def _get_degree_data_from_row(row: pd.Series, cols_prefix: str) -> Tuple[List[int], List[float]]:
    if cols_prefix.endswith('_'):
        relevant_cols = [col for col in row.index if col.startswith(cols_prefix) and pd.notna(row[col])]
    else:
        relevant_cols = [col for col in row.index if col.startswith(cols_prefix)
                         and not col.startswith(f'{cols_prefix}in_')
                         and not col.startswith(f'{cols_prefix}out_')
                         and pd.notna(row[col])]

    degrees_dict = {}
    for col in relevant_cols:
        try:
            degree = int(col.split('_')[-1])
            degrees_dict[degree] = row[col]
        except ValueError:
            pass

    sorted_degrees = sorted(degrees_dict.items())
    return [d[0] for d in sorted_degrees], [d[1] for d in sorted_degrees]
