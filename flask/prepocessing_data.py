import re

header = [ "time", "temperature", "dew_point", "humidity", "wind", "wind_speed", "wind_gust", "pressure", "precip", "condition" ]
mask_number = [0, 1,1,1, 0, 1,1,2,2,0]

def get_number_or_string(strin, is_number):
  if is_number == 0:
    return strin
  new_val = re.findall(r"[-+]?(?:\d*\.\d+|\d+)",strin)
  if is_number == 1:
    return int(new_val[0])
  if is_number == 2:
    return float(new_val[0])
  return strin

def preprocessing_from_csv(row):
  newDoc = { header[i]:get_number_or_string(row[i], mask_number[i]) for i in range(0, len(header)) }
  return newDoc