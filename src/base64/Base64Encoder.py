import base64


"""
    base64 characters
    [A-Z]   26
    [a-z]   26
    [0-9]   10
    +/      2
    Total:  64 = 2 ^ 6 Bit
"""

base64_chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"


def encode_base64(data: str) -> str:
    binary_data = ''.join(format(ord(char), '08b') for char in data)

    # pad the binary data to a multiple of 6
    while len(binary_data) % 6 != 0:
        binary_data += '0'

    # group the binary data into chunks of 6 bits and convert to decimal
    chunks = [int(binary_data[i:i+6], 2) for i in range(0, len(binary_data), 6)]

    # map decimal values to Base64 characters
    encoded_data = ''.join(base64_chars[i] for i in chunks)

    # add padding '=' characters if needed
    padding = (4 - len(encoded_data) % 4) % 4
    encoded_data += '=' * padding
    return encoded_data

# --------------------------------------------------


def decode_base64(data: str) -> str:
    pass


def builtin_encode(data: str) -> str:
    encoded_data = base64.b64encode(data.encode("utf-8")).decode("utf-8")
    return encoded_data


def builtin_decode(data: str) -> str:
    decoded_data = base64.b64decode(data.encode("utf-8")).decode("utf-8")
    return decoded_data


# if __name__ == "__main__":
input_data = "Hello World"
print(ord('A'))
print(format(ord('A'), '08b'))
encoded_data_1 = builtin_encode(input_data)
encoded_data_2 = builtin_encode(input_data)
print(encoded_data_1)
print(encoded_data_2)
