def dataprocessing(data:str):
    try:
        if "#" in data:
            return 0
        else:
            if "" == data:
                return 0
            else:
                return float(data)
    except:
        return data
if __name__ == "__main__":
    print(dataprocessing("16:23:32"))