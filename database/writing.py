import json
import pathlib

from data_model import BadCookerData

def load(db_path: pathlib.Path) -> BadCookerData:
    with db_path.open("r") as f:
        dict_data = json.load(f)
        return BadCookerData.from_dict(dict_data)

def save(db_path: pathlib.Path, data: BadCookerData) -> None:
    with db_path.open("w") as f:
        dict_data = data.to_dict()
        json.dump(dict_data, f)
