from flask import Flask, render_template, request
import base64
import string
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import os

app = Flask(__name__)

# Phonetic Alphabet Dictionaries
phonetic_alphabets = {
    "NATO": {
        'A': 'Alfa', 'B': 'Bravo', 'C': 'Charlie', 'D': 'Delta', 'E': 'Echo', 'F': 'Foxtrot',
        'G': 'Golf', 'H': 'Hotel', 'I': 'India', 'J': 'Juliett', 'K': 'Kilo', 'L': 'Lima',
        'M': 'Mike', 'N': 'November', 'O': 'Oscar', 'P': 'Papa', 'Q': 'Quebec', 'R': 'Romeo',
        'S': 'Sierra', 'T': 'Tango', 'U': 'Uniform', 'V': 'Victor', 'W': 'Whiskey', 'X': 'X-ray',
        'Y': 'Yankee', 'Z': 'Zulu'
    },
    "German": {
        'A': 'Anton', 'B': 'Berta', 'C': 'Cäsar', 'D': 'Dora', 'E': 'Emil', 'F': 'Friedrich',
        'G': 'Gustav', 'H': 'Heinrich', 'I': 'Ida', 'J': 'Julius', 'K': 'Kaufmann', 'L': 'Ludwig',
        'M': 'Martha', 'N': 'Nordpol', 'O': 'Otto', 'P': 'Paula', 'Q': 'Quelle', 'R': 'Richard',
        'S': 'Siegfried', 'T': 'Theodor', 'U': 'Ulrich', 'V': 'Viktor', 'W': 'Wilhelm', 'X': 'Xanthippe',
        'Y': 'Ypsilon', 'Z': 'Zacharias'
    },
    "Swedish Armed Forces": {
        'A': 'Adam', 'B': 'Bertil', 'C': 'Cesar', 'D': 'David', 'E': 'Erik', 'F': 'Filip',
        'G': 'Gustav', 'H': 'Helge', 'I': 'Ivar', 'J': 'Johan', 'K': 'Kalle', 'L': 'Ludvig',
        'M': 'Martin', 'N': 'Niklas', 'O': 'Olof', 'P': 'Petter', 'Q': 'Qvintus', 'R': 'Rudolf',
        'S': 'Sigurd', 'T': 'Tore', 'U': 'Urban', 'V': 'Viktor', 'W': 'Wilhelm', 'X': 'Xerxes',
        'Y': 'Yngve', 'Z': 'Zäta'
    },
    "Japanese Armed Forces": {
        'A': 'Aki', 'B': 'Banto', 'C': 'Chihei', 'D': 'Dai', 'E': 'Eiko', 'F': 'Fuji',
        'G': 'Gun', 'H': 'Hachi', 'I': 'Ichi', 'J': 'Jun', 'K': 'Kai', 'L': 'Roku',
        'M': 'Mitsu', 'N': 'Nichi', 'O': 'Oka', 'P': 'Papa', 'Q': 'Qin', 'R': 'Rai',
        'S': 'Sora', 'T': 'Tora', 'U': 'Umi', 'V': 'Vega', 'W': 'Washi', 'X': 'Xenon',
        'Y': 'Yama', 'Z': 'Zulu'
    },
    "Russian": {
        'A': 'Anna', 'B': 'Boris', 'C': 'Tsaplya', 'D': 'Dmitriy', 'E': 'Elena', 'F': 'Fyodor',
        'G': 'Grigoriy', 'H': 'Khariton', 'I': 'Ivan', 'J': 'Yogan', 'K': 'Konstantin', 'L': 'Leonid',
        'M': 'Mikhail', 'N': 'Nikolay', 'O': 'Olga', 'P': 'Pavel', 'Q': 'Shchuka', 'R': 'Roman',
        'S': 'Sergey', 'T': 'Timofey', 'U': 'Ulyana', 'V': 'Vasiliy', 'W': 'Viktor', 'X': 'Ksi',
        'Y': 'Yery', 'Z': 'Zoya'
    },
    "Ukrainian": {
        'A': 'Andriy', 'B': 'Bohdan', 'C': 'Tsentr', 'D': 'Dmytro', 'E': 'Eney', 'F': 'Fedir',
        'G': 'Hryhoriy', 'H': 'Hanna', 'I': 'Ivan', 'J': 'Yosyp', 'K': 'Kyiv', 'L': 'Leonid',
        'M': 'Mariya', 'N': 'Nazar', 'O': 'Oleksiy', 'P': 'Pavlo', 'Q': 'Shchuka', 'R': 'Roman',
        'S': 'Stepan', 'T': 'Taras', 'U': 'Ulyana', 'V': 'Vasyl', 'W': 'Volodymyr', 'X': 'Ksi',
        'Y': 'Yevhen', 'Z': 'Zorya'
    },
    "Hebrew": {
        'A': 'Avraham', 'B': 'Binyamin', 'C': 'Tzvi', 'D': 'David', 'E': 'Edward', 'F': 'Fredi',
        'G': 'Gideon', 'H': 'Hillel', 'I': 'Yitzhak', 'J': 'Yosef', 'K': 'Carmel', 'L': 'Levi',
        'M': 'Moshe', 'N': 'Nahum', 'O': 'Omer', 'P': 'Pinchas', 'Q': 'Qayin', 'R': 'Reuven',
        'S': 'Shmuel', 'T': 'Tamar', 'U': 'Uri', 'V': 'Victor', 'W': 'Wolf', 'X': 'Xai',
        'Y': 'Yaakov', 'Z': 'Zeev'
    },
    "US Military (Old) Alphabet": {
        'A': 'Able', 'B': 'Baker', 'C': 'Charlie', 'D': 'Dog', 'E': 'Easy', 'F': 'Fox',
        'G': 'George', 'H': 'How', 'I': 'Item', 'J': 'Jig', 'K': 'King', 'L': 'Love',
        'M': 'Mike', 'N': 'Nan', 'O': 'Opa', 'P': 'Peter', 'Q': 'Queen', 'R': 'Roger',
        'S': 'Sugar', 'T': 'Tare', 'U': 'Uncle', 'V': 'Victor', 'W': 'William', 'X': 'X-ray',
        'Y': 'Yoke', 'Z': 'Zebra'
    },
    "Western Union International Alphabet": {
        'A': 'Adam', 'B': 'Berlin', 'C': 'Caesar', 'D': 'Davis', 'E': 'Edward', 'F': 'Frederick',
        'G': 'George', 'H': 'Henry', 'I': 'Inger', 'J': 'John', 'K': 'King', 'L': 'Louis',
        'M': 'Mary', 'N': 'Nora', 'O': 'Ocean', 'P': 'Peter', 'Q': 'Queen', 'R': 'Robert',
        'S': 'Sam', 'T': 'Thomas', 'U': 'Union', 'V': 'Victor', 'W': 'William', 'X': 'X-ray',
        'Y': 'Yellow', 'Z': 'Zebra'
    },
    "British Forces Phonetic Alphabet": {
        'A': 'Apple', 'B': 'Bombay', 'C': 'Charlie', 'D': 'Dog', 'E': 'Edward', 'F': 'Freddie',
        'G': 'George', 'H': 'Harry', 'I': 'Indigo', 'J': 'Jig', 'K': 'King', 'L': 'London',
        'M': 'Mike', 'N': 'Niger', 'O': 'Orange', 'P': 'Peter', 'Q': 'Queen', 'R': 'Robert',
        'S': 'Sugar', 'T': 'Tare', 'U': 'Uncle', 'V': 'Victor', 'W': 'William', 'X': 'X-ray',
        'Y': 'Yellow', 'Z': 'Zulu'
    },
    "Australian Defence Force Phonetic Alphabet": {
        'A': 'Able', 'B': 'Baker', 'C': 'Charlie', 'D': 'Dog', 'E': 'Easy', 'F': 'Fox',
        'G': 'George', 'H': 'How', 'I': 'Item', 'J': 'Jig', 'K': 'King', 'L': 'Love',
        'M': 'Mike', 'N': 'Nan', 'O': 'Opa', 'P': 'Peter', 'Q': 'Queen', 'R': 'Roger',
        'S': 'Sugar', 'T': 'Tare', 'U': 'Uncle', 'V': 'Victor', 'W': 'William', 'X': 'X-ray',
        'Y': 'Yoke', 'Z': 'Zulu'
    },
    "Chinese Phonetic Alphabet (Pinyin)": {
        'A': 'ā', 'B': 'bā', 'C': 'cā', 'D': 'dā', 'E': 'ē', 'F': 'fā',
        'G': 'gā', 'H': 'hā', 'I': 'ī', 'J': 'jī', 'K': 'kā', 'L': 'lā',
        'M': 'mā', 'N': 'nā', 'O': 'ō', 'P': 'pā', 'Q': 'qī', 'R': 'rā',
        'S': 'sā', 'T': 'tā', 'U': 'ū', 'V': 'vī', 'W': 'wā', 'X': 'xī',
        'Y': 'yī', 'Z': 'zī'
    },
    "French Phonetic Alphabet": {
        'A': 'Alphonse', 'B': 'Berthe', 'C': 'César', 'D': 'Denis', 'E': 'Emile', 'F': 'Félix',
        'G': 'Georges', 'H': 'Henri', 'I': 'Irène', 'J': 'Jean', 'K': 'Kléber', 'L': 'Louis',
        'M': 'Maurice', 'N': 'Nicolas', 'O': 'Oscar', 'P': 'Pierre', 'Q': 'Quentin', 'R': 'Robert',
        'S': 'Sébastien', 'T': 'Thérèse', 'U': 'Ursule', 'V': 'Victor', 'W': 'William', 'X': 'Xavier',
        'Y': 'Yves', 'Z': 'Zacharie'
    },
    "Italian Phonetic Alphabet": {
        'A': 'Alfa', 'B': 'Bore', 'C': 'Carlo', 'D': 'Domino', 'E': 'Edo', 'F': 'Firenze',
        'G': 'Giulia', 'H': 'Hugo', 'I': 'Imola', 'J': 'Giulio', 'K': 'Kappa', 'L': 'Luca',
        'M': 'Maria', 'N': 'Napoli', 'O': 'Olio', 'P': 'Pisa', 'Q': 'Quinto', 'R': 'Roma',
        'S': 'Sandro', 'T': 'Torre', 'U': 'Uomo', 'V': 'Venezia', 'W': 'Walt', 'X': 'Xilo',
        'Y': 'Ypsilon', 'Z': 'Zebra'
    },
    "Spanish Phonetic Alphabet": {
        'A': 'Alfa', 'B': 'Bravo', 'C': 'César', 'D': 'Delta', 'E': 'Echo', 'F': 'Foxtrot',
        'G': 'Golf', 'H': 'Hotel', 'I': 'India', 'J': 'Julieta', 'K': 'Kilo', 'L': 'Lima',
        'M': 'Mike', 'N': 'November', 'O': 'Oscar', 'P': 'Papa', 'Q': 'Quebec', 'R': 'Romeo',
        'S': 'Sierra', 'T': 'Tango', 'U': 'Uniforme', 'V': 'Víctor', 'W': 'Whiskey', 'X': 'Xilófono',
        'Y': 'Yankee', 'Z': 'Zulú'
    },
    "Brazilian Portuguese Phonetic Alphabet": {
        'A': 'África', 'B': 'Brasil', 'C': 'César', 'D': 'Dado', 'E': 'Emílio', 'F': 'Fóssil',
        'G': 'Gato', 'H': 'Hotel', 'I': 'Índia', 'J': 'Jogo', 'K': 'Kilo', 'L': 'Lima',
        'M': 'Maria', 'N': 'Nação', 'O': 'Olga', 'P': 'Portugal', 'Q': 'Quênia', 'R': 'Rio',
        'S': 'Sao Paulo', 'T': 'Tucano', 'U': 'Uruguai', 'V': 'Vera', 'W': 'Wagner', 'X': 'Xuxa',
        'Y': 'Ypiranga', 'Z': 'Zebra'
    },
}

