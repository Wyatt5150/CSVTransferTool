import csv
import glob
import pandas as pd

Subjects = {
    "Subject_Name_Here" : "SID_Number_Here"
}

Activities = {
    "Drink" : "01",
    "Pick" : "02",
    "Put" : "03",
    "Sweep" : "05",
    "Wash" : "06",
    "Wave" : "07",
    "Walk" : "08",
    "Sit" : "09",
    "Back" : "10",
    "Front" : "11",
    "Left" : "12",
    "Right" : "13",
    "Rotate" : "14"
}


def FindId(query, document):
    id = -1
    for subject in document:
        if subject.lower() in query.lower():
            id = str(document[subject])
            break
    return id

def Get_Page(filePath):
    file = pd.ExcelFile(filePath)
    page = -1
    for sheet in file.sheet_names:
        if "trim" in sheet:
            page = sheet
            break

    return page

def Sort_CSV(src, dst):
    data = []
    # Stores each important line from the file and stores it in a temp array
    # Then appends that temp array to data
    # Determines cuttof by blank spaces and skips the very first line
    with open(src, 'r') as ReadFile:
        reader = csv.reader(ReadFile, delimiter=',')
        
        temp_data = []
        
        accepting = False
        for row in reader:
            if not accepting:
                accepting = True
                continue
            if len(row) < 1:
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
        toWrite = dst + str(i+1) + ".csv"
        with open(toWrite, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_MINIMAL)
            for line in data[i]:
                writer.writerow(line)
    

folderNames = glob.glob("Data/*")

for folder in folderNames:
    SID = FindId(folder, Subjects)
    if SID == -1:
        print("Could not find SID associated with: ", folder)
        continue
    SID = "S" + SID

    fileNames = glob.glob(folder + "/*.xlsx")
    for file in fileNames:
        AID = FindId(file, Activities)
        if AID == -1:
            print("Could not find AID associated with: ", file)
            continue
        AID = "A" + AID

        page = Get_Page(file)
        if page == -1:
            print("Could not parse file: ", file)
            continue

        sheet = pd.read_excel(file, sheet_name = page, header = 0)

        csv_loc = {
            'p_a' : [f'CSVs/P_Accel_Raw/{SID + AID}.csv', f'CSVs/P_Accel_Final/{SID + AID}T0'],
            'p_g' : [f'CSVs/P_Gyro_Raw/{SID + AID}.csv', f'CSVs/P_Gyro_Final/{SID + AID}T0'],
            'w_a' : [f'CSVs/W_Accel_Raw/{SID + AID}.csv', f'CSVs/W_Accel_Final/{SID + AID}T0'],
            'w_g' : [f'CSVs/W_Gyro_Raw/{SID + AID}.csv', f'CSVs/W_Gyro_Final/{SID + AID}T0']
        }

        for key in csv_loc:
            sheet.to_csv(csv_loc[key][0], encoding='utf-8', index = False, columns=sheet.filter(like=key))
            Sort_CSV(csv_loc[key][0],csv_loc[key][1])
