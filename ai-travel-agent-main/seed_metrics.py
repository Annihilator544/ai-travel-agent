import random
import time
import json
from agents.metrics.recorder import start_session, end_session, snapshot


def seed(n=5):
    for i in range(n):
        s = start_session()
        # simulate planning time
        time.sleep(0.01)
        # random time saved between 30s and 600s
        time_saved = random.uniform(30, 600)
        savings = round(random.uniform(5.0, 120.0), 2)
        satisfaction = random.randint(3, 5)
        end_session(s, time_saved_seconds=time_saved, savings=savings, satisfaction=satisfaction)


def export_snapshot(outfile='metrics_snapshot.json'):
    data = snapshot()
    with open(outfile, 'w', encoding='utf-8') as f:
        json.dump(data, f)
    print('Wrote', outfile)


if __name__ == '__main__':
    seed(5)
    print('Seeded demo metrics:')
    cur = snapshot()
    print(cur)
    export_snapshot()
