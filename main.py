import csv
import glob

# Note - due to most people having two put files
# The activity keys are Put1 = 3 and Put2 = 31 
# So Put2 would have to be manually adjusted at the end
Activities = {
    "Data\\Drink.csv" : "A01",
    "Data\\Pick.csv" : "A02",
    "Data\\Put1.csv" : "A03",
    "Data\\Put2.csv" : "A031",
    "Data\\Sweep.csv" : "A05",
    "Data\\Wash.csv" : "A06",
    "Data\\Wave.csv" : "A07",
    "Data\\Walk.csv" : "A08",
    "Data\\Sit.csv" : "A09",
    "Data\\Back.csv" : "A10",
    "Data\\Front.csv" : "A11",
    "Data\\Left.csv" : "A12",
    "Data\\Right.csv" : "A13",
    "Data\\Rotate.csv" : "A14"
}

# Takes in all csv files from data
csvFileNames = glob.glob("Data/*.csv")
print(csvFileNames)

# LOAD ID HERE, S--
subject = 'S39' 

for file in csvFileNames:
    # Checks for activity in Activities map, prints if activity is missed
    if not (file in Activities.keys()):
        print(file, "- missed")
        continue
    prefix = ".\\Final\\" + subject + Activities[file] + 'T0'

    data = []

    # Stores each important line from the file and stores it in a temp array
    # Then appends that temp array to data
    # Determines cuttof by blank spaces and skips the very first line
    with open(file, 'r') as ReadFile:
        reader = csv.reader(ReadFile, delimiter=',')
        
        temp_data = []
        
        accepting = False
        for row in reader:
            if not accepting:
                accepting = True
                continue
            if row[0] == '':
                if len(temp_data) > 0:
                    data.append(temp_data)
                    temp_data = []
            else:
                temp_data.append(row[0:6])
        if len(temp_data) > 0:
            data.append(temp_data)


    # Dumps each array from data into it's own csv file
    for i in range(0, len(data)):
        toWrite = prefix + str(i+1) + ".csv"
        with open(toWrite, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_MINIMAL)
            for line in data[i]:
                writer.writerow(line)
    