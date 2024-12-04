from datetime import datetime
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

def Screening_time(all_time:tuple,check_time:str) -> bool:
    # 定义时间范围
    start_time = all_time[0]
    end_time = all_time[1]
    time_obj = datetime.strptime(check_time, "%H:%M:%S")
    is_within_range = start_time <= time_obj.time() <= end_time
    if is_within_range:
        return True
    else:
        return False

if __name__ == "__main__":
    print(dataprocessing("16:23:32"))
