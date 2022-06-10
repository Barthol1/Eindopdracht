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
        self.parser.add_argument("--verbose", action='store_true')
        args = self.parser.parse_args()

        csvfile = self.getCSV(args.filename)
        analyser = NumericalAnalyser(csvfile, args.verbose)

        print(analyser.cartAmount())
        print(analyser.getUniqueDrivers())
        print(analyser.getDrivenHeats())
        print(analyser.getFastestDriverByTime())
        print(analyser.getFastestDriverByHeat())

        if(args.text == "fastest"):
            print(analyser.get_best_kart())

    def getCSV(self, filename):
        try:
            file = pd.read_csv(filename)
            return file
        except FileNotFoundError:
            print("file not found...")

if(__name__ == "__main__"):
    main = Main()
    main.run()
