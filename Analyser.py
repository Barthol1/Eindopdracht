from numpy import int32
import pandas as pd

class NumericalAnalyser:
    csv: pd.DataFrame
    def __init__(self, csv):
        self.csv = csv

    def cartAmount(self):
        return self.csv["NumberOfKarts"].sum()
    def getUniqueDrivers(self):
        return self.csv["DriverName"].nunique()
    def getDrivenHeats(self):
        min = self.csv["HeatNumber"].min()
        max = self.csv["HeatNumber"].max()
        return int(max) - int(min)
    def getFastestDriverByTime(self):
        sorted = self.csv
        sorted = sorted.sort_values(by=["Laptime"], ascending=True)
        sorted = sorted.drop_duplicates(subset=["DriverName"])
        sorted = sorted.head(10)
        return sorted
    def getFastestDriverByHeat(self):
        fastest_heat_times = self.csv.groupby('HeatNumber').agg({'Laptime': 'min'})
        fastest_heat_times = fastest_heat_times.reset_index()
        fastest_heat_times.sort_values('Laptime', inplace=True)
        fastest_heat_times = fastest_heat_times.head(10)
        return fastest_heat_times
    