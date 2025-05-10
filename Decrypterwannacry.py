import os
from Crypto.Cipher import AES

# Funkcja deszyfrująca plik (AES-GCM)
def decrypt_file(input_file, key):
    try:
        with open(input_file, 'rb') as f:
            nonce = f.read(16)          # IV (nonce)
            tag = f.read(16)            # Tag autentyczności
            encrypted_data = f.read()   # Zaszyfrowane dane

        cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
        decrypted_data = cipher.decrypt_and_verify(encrypted_data, tag)

        # Tworzymy plik wynikowy o nazwie oryginalnej (bez .enc)
        output_file = input_file.replace('.enc', '_odszyfrowany')
        with open(output_file, 'wb') as f:
            f.write(decrypted_data)

        print(f"Deszyfrowanie zakończone: {input_file} -> {output_file}")
    except (ValueError, KeyError) as e:
        print(f"Błąd deszyfrowania {input_file} lub błędna autentyczność danych: {e}")
    except Exception as e:
        print(f"Inny błąd: {e}")

# Funkcja, która przechodzi przez wszystkie pliki w systemie i odszyfrowuje je
def decrypt_all_files_in_system(root_dir, key):
    for dirpath, dirnames, filenames in os.walk(root_dir):  # Przechodzi przez wszystkie katalogi
        for filename in filenames:
            try:
                file_path = os.path.join(dirpath, filename)
                # Sprawdzenie, czy plik ma rozszerzenie .enc, aby odszyfrować tylko zaszyfrowane pliki
                if file_path.endswith('.enc'):
                    decrypt_file(file_path, key)
            except Exception as e:
                print(f"Błąd deszyfrowania pliku {filename}: {e}")

# Generowanie losowego klucza AES-256 (ten sam klucz, co do szyfrowania)
key = get_random_bytes(32)

# Określenie katalogu root, od którego zaczynamy (np. C:\ na Windows lub / na Linuxie)
root_dir = 'C:\\'  # Na Windowsie, jeśli chcesz odszyfrować wszystkie pliki na całym dysku.
#root_dir = '/'  # Na Linuxie

# Odszyfrowanie wszystkich plików w systemie
decrypt_all_files_in_system(root_dir, key)
