import xlrd
import matplotlib.pyplot as plt
import numpy as np

left = 0.01
width = 0.9
bottom = 0.2
height = 0.9
right = left + width
top = bottom + height

commodities_no_oil = {"apples, red delicious": 2,
                      "bananas": 3,
                      "cherries": 4,
                      "grapefruit": 5,
                      "grapes, thompson seedless": 6,
                      "lemons": 7,
                      "orange juice": 8,
                      "oranges, navel": 9,
                      "oranges, valencia": 10,
                      "peaches": 11,
                      "pears, anjou": 12,
                      "strawberries": 13
                      }


def get_oil_figure():
    production_loc_oil = (
        r'U.S._Field_Production_of_Crude_Oil_Weekly.xls')
    price_loc_oil = (
        r'price_data_oil.xls')
    price_wb = xlrd.open_workbook(price_loc_oil)
    price_sheet = price_wb.sheet_by_index(1)
    production_wb = xlrd.open_workbook(production_loc_oil)
    production_sheet = production_wb.sheet_by_index(0)

    x = [production_sheet.cell_value(i, 1) for i in range(2032 - 1, 5, -1)]
    y = [price_sheet.cell_value(i, 1) for i in range(3, 1877)]
    c = x[:len(y)]
    fig, axs = plt.subplots(2)
    axs[0].plot(x)
    axs[1].plot(y)

    return plt.gcf()


def get_no_oil_commodities_figure(what_commodity='lemons'):
    plt.subplots(1)
    loc_fruits = (r'data_all_things.xls')

    wb = xlrd.open_workbook(loc_fruits)
    sheet = wb.sheet_by_index(commodities_no_oil[what_commodity] - 1)

    print(sheet.cell_value(0, 0))

    # get month values for y axis
    y = [sheet.cell_value(3, i) for i in range(2, 15) if i != 12]

    # get a list of lists to create the x values
    x = [[sheet.cell_value(i, j) for j in range(2, 15) if j != 12]
         for i in range(4, 26)]
    # find NAs on the excel and replace them with an average of the prices up to that point

    def find_average(x, col, row):
        no_na = [float(x[row][i])
                 for i in range(1, col) if type(x[row][i]) is float]

        sum_no_na = sum(no_na)
        # return the price of that month the previous year if the sum = 0
        if sum_no_na == 0:
            if row - 1 > 4:
                return sum(x[row - 1]) / 12
            else:
                return 0
        average = sum_no_na / (col)

        return average

    # find_average helper

    def clean_up_na(x):
        for row in range(len(x)):
            for col in range(len(x[row])):
                if type(x[row][col]) is str:
                    x[row][col] = find_average(x, col, row)

    clean_up_na(x)
    # get average price fluctuation

    def fluctuations(x):

        difference = 0
        # get price differences of every year
        for i in range(len(x)):
            difference += max(x[i]) - min(x[i])
        avereage_fluctuation = difference / len(x)

        # get average price to get what percentage of the price will fluctuate
        average_price = np.average(x)

        what_percentage = avereage_fluctuation/average_price
        return avereage_fluctuation, what_percentage

    fluctuation, percentage = fluctuations(x)

    for i in range(len(x)):
        year = 2021 - i
        plt.plot(y, x[i],  label=str(year))
    ax = plt.gca()
    ax.set_ylim([np.amin(x) - 0.1, np.amax(x) + 0.01])
    ax.set_title('Price of ' + what_commodity + ' from 2000 - 2021')
    ax.set_ylabel("Dollars per pound")
    ax.set_xlabel("Month")
    ax.set_facecolor('#ffbf80')
    ax.grid('on')
    # tweak the axis labels
    xlab = ax.xaxis.get_label()
    ylab = ax.yaxis.get_label()

    xlab.set_style('italic')
    xlab.set_size(10)
    ylab.set_style('italic')
    ylab.set_size(10)

    # tweak the title
    ttl = ax.title
    ttl.set_weight('bold')
    plt.legend(bbox_to_anchor=(1.05, 1))
    plt.margins(x=None, y=None, tight=True)
    info_message = f'Average Fluctuation: {fluctuation}\nFluctuation Percentage: {str(percentage * 100)}'
    plt.figtext(left, bottom, info_message,
                horizontalalignment='left',
                verticalalignment='top', color='black', size=12,
                transform=ax.transAxes)
    plt.subplots_adjust(left=0.125, right=0.820, top=0.88, bottom=0.16)
    return plt.gcf()
