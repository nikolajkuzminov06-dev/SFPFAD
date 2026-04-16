import os
import requests
import struct
import keyboard
import time
import warnings

warnings.filterwarnings("ignore")
os.environ['PYTHONWARNINGS'] = 'ignore'

def download_system_file_pdb():
    os.system('')

    print("SFPFAD (System File PDB Find And Download) TOOL")

    time.sleep(0.5)

    print("")

    print("Чтобы программа работала тебе нужен Windows")

    time.sleep(0.5)

    print("")

    print("Работает только если у Microsoft есть файл pdb для этого файла")

    time.sleep(0.5)

    system_file_path = input('Путь до системного файла (Или просто перетащи сюда): ').strip('"')
    save_dir = os.path.join(os.path.expanduser("~"), input('В какую папку (Которая находится в ~ а именно в папке твоего пользователя) ты установишь файл (Или просто перетащи сюда): ').strip('"'))

    with open(system_file_path, "rb") as f:
        data = f.read()

    offset = data.find(b"RSDS")
    if offset == -1:
        print("")
        print("Сигнатура RSDS не найдена.")
        return

    guid_raw = data[offset + 4: offset + 20]
    age_raw = data[offset + 20: offset + 24]

    pdb_name_end = data.find(b"\x00", offset + 24)
    pdb_name = data[offset + 24: pdb_name_end].decode("ascii")

    output_file_path = os.path.join(save_dir, pdb_name)

    os.makedirs(os.path.dirname(output_file_path), exist_ok=True)

    g1 = guid_raw[0:4][::-1].hex().upper()
    g2 = guid_raw[4:6][::-1].hex().upper()
    g3 = guid_raw[6:8][::-1].hex().upper()
    g4 = guid_raw[8:16].hex().upper()

    age_int = struct.unpack("<I", age_raw)[0]
    age = f"{age_int:X}"

    if not age: age = '1'

    full_guid = f"{g1}{g2}{g3}{g4}{age}"
    url = f"https://msdl.microsoft.com/download/symbols/{pdb_name}/{full_guid}/{pdb_name}"

    print(f"Попытка скачать: {url}")

    try:
        r = requests.get(url, stream=True)
        if r.status_code == 200:
            with open(output_file_path, 'wb') as f:
                print("")
                print("Теперь жди загрузки!")
                print("\n")

                last_switch_time = time.time()
                is_first_line = True

                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)

                    current_time = time.time()
                    if current_time - last_switch_time > 1.0:
                        is_first_line = not is_first_line
                        last_switch_time = current_time

                        if is_first_line:
                            print("\033[A\033[K" + "Проверка то что программа работает (Если текст перестал прыгать то программа зависла)" + "\n" + " " * 100 + "\r", end="")
                        else:
                            print("\033[A\033[K" + " " * 30 + "\n" + "Проверка то что программа работает (Если текст перестал прыгать то программа зависла)" + "\r", end="")
            print("")
            print(f"Файл сохранен в: {output_file_path}")
        else:
            print("")
            print(f"Сервер ответил ошибкой {r.status_code}.")
    except Exception as e:
        print("")
        print(f"Ошибка при скачивании: {e}")

    print("")

    print("Нажмите ENTER чтобы продолжить...")

    keyboard.wait('enter')

if __name__ == "__main__":
    download_system_file_pdb()
