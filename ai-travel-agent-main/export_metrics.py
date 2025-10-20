import json
from agents.metrics.recorder import snapshot

def main(outfile='metrics_snapshot.json'):
    data = snapshot()
    with open(outfile, 'w', encoding='utf-8') as f:
        json.dump(data, f)
    print('Wrote', outfile)

if __name__ == '__main__':
    main()
