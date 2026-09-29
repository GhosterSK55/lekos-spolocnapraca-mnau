def vypis_oliver():
    for i in range(10):
        print("oliver")

def menu():
    while True:
        print("\n--- MENU ---")
        print("1. Vypis oliver 10x")
        print("2. Pozdrav")
        print("3. Koniec")
        volba = input("Zadaj volbu (1-3): ")

        if volba == "1":
            vypis_oliver()
        elif volba == "2":
            print("Ahoj, ja som Oliver!")
        elif volba == "3":
            print("Koniec programu.")
            break
        else:
            print("Neplatna volba, skus znova.")

if __name__ == "__main__":
    vypis_oliver()
    menu()
