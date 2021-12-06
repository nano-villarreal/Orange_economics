import xlrd
import matplotlib.pyplot as plt
import numpy as np

loc = (r'C:\Users\emili\Projects\Oragne_Economics\data.xls')

wb = xlrd.open_workbook(loc)
sheet = wb.sheet_by_index(0)

print(sheet.cell_value(0, 0))

# get month values for y axis
y = [sheet.cell_value(3, i) for i in range(1, 14) if i != 11]

# get a list of lists to create the x values
x = [[sheet.cell_value(i, j) for j in range(1, 14) if j != 11]
     for i in range(4, 26)]

# find NAs on the excel and replace them with an average of the prices up to that point


def find_average(x, col, row):
    no_na = [x[row][i] for i in range(col) if x[i] != 'NA']
    sum_no_na = sum(no_na)
    average = sum_no_na / (col)
    if average > 1.8:
        print(sum_no_na, 'sum')
        print(col, 'col')

    return average

# find_average helper


def clean_up_na(x):
    for row in range(len(x)):
        for col in range(len(x[row])):
            if x[row][col] == 'NA':
                x[row][col] = find_average(x, col, row)


clean_up_na(x)


for i in range(len(x)):
    year = 2021 - i
    plt.plot(y, x[i],  label=str(year))
ax = plt.gca()
ax.set_ylim([np.amin(x) - .1, np.amax(x) + .01])
ax.set_title('Price of oranges from 2000 - 2021')
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

plt.show()

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

print(fluctuation, 'fluctuation')
print(str(percentage * 100) + '% of fluctuation')
