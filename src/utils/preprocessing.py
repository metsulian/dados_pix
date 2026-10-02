from datetime import datetime

def prepare_data(data):
    for row in data:
        row["AnoMes"] = datetime.strptime(str(row["AnoMes"]), "%Y%m").date()
    return data