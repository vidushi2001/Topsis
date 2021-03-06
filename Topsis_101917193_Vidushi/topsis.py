import pandas as pd
import numpy as np

rollNumber = '101917193'

class topsis:

    def __init__(self, input, weight, impact, output):
        self.input = input
        self.weight = weight
        self.impact = impact
        self.output = output
        self.roll_no = rollNumber
        

    def calculate(self):
        weights = self.weight.split(',')
        try:
            weights = [int(i) for i in weights]
        except ValueError:
            print("Weights should only be numbers\n")
            exit()

        impacts = self.impact.split(',')
        for i in impacts:
            if i != '+' and i != '-':
                print("impacts should be either + or -")
                exit()

        try:
            read_file = pd.read_excel(self.input)
            read_file.to_csv(self.roll_no + '-data.csv', index=None, header=True)
            df = pd.read_csv(self.roll_no + "-data.csv")
        except FileNotFoundError:
            print("File not found")
            exit()

        if len(df.columns) < 3:
            print("Input file should contain atleast 3 columns.\n")
            exit()

        check = {len(df.columns)-1, len(weights), len(impacts)}
        if len(check) != 1:
            print(
                "Number of weights, number of impacts and number of indicators must be same.\n")
            exit()

        for col in df.iloc[:, 1:]:
            for i in df[col]:
                if isinstance(i, float) == False:
                    print("Columns must contain numeric values\n")
                    exit()

        arr = np.array(df.iloc[:, 1:])

        rss = np.sqrt(np.sum(arr**2, axis=0))

        arr = np.divide(arr, rss)
        arr = arr*weights

        ideals = np.zeros((arr.shape[1], 2))
        for i in range(len(impacts)):
            l = np.zeros(2)
            if impacts[i] == '+':
                l[0] = max(arr[:, i])
                l[1] = min(arr[:, i])
            elif impacts[i] == '-':
                l[0] = min(arr[:, i])
                l[1] = max(arr[:, i])
            ideals[i, 0] = l[0]
            ideals[i, 1] = l[1]
        ideals = ideals.T

        distances = np.zeros((arr.shape[0], 2))

        for i in range(arr.shape[0]):
            best_dist = np.linalg.norm(arr[i, :] - ideals[0, :])
            worst_dist = np.linalg.norm(arr[i, :] - ideals[1, :])
            distances[i, 0] = best_dist
            distances[i, 1] = worst_dist

        performance_score = np.divide(
            distances[:, 1], np.add(distances[:, 0], distances[:, 1]))

        rank = np.zeros(arr.shape[0])

        temp = list(performance_score)
        count = 1
        for i in range(len(performance_score)):
            ind = np.argmax(temp)
            rank[ind] = count
            count += 1
            temp[ind] = -99

        df_out = df
        df_out['Topsis Score'] = performance_score
        df_out['Rank'] = rank
        df_out.to_csv(self.output, index=None)
        print("Completed succesfully! Check " +
              self.output+" for the output\n")