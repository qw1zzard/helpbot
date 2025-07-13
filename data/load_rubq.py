import csv

import requests

INPUT_JSON_URL = 'https://raw.githubusercontent.com/vladislavneon/RuBQ/master/RuBQ_2.0/RuBQ_2.0_dev.json'
OUTPUT_CSV = 'data/data.csv'


def load_rubq(url: str) -> list[dict]:
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()

    entries = [
        {
            'id': idx,
            'question': item['question_text'].strip(),
            'answer': item.get('answer_text'),
        }
        for idx, item in enumerate(data, start=1)
    ]
    return entries


def write_csv(entries: list[dict], output_path: str):
    with open(output_path, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['id', 'question', 'answer'])
        writer.writeheader()
        for item in entries:
            writer.writerow(item)


if __name__ == '__main__':
    entries = load_rubq(INPUT_JSON_URL)
    write_csv(entries, OUTPUT_CSV)
    print(f'Converted {len(entries)} entries to {OUTPUT_CSV}')
