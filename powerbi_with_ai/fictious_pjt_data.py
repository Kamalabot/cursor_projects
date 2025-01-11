import numpy as np
import pandas as pd

# Generating fictitious data
num_rows = 30  # Define the number of fictitious rows

fictitious_data = {
    "S.No": range(1, num_rows + 1),
    "Customer": np.random.choice(
        ["Renault", "TML", "Hyundai", "Ford", "Mahindra"], num_rows
    ),
    "Program": np.random.choice(
        ["BBG D2C", "Intra V30", "X1324/1312", "SUV-X", "Sedan-Y"], num_rows
    ),
    "Product": np.random.choice(["R&P", "Axle", "Transmission", "Chassis"], num_rows),
    "Plant": np.random.choice([2, 3, 4, 5], num_rows),
    "APQP ID": [f"SGP-24-{str(i).zfill(3)}" for i in range(1, num_rows + 1)],
    "Kick off Date": pd.date_range(
        start="2024-01-01", periods=num_rows, freq="7D"
    ).strftime("%d.%m.%y"),
    "Proto Sample Reqmt": np.random.choice(
        ["-", "15.02.24", "12.03.24", "Pending"], num_rows
    ),
    "OTOP Reqmt P/A": np.random.choice(
        ["07.06.24", "30.08.24", "15.09.24", "-"], num_rows
    ),
    "Child Parts MRD(gate2)": pd.date_range(
        start="2024-03-01", periods=num_rows, freq="10D"
    ).strftime("%d.%m.%y"),
    "OTOP Drg(gate3)": pd.date_range(
        start="2024-04-01", periods=num_rows, freq="12D"
    ).strftime("%d.%m.%y"),
    "TFC Closure(gate3)": pd.date_range(
        start="2024-05-01", periods=num_rows, freq="14D"
    ).strftime("%d.%m.%y"),
    "Part no Availability in SAP(gate3)": pd.date_range(
        start="2024-06-01", periods=num_rows, freq="16D"
    ).strftime("%d.%m.%y"),
    "Child Parts MRD(gate3)": pd.date_range(
        start="2024-07-01", periods=num_rows, freq="18D"
    ).strftime("%d.%m.%y"),
    "Child Parts PPAP(gate3)": np.random.choice(
        ["TBC", "Approved", "Pending"], num_rows
    ),
    "BC Plan vs Actual(gate3)": np.random.choice(
        ["TBC", "On Track", "Delayed"], num_rows
    ),
    "Stock Norms(gate4)": pd.date_range(
        start="2024-08-01", periods=num_rows, freq="20D"
    ).strftime("%d.%m.%y"),
    "Capacity(gate4)": pd.date_range(
        start="2024-09-01", periods=num_rows, freq="22D"
    ).strftime("%d.%m.%y"),
    "Hand over to PMMD(gate5)": pd.date_range(
        start="2024-10-01", periods=num_rows, freq="24D"
    ).strftime("%d.%m.%y"),
}

df_fictitious = pd.DataFrame(fictitious_data)

# Save the generated data to an Excel file
file_path_fictitious = "Fictitious_GateDates.xlsx"
df_fictitious.to_excel(file_path_fictitious, index=False)
