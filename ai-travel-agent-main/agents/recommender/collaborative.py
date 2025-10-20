import json
from pathlib import Path
from typing import List

import numpy as np
from sklearn.neighbors import NearestNeighbors


DATA_PATH = Path(__file__).parent / 'sample_user_item.json'


def load_sample_data():
    if not DATA_PATH.exists():
        return {}
    return json.loads(DATA_PATH.read_text())


def build_model(user_item_matrix: List[List[float]]):
    arr = np.array(user_item_matrix)
    model = NearestNeighbors(metric='cosine', algorithm='brute')
    model.fit(arr)
    return model


def recommend_for_user(user_index: int, user_item_matrix: List[List[float]], k: int = 3):
    model = build_model(user_item_matrix)
    distances, indices = model.kneighbors([user_item_matrix[user_index]], n_neighbors=k + 1)
    # skip the first (self)
    return indices[0][1:]
