import os
import struct
import keyboard
import warnings

warnings.filterwarnings("ignore")
os.environ['PYTHONWARNINGS'] = 'ignore'


def get_system_file_pdb_link():
    os.system('')

    system_file_path = input('\nПуть до системного файла (Поддерживается D&D): ').strip('"')

    try:
        with open(system_file_path, "rb") as f:
            data = f.read()

        offset = data.find(b"RSDS")
        if offset == -1:
            print("\nСигнатура RSDS не найдена.")
            return

        guid_raw = data[offset + 4: offset + 20]
        age_raw = data[offset + 20: offset + 24]
        pdb_name_end = data.find(b"\x00", offset + 24)
        pdb_name = data[offset + 24: pdb_name_end].decode("ascii")

        g1 = guid_raw[0:4][::-1].hex().upper()
        g2 = guid_raw[4:6][::-1].hex().upper()
        g3 = guid_raw[6:8][::-1].hex().upper()
        g4 = guid_raw[8:16].hex().upper()

        age_int = struct.unpack("<I", age_raw)[0]
        age = f"{age_int:X}"
        if not age:
            age = '1'

        full_guid = f"{g1}{g2}{g3}{g4}{age}"
        url = f"https://msdl.microsoft.com/download/symbols/{pdb_name}/{full_guid}/{pdb_name}"

        print("\n" + "=" * 30)
        print(f"PDB Name: {pdb_name}")
        print(f"GUID:     {full_guid}")
        print(f"URL:      {url}")
        print("=" * 30)

    except Exception as e:
        print(f"\nОшибка при анализе файла: {e}")

    print("\nНажмите ENTER чтобы выйти...")
    keyboard.wait('enter')
