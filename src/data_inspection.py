import pandas as pd


DATA_PATH = "data/raw"


def inspect_dataset(file_name):
    file_path = f"{DATA_PATH}/{file_name}"

    print(f"\n{'=' * 60}")
    print(f"FILE: {file_name}")
    print(f"{'=' * 60}")

    df = pd.read_csv(file_path, nrows=1000)

    print(f"Sample rows: {len(df)}")
    print(f"Total columns: {len(df.columns)}")
    print("\nColumns:")
    print(df.columns.tolist())

    print("\nMissing values:")
    print(df.isnull().sum().sort_values(ascending=False).head(10))

    print("\nData types:")
    print(df.dtypes)

    print("\nFirst 5 rows:")
    print(df.head())


def main():
    inspect_dataset("sales_train_validation.csv")
    inspect_dataset("calendar.csv")
    inspect_dataset("sell_prices.csv")


if __name__ == "__main__":
    main()