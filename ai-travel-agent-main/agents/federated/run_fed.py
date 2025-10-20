from .fedavg import simulate_federated_rounds


def main():
    model = simulate_federated_rounds(num_clients=4, rounds=3, dim=6)
    print('Trained model weights (sample):', model[:6])


if __name__ == '__main__':
    main()
