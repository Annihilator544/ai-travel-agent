from agents.optimizer.cost_optimizer import rank_by_price, recommend


def test_rank_and_recommend():
    options = [
        {'id': 'a', 'price': 300},
        {'id': 'b', 'price': 150},
        {'id': 'c', 'price': 450}
    ]
    ranked = rank_by_price(options)
    assert [o['id'] for o in ranked] == ['b', 'a', 'c']

    rec = recommend(options, budget=200)
    assert rec['id'] == 'b' and rec['within_budget'] is True

    rec2 = recommend(options, budget=100)
    assert rec2['id'] == 'b' and rec2['within_budget'] is False
