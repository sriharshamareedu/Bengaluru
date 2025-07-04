import json
import pickle
import numpy as np

__locations = None
__data_columns = None
__model = None

def get_estimated_price(location, sqft, bhk, bath):
    if __model is None or __data_columns is None:
        raise Exception("Model or data columns not loaded")

    try:
        loc_index = __data_columns.index(location.lower())
    except:
        loc_index = -1

    x = np.zeros(len(__data_columns))
    x[0] = sqft
    x[1] = bath
    x[2] = bhk
    if loc_index >= 0:
        x[loc_index] = 1

    return round(__model.predict([x])[0], 2)


def get_location_names():
    return __locations

def load_saved_artifacts():
    print("loading saved artifacts..start")
    global __data_columns
    global __locations
    global __model

    with open("./artifcats/columns.json") as f:
        #__data_columns = json.load(f)['data_columns']
        __data_columns = [col.lower() for col in json.load(f)['data_columns']]
        __locations = __data_columns[3:]

    with open("./artifcats/bangalore_home_prices_model.pickle", 'rb') as f:
        __model = pickle.load(f)

    print("Loading saved artifacts..done")

# ✅ Automatically load when module is imported
load_saved_artifacts()

# Optional test block
if __name__ == '__main__':
    print(get_location_names())
    print(get_estimated_price('1st Phase JP Nagar', 1000, 3, 3))
    print(get_estimated_price('1st Phase JP Nagar', 1000, 2, 2))
    print(get_estimated_price('Kalhalli', 1000, 3, 3))
    print(get_estimated_price('Ejipura', 1000, 3, 3))
