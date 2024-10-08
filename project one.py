PRODUCT_ID_INDEX = 0
PRODUCT_NAME_INDEX = 1
CATEGORY_INDEX = 2
DISCOUNTED_PRICE_INDEX = 3
ACTUAL_PRICE_INDEX = 4
DISCOUNTED_PERCENTAGE_INDEX = 5
RATING_INDEX = 6
RATING_COUNT_INDEX = 7


def read_csvfile(csvfile):
    """
    Read the file and return a list contains the all the data in the file.
    :param csvfile: file name
    :return: list of the data in the file
    """
    data = []

    with open(csvfile, "r") as file:
        is_first_row = True
        for line in file:
            line = line.strip().split(",")
            # For non-first row data, covert some fields to appropriate data types
            if not is_first_row:
                line[DISCOUNTED_PRICE_INDEX] = int(line[DISCOUNTED_PRICE_INDEX])
            else:
                is_first_row = False
            data.append(line)
    return data


def task1(data, category):
    """
    Find the product with the highest discounted price and the highest rating.
    :param data: list of the data in the file
    :return: a tuple (product_id1, product_id2)
    """
    result1 = []
    highest_discounted_price = -float('inf')
    lowest_discounted_price = float('inf')

    product_id1 = None
    product_id2 = None

    # read all the rows in the file
    for line in data:
        if line[CATEGORY_INDEX] == category:
            discounted_price = line[DISCOUNTED_PRICE_INDEX]
            product_id = line[PRODUCT_ID_INDEX]

            # find the highest discounted price
            if discounted_price > highest_discounted_price:
                highest_discounted_price = discounted_price
                product_id1 = product_id.lower()

            # find the lowest discounted price
            if discounted_price < lowest_discounted_price:
                lowest_discounted_price = discounted_price
                product_id2 = product_id.lower()

    # if not exist return 0
    if product_id1 is None or product_id2 is None:
        return [0, 0]

    result1 = [product_id1, product_id2]

    return result1
def task2(data, category):
    """
    calculate the mean median and mean absolute deviation of products for a specific category whith rating count > 1000
    :param data: list of the data in the file
    :param category: specific category
    :return: (mean, median, mad)
    """
    result2 = []
    actual_prices =[]
    for line in data:
        if line[CATEGORY_INDEX] == category and int(line[RATING_COUNT_INDEX]) > 1000:
            actual_price = line[ACTUAL_PRICE_INDEX]
            actual_prices.append(actual_price)

    if not actual_prices:
        return [0, 0, 0]  # if no actual price satisfys the requirement, return 0 

    n = len(actual_prices)

    # calculate mean value
    mean_value = sum(actual_prices) / n

    # calculate median value
    actual_prices.sort()  # ordering the sequence of actual price

    if n % 2 == 1:
        median_value = actual_prices[n // 2]  # odd number of elements, the middle two values divided by  2
    else:
        median_value = (actual_prices[n // 2 - 1] + actual_prices[n // 2]) / 2  # even number of elements, the average value of the middle two

    # calculate mean absolute deviation 
    mad_value = sum(abs(price - mean_value) for price in actual_prices) / n
    result2 = [mean_value, int(median_value), mad_value]

    return result2
def task3(data):
    """
    Calculate the standard deviation of the discounted percentages for products with rating
in the range 3.3≤rating≤4.3, for each category.
    :param data: list of data in the file
    :return: arrange the standard deviation in desc order (4 d.p.)
    """
    result3 = []
    std_deviations = []

    # obtain all the categories 
    categories = list(set(line[CATEGORY_INDEX] for line in data))

    # define a function to calculate the square root part
    def calculate_square_root(value):
        if value == 0:
            return 0
        guess = value / 2.0
        for _ in range(20):
            guess = (guess + value / guess) / 2.0
        return guess

    # define a function to calculate standard deviation
    def calculate_standard_deviation(discounted_percentages):
        if len(discounted_percentages) < 2:
            return 0  # cannot calculate sd

        mean_value = sum(discounted_percentages) / len(discounted_percentages)
        squared_diff_sum = sum((x - mean_value) ** 2 for x in discounted_percentages)
        return calculate_square_root(squared_diff_sum / (len(discounted_percentages) - 1))

    # calculate standard deviation for each category
    for category in categories:
        discounted_percentages = []
        for line in data:
            try:
                rating = float(line[RATING_INDEX])  # change the data type of rating into float
            except ValueError:
                continue  # if unsuccessful skip that line and continue

            if line[CATEGORY_INDEX] == category and 3.3 <= rating <= 4.3:
                discounted_percentages.append(line[DISCOUNTED_PERCENTAGE_INDEX])

        # calculate the standard deviation of a category
        std_deviation = calculate_standard_deviation(discounted_percentages)

        if std_deviation > 0:  # record sd > 0 only
            std_deviations.append(std_deviation)

    # descending order
    std_deviations.sort(reverse=True)

    # 4 decimal place
    result3 = [round(std_dev, 4) for std_dev in std_deviations]

    # return the standard deviation
    return result3
def task4(sales_file, highest_product_id, lowest_product_id):
    """
    calculate the correlation coefficient between the sales of the highest discounted product and the sales of the lowest disocunted product 
    :param sales_file: a TXT file containing sales data
    :param highest_product_id: the product id which has the highest sales
    :param lowest_product_id: the product id which has the lowest sales
    """

    result4 = [] # store the result

    highest_product_sales = [] # store the sales of the highest product id
    lowest_product_sales = [] # store the sales of the lowest product id

    with open(sales_file, "r") as file:
        # process each line in the sales_file
        for line in file:
            line = line.strip().split(",")
            year_sales_highest = 0
            year_sales_lowest = 0

            for item in line:
                try:
                    product_id, units_sold = item.split(":")
                    product_id = product_id.strip().upper() # product ID to uppercase

                    if product_id == highest_product_id.upper(): 
                        year_sales_highest = int(units_sold) # Record sales for the highest product ID
                    elif product_id == lowest_product_id.upper():
                        year_sales_lowest = int(units_sold) # Record sales for the lowest product ID

                except ValueError:
                    continue # skip the adnormal lines
            highest_product_sales.append(year_sales_highest)
            lowest_product_sales.append(year_sales_lowest)
      # check if the list has enought amount of data      
    if len(highest_product_sales) < 2 or len(lowest_product_sales) < 2:
        return 0
        n = len(highest_product_sales)
    # Calculate means of the sales data
    mean_x = sum(highest_product_sales) / n 
    mean_y = sum(lowest_product_sales) / n

    numerator = sum((highest_product_sales[i] - mean_x) * (lowest_product_sales[i] - mean_y) for i in range(n))
    denominator_x = sum((highest_product_sales[i] - mean_x) ** 2 for i in range(n))
    denominator_y = sum((lowest_product_sales[i] - mean_y) ** 2 for i in range(n))
    # mean cannot be 0
    if denominator_x == 0 or denominator_y == 0:
        return 0
    # calculate the correlation coefficient 
    correlation = numerator / ((denominator_x ** 0.5) * (denominator_y ** 0.5))
    result4 = round(correlation, 4)
    return result4

# summarise the results
def main(products_file, sales_file, category):
    data = read_file(products_file)
    op1 = task1(data, category)
    op2 = task2(data, category)
    op3 = task3(data)
    op4 = task4(sales_file, op1[0], op1[1])
    return op1, op2, op3, op4




