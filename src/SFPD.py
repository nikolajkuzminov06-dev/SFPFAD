import os
import requests
import keyboard
import warnings

warnings.filterwarnings("ignore")
os.environ['PYTHONWARNINGS'] = 'ignore'


def download_by_link():
    os.system('')

    url = input('\nВставь прямую ссылку на файл: ').strip()
    save_dir = input('Путь до папки (куда сохранить): ').strip('"')

    if not url:
        print("Ссылка не введена!")
        return

    pdb_name = url.split('/')[-1] if '/' in url else 'downloaded_file.pdb'
    output_file_path = os.path.join(save_dir, pdb_name)

    try:
        os.makedirs(save_dir, exist_ok=True)
        print(f"\nПопытка скачать: {url}")

        r = requests.get(url, stream=True)
        if r.status_code == 200:
            with open(output_file_path, 'wb') as f:
                print("Загрузка идет...")
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
            print(f"\nГотово! Файл сохранен в: {output_file_path}")
        else:
            print(f"\nОшибка сервера: {r.status_code}")
    except Exception as e:
        print(f"\nОшибка: {e}")

    print("\nНажмите ENTER для выхода...")
    keyboard.wait('enter')
