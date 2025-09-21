import pandas as pd

def readcsv(filename:str, baseurl="apiv1/data/"):
    url = baseurl + filename +'.csv'
    df = pd.read_csv(url)
    return df.to_dict('records')

def main():
    df = readcsv("generacion")
    print(df)

if __name__ == '__main__':
    main()