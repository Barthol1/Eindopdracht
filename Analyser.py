import matplotlib.pyplot as plot
from numpy import int32
import pandas as pd
from time import time

class NumericalAnalyser:
    csv: pd.DataFrame
    isVerbose = False
    def __init__(self, csv, isVerbose):
        print(isVerbose)
        self.csv = csv
        self.isVerbose = isVerbose
        print(self.isVerbose)

    def timer_func(func):
        def wrapper(*args, **kwargs):
            t1 = time()
            result = func(*args, **kwargs)
            t2 = time()
            timingstring = f'Function {func.__name__!r} executed in {(t2-t1):.4f}s \n' + str(result)
            return {"result": result, "time": timingstring}
        return wrapper

    @timer_func
    def cartAmount(self):
        return self.csv["NumberOfKarts"].sum()
    @timer_func
    def getUniqueDrivers(self):
        return self.csv["DriverName"].nunique()
    @timer_func
    def getDrivenHeats(self):
        min = self.csv["HeatNumber"].min()
        max = self.csv["HeatNumber"].max()
        return int(max) - int(min)
    @timer_func
    def getFastestDriverByTime(self):
        sorted = self.csv
        sorted = sorted.sort_values(by=["Laptime"], ascending=True)
        sorted = sorted.drop_duplicates(subset=["DriverName"])
        sorted = sorted.head(10)
        return sorted
    @timer_func
    def getFastestDriverByHeat(self):
        fastest_heat_times = self.csv.groupby('HeatNumber').agg({'Laptime': 'min'})
        fastest_heat_times = fastest_heat_times.reset_index()
        fastest_heat_times.sort_values('Laptime', inplace=True)
        fastest_heat_times = fastest_heat_times.head(10)
        return fastest_heat_times
    @timer_func
    def get_best_kart(self):
        # 1. Neem van een kart alle rondetijden
        # 2. Schrap  de rondetijden die boven de 42 seconden uitkomen en/of gereden zijn in een heat met meer dan 10 coureurs.
        filtered = (self.csv.sort_values(by=["Laptime"], ascending=True)
            .groupby('KartNumber')
            .apply(lambda x: x[(x['Laptime'] <= "00:42.000") | (x["NumberOfKarts"] <= 10)])
        ).reset_index(drop = True)

        filtered['Laptime'] = filtered['Laptime'].str.replace(':','').astype(float).apply(pd.to_numeric)

        # 3. Selecteer de 10% snelste rondetijden van filter
        filtered = filtered[filtered['Laptime'] <= filtered.groupby(['KartNumber'])['Laptime'].transform('quantile', 0.1)].reset_index(drop=True)
        
        # 4. Bereken gemiddelde van elke groep
        filtered["Mean"] = filtered['Laptime'].groupby(filtered['KartNumber']).transform('mean')

        # 5. Laagste gemiddelde van alle karts is de beste kart
        result = filtered[filtered["Mean"] == filtered["Mean"].min()]["KartNumber"].head(1).to_string(index=False)

        return (f'The best kart is kart: #{result}')

    @timer_func
    def getScatterPlot(self):
        filtered = self.csv
        plot.scatter(x=filtered['HeatNumber'], y=filtered['HeatNumber'])
        plot.title("Scatter plot between two variables X and Y")
        plot.show()
        
        # pd.DataFrame(['HeatNumber'])
        # medal_data = df['HeatNumber']
        # plot.pie(medal_data, autopct='%1.1f%%', shadow=True, startangle=140)
        # plot.show()
        
        
        
        
        
        # filtered = filtered.groupby(["KartNumber"]).size()
        # filtered.plot(kind='pie', shadow=True)
        
        
              
        # plot = pd.plot.scatter(x='Aantal karts in een heat', y='Snelste tijd in een heat', title="Scatter plot between two variables X and Y")
        # plot.show(block=True)