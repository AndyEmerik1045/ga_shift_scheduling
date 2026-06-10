import pandas as pd

def simpan_history_generasi(history, path):
    df = pd.DataFrame(history)
    df.to_csv(path, index=False)