# Morse Code Dictionary
morse_code = {
    'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.', 'F': '..-.', 'G': '--.', 'H': '....',
    'I': '..', 'J': '.---', 'K': '-.-', 'L': '.-..', 'M': '--', 'N': '-.', 'O': '---', 'P': '.--.',
    'Q': '--.-', 'R': '.-.', 'S': '...', 'T': '-', 'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-',
    'Y': '-.--', 'Z': '--..', '1': '.----', '2': '..---', '3': '...--', '4': '....-', '5': '.....',
    '6': '-....', '7': '--...', '8': '---..', '9': '----.', '0': '-----', ' ': '/'
}

# Reverse Morse Code Dictionary for Decoding
reverse_morse_code = {v: k for k, v in morse_code.items()}

# Function to Encode with Phonetic Alphabet
def encode_phonetic(phrase, alphabet='NATO'):
    result = []
    for char in phrase.upper():
        if char in phonetic_alphabets[alphabet]:
            result.append(phonetic_alphabets[alphabet][char])
        else:
            result.append(char)
    return ' '.join(result)

def decode_phonetic(phrase, alphabet='NATO'):
    # Create a reverse mapping for the phonetic alphabet
    reverse_phonetic = {v: k for k, v in phonetic_alphabets[alphabet].items()}
    result = []
    for word in phrase.split():
        if word in reverse_phonetic:
            result.append(reverse_phonetic[word])
        else:
            result.append(word)  # Keep unsupported words as-is
    return ''.join(result)

