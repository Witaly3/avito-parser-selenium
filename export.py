import pandas as pd
import sqlite3


def exporting():
    conn = sqlite3.connect("realty.db")
    df = pd.read_sql("select * from offers", conn)
    df.to_excel(r"result.xlsx", index=False)


if __name__ == "__main__":
    exporting()
