# LockncodeCipher

## Overview

LockncodeCipher is a web-based application built using Flask that allows users to encode and decode text using various phonetic alphabets and cryptographic techniques. The application integrates several encryption methods such as Caesar cipher, Vigenère cipher, Base64 encoding, and AES encryption. The goal of the system is to facilitate secure communication and provide educational tools for learning about different encoding techniques and cryptography.
![image (3)](https://github.com/user-attachments/assets/596a3c83-560a-474f-af89-bc6f57bac6a3)
![image (1)](https://github.com/user-attachments/assets/1ca6a2dd-4375-4c32-90cc-f190d63d11f1)
![image (2)](https://github.com/user-attachments/assets/733aaad2-80fc-46bc-95ac-8714f21cbc88)
![image](https://github.com/user-attachments/assets/26f026cf-4655-4f25-ba85-831585a3b3ee)

## Key Components

### 1. **Phonetic Alphabet Encoding and Decoding**

**Phonetic Alphabets Supported:**

- NATO
- German
- Swedish Armed Forces
- Japanese Armed Forces
- Russian
- Ukrainian
- Hebrew
- US Military (Old)
- Western Union
- British Forces
- Australian Defence Force
- Chinese (Pinyin)
- French
- Italian
- Spanish
- Brazilian Portuguese

**Encoding:**
- Converts each character in the input phrase to its corresponding phonetic alphabet representation.
  - Example: `"A"` → `"Alfa"` (NATO), `"B"` → `"Bravo"` (NATO).

**Decoding:**
- Reverses the process and returns the original text from the phonetic code.
  - Example: `"Alfa"` → `"A"` (NATO).

### 2. **Morse Code Encoding and Decoding**

**Supported Characters:**
- A-Z, 0-9, and space.

**Encoding:**
- Converts text to Morse code.
  - Example: `"A"` → `".-"` in Morse.

**Decoding:**
- Converts Morse code back to the original text.
  - Example: `".-"` → `"A"`.

### 3. **Cryptographic Techniques**

#### Caesar Cipher
- A substitution cipher where each letter is shifted by a specified number of positions in the alphabet. Supports both encryption and decryption.
  - Example: With a shift of 3, `"A"` becomes `"D"`.

#### Vigenère Cipher
- A polyalphabetic cipher that uses a keyword to determine the shift for each letter in the text. Supports both encryption and decryption.
  - Example: For the keyword `"KEY"`, the text `"HELLO"` is encrypted based on the shifts defined by `"K"`, `"E"`, and `"Y"`.

#### Base64 Encoding/Decoding
- Converts binary data (text) into a text representation using 64 characters, making it useful for encoding data for transmission or storage.
  - Example: The string `"Hello"` is encoded as `"SGVsbG8="`.

#### AES Encryption/Decryption
- Implements the AES (Advanced Encryption Standard) algorithm to encrypt and decrypt data securely. Requires a 16, 24, or 32-byte key.
  - Example: Encrypting `"Hello"` with a key using AES results in ciphertext, which can later be decrypted back to `"Hello"` using the same key.

### 4. **Flask Web Application**

- The system uses Flask to create a web-based interface for users to interact with the encoding and decoding functionalities.
- Users can input text, select the desired encoding or cipher, and view the results.
- A simple HTML interface is used to display results and options.

## Technical Details

### Libraries Used:
- **Flask**: For building the web application.
- **cryptography.hazmat**: For cryptographic operations such as AES encryption.
- **base64**: For Base64 encoding and decoding operations.
- **string**: For string manipulations, particularly in the Vigenère cipher.

### Algorithms:
- **Caesar Cipher**: A simple substitution cipher for encryption.
- **Vigenère Cipher**: A more complex cipher based on a keyword.
- **AES (Advanced Encryption Standard)**: A symmetric encryption algorithm for secure communication.
- **Morse Code**: For encoding and decoding text using Morse code standards.

## System Flow

1. The user enters a phrase into the web interface.
2. The user selects the phonetic alphabet or cryptographic technique they wish to use.
3. The application performs the encoding or cipher operation based on user input and displays the result.
4. For encryption techniques like AES, the user provides a key for encryption/decryption.

## Potential Use Cases

- **Secure Communication**: Useful for covert communication, especially in military, defense, or emergency situations.
- **Learning Tool**: Assists users in learning different phonetic alphabets and cryptographic techniques.
- **Data Security**: Encrypts and securely transmits sensitive data.


## Usage

Open the Web Application: Navigate to the URL http://127.0.0.1:5000 in your web browser.

Select Encoding/Decoding Method: Choose from phonetic alphabet options or cryptographic techniques (Caesar cipher, Vigenère cipher, Base64 encoding/decoding, AES encryption).

Enter Text: Type the text you wish to encode or decode.

View Results: The encoded/decoded text will appear immediately after you select your desired encoding method or cipher.

## Installation

To run this project locally, follow these steps:

### 1. Clone the Repository And Run

```bash
git clone https://github.com/A1R0NHZ/LockncodeCipher.git
cd LockncodeCipher
python app.py

