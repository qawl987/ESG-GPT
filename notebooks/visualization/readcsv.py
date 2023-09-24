import csv
# Open the CSV file
def readcsv(folder, file):
    # label_cnt = 27 if 'xml' in folder else 26
    label_cnt = 26
    # print(folder)
    # if 'xml' in folder:
    #     print('yes')
    with open(f'./{folder}/{file}', 'r') as f:
        # Create a CSV reader object
        reader = csv.reader(f)
        labels = []
        counts = []
        # Iterate through the rows of the CSV file
        for row in reader:
            #   collect column value
            labels.append(row[1])
        for i in range(label_cnt):
            # count label number in collected column value
            count = labels.count(str(i))
            counts.append(count)
    # Set data
    if 'xml' not in folder:
        counts.append(300)
    values = counts
    min_value = min(values)
    max_value = max(values)
    # Calculate the range of the values
    value_range = max_value - min_value
    # Normalize the values and store them in a new list
    normalized_values = []
    for value in values:
        normalized_value = ((value - min_value) / value_range) * 100
        normalized_value = int(normalized_value)
        normalized_values.append(normalized_value)
    return normalized_values