# Caesar Cipher
def caesar_cipher(text, shift, mode='encrypt'):
    result = []
    for char in text:
        if char.isalpha():
            shifted = chr((ord(char.upper()) - 65 + shift) % 26 + 65)
            result.append(shifted.lower() if char.islower() else shifted)
        else:
            result.append(char)
    return ''.join(result)

# Vigenère Cipher
def vigenere_cipher(text, key, mode='encrypt'):
    alphabet = string.ascii_uppercase
    key = ''.join([char.upper() for char in key if char.upper() in alphabet])
    if not key:
        raise ValueError("Key must contain at least one valid letter (A-Z).")
    
    result = []
    key_index = 0

    for char in text:
        if char.upper() in alphabet:
            shift = alphabet.index(key[key_index % len(key)])
            if mode == 'decrypt':
                shift = -shift
            shifted_char = alphabet[(alphabet.index(char.upper()) + shift) % 26]
            result.append(shifted_char.lower() if char.islower() else shifted_char)
            key_index += 1
        else:
            result.append(char)
    return ''.join(result)

# Base64 Encoding/Decoding
def base64_encode(text):
    return base64.b64encode(text.encode()).decode()

def base64_decode(encoded_text):
    return base64.b64decode(encoded_text).decode()

# AES Encryption/Decryption
def aes_encrypt(plaintext, key):
    key = key.encode()
    if len(key) not in [16, 24, 32]:
        raise ValueError("Key must be 16, 24, or 32 bytes long")
    
    iv = os.urandom(16)
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    pad_length = 16 - (len(plaintext) % 16)
    plaintext_padded = plaintext.encode() + bytes([pad_length] * pad_length)
    ciphertext = encryptor.update(plaintext_padded) + encryptor.finalize()
    return base64.b64encode(iv + ciphertext).decode()

