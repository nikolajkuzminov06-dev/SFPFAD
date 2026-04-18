from src import SFPF
from src import SFPD
from src import SFPFAD

while True:
    print("Меню")
    print("1. Найти и скачать")
    print("2. Найти")
    print("3. Скачать")
    print("0. Выйти")
    choice = input('--> ')

    if choice == "1":
        SFPFAD.download_system_file_pdb()

    elif choice == "2":
        SFPF.get_system_file_pdb_link()

    elif choice == "3":
        SFPD.download_by_link()

    elif choice == "0":
        break

    else:
        print("Неверный ввод")