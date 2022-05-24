from logging import exception
import sys
import argparse
import pandas as pd
import Analyser
from Analyser import NumericalAnalyser
class Main:
    parser = argparse.ArgumentParser()
    def run(self):
        self.parser.add_argument("filename")
        self.parser.add_argument("--text")
        self.parser.add_argument("--graphics")
        args = self.parser.parse_args()

        csvfile = self.getCSV(args.filename)
        analyser = NumericalAnalyser(csvfile)

        print(analyser.cartAmount())
        print(analyser.getUniqueDrivers())
        print(analyser.getDrivenHeats())
        if self.parser.text:
            print(analyser.getFastestDriverByTime())
            print(analyser.getFastestDriverByHeat())


    def getCSV(self, filename):
        try:
            file = pd.read_csv(filename)
            return file
        except FileNotFoundError:
            print("file not found...")

if(__name__ == "__main__"):
    main = Main()
    main.run()
