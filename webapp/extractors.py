import pandas as pd
def transform(dataset):
    new_dataset = []
    for data in dataset:
        new_data = {}
        for key,value in data.items():
            key = key.lower().replace(" ","_")
            if key=="gender":
                if value.lower()=="male":
                    value = "0"
                elif value.lower() == "female":
                    value = "1"
                else:
                    value = "2"
            new_data[key]=value
        new_dataset.append(new_data)
    return new_dataset
def getFromCSV(file):
    df = pd.read_csv(file)
    return transform(df.T.to_dict().values())
def getFromXLS(file):
    df = pd.read_excel(file)
    return transform(df.T.to_dict().values())