def aes_decrypt(ciphertext, key):
    key = key.encode()
    if len(key) not in [16, 24, 32]:
        raise ValueError("Key must be 16, 24, or 32 bytes long")
    
    ciphertext = base64.b64decode(ciphertext)
    iv = ciphertext[:16]
    ciphertext = ciphertext[16:]
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    plaintext_padded = decryptor.update(ciphertext) + decryptor.finalize()
    pad_length = plaintext_padded[-1]
    plaintext = plaintext_padded[:-pad_length]
    return plaintext.decode()

# Morse Code Encoding
def morse_encode(text):
    result = []
    for char in text.upper():
        if char in morse_code:
            result.append(morse_code[char])
        else:
            result.append(char)  # Keep unsupported characters as-is
    return ' '.join(result)

# Morse Code Decoding
def morse_decode(morse_text):
    result = []
    for code in morse_text.split(' '):
        if code in reverse_morse_code:
            result.append(reverse_morse_code[code])
        else:
            result.append(code)  # Keep unsupported Morse code as-is
    return ''.join(result)

# Web Interface
@app.route('/', methods=['GET', 'POST'])
def home():
    result = None
    input_length = 0
    output_length = 0
    error = None

    if request.method == 'POST':
        try:
            text = request.form['text']
            cipher_type = request.form['cipher']
            mode = request.form.get('mode', 'encrypt')
            input_length = len(text)

            if cipher_type == 'phonetic':
                alphabet = request.form.get('alphabet', 'NATO')
                if mode == 'encrypt':
                    result = encode_phonetic(text, alphabet)
                else:
                    result = decode_phonetic(text, alphabet)
            elif cipher_type == 'caesar':
                shift = int(request.form.get('shift', 0))
                result = caesar_cipher(text, shift, mode)
            elif cipher_type == 'vigenere':
                key = request.form.get('key', '')
                if not key:
                    raise ValueError("Key is required for Vigenère cipher.")
                result = vigenere_cipher(text, key, mode)
            elif cipher_type == 'base64':
                result = base64_encode(text) if mode == 'encrypt' else base64_decode(text)
            elif cipher_type == 'aes':
                key = request.form.get('key', '')
                if not key:
                    raise ValueError("Key is required for AES encryption.")
                result = aes_encrypt(text, key) if mode == 'encrypt' else aes_decrypt(text, key)
            elif cipher_type == 'morse':
                result = morse_encode(text) if mode == 'encrypt' else morse_decode(text)
            else:
                raise ValueError("Invalid cipher type.")

            output_length = len(result)
        except Exception as e:
            error = str(e)

    return render_template('index.html', result=result, input_length=input_length, output_length=output_length, error=error)

if __name__ == '__main__':
    app.run(debug=True)