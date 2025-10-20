from typing import List
import numpy as np


"""Lightweight Federated Averaging (FedAvg) prototype.

This module simulates federated training across multiple clients. Each client
has a small local model represented by a weight vector (numpy array). Clients
compute local updates and the server aggregates them via weighted averaging.

This is a demonstrative scaffold — it doesn't use TensorFlow Federated but it
shows the protocol flow and can be replaced with a proper FL framework later.
"""


def init_model(dim: int = 10):
    return np.zeros(dim)


def client_update(model, data_x, data_y, epochs=1, lr=0.1):
    """Perform a tiny SGD on linear regression L2 loss for demonstration.

    data_x: (n, dim), data_y: (n,)
    Returns updated model weights.
    """
    w = model.copy()
    for _ in range(epochs):
        preds = data_x.dot(w)
        grad = (2.0 / data_x.shape[0]) * data_x.T.dot(preds - data_y)
        w = w - lr * grad
    return w


def server_aggregate(updates: List[np.ndarray], weights: List[int] = None):
    """Aggregate client updates using weighted averaging.

    weights default to equal weighting if not provided.
    """
    if weights is None:
        weights = [1] * len(updates)
    total = sum(weights)
    avg = sum(u * w for u, w in zip(updates, weights)) / total
    return avg


def simulate_federated_rounds(num_clients: int = 3, rounds: int = 5, dim: int = 5):
    # Initialize server model
    server_model = init_model(dim)
    client_data = []
    rng = np.random.RandomState(0)
    for i in range(num_clients):
        # synthetic linear data with small differences per client
        X = rng.randn(50, dim) + i * 0.1
        true_w = rng.randn(dim)
        y = X.dot(true_w) + 0.1 * rng.randn(50)
        client_data.append((X, y))

    for r in range(rounds):
        updates = []
        for (X, y) in client_data:
            local_w = client_update(server_model, X, y, epochs=2, lr=0.01)
            updates.append(local_w)
        server_model = server_aggregate(updates)
    return server_model
