import csv
import matplotlib.pyplot as plt
import numpy as np

type Chart = dict[tuple[int, int], float]

CHART_PATH = "chart.csv"

def read_chart() -> Chart:
    data = {}
    with open(CHART_PATH, newline="") as csvfile:
        reader = csv.reader(csvfile, delimiter=",")
        for (index, row) in enumerate(reader):
            if index == 0:
                continue
            date = row[0].split(".")
            value = row[1]
            data[(int(date[0]), int(date[1]))] = float(value)
    return data

def get_year_range(chart: Chart) -> tuple[int, int]:
    minimal_year = None
    maximum_year = None
    for date in chart.keys():
        if (minimal_year is None or date[1] < minimal_year) and date[0] == 1:
            minimal_year = date[1]
        if (maximum_year is None or date[1] > maximum_year) and date[0] == 12:
            maximum_year = date[1]
    return [minimal_year, maximum_year]

"""
returns: (minimal_yield, average_yield, maximal_yield)
"""
def get_year_values(chart: Chart, year_range: tuple[int, int], years: int) -> tuple[int, int ,int]:
    yields = []
    for year in range(year_range[0], year_range[1] - years + 2):
        start = chart[(1, year)]
        end = chart[(12, year + years - 1)]
        # years root of yield
        yield_ = ((end / start)**(1/years)) - 1
        yields.append(yield_)
    return (
        min(yields),
        sum(yields) / len(yields),
        max(yields)
    )

if __name__ == "__main__":
    chart = read_chart()
    (min_year, max_year) = get_year_range(chart)
    year_range = max_year - min_year
    

    x = list(range(1, year_range - 1))
    min_yields = []
    avg_yields = []
    max_yields = []
    for y in x:
        yield_ = get_year_values(chart, (min_year, max_year), y)
        min_yields.append(yield_[0])
        avg_yields.append(yield_[1])
        max_yields.append(yield_[2])

    plt.figure(figsize=(12, 7))
    
    plt.plot(x, min_yields, label = "Minimal yield", color = "red")
    plt.plot(x, avg_yields, label = "Average yield", color = "blue")
    plt.plot(x, max_yields, label = "Maximal yield", color = "green")

    plt.xticks(np.arange(0, max(x) + 1, 2.0))
    plt.yticks(np.arange(round(min(min_yields),1)-0.1, round(max(max_yields),1)+0.1, 0.05))

    ax = plt.gca()
    vals = ax.get_yticks()
    ax.set_yticklabels(["{:,.2%}".format(x) for x in vals])
    
    plt.title("Yield of MSCI World per length of investment since 1979")
    plt.xlabel("Invest for x years")
    plt.ylabel("Yield p.a.")
    plt.grid()
    plt.legend()

    plt.savefig("plot.svg")
    
