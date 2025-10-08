import math
import io
import os
import chess
import chess.pgn

def to_binary_string(value: int, length: int) -> str:
    return format(value, "b").zfill(length)

def bytes_to_bitstring(b: bytes) -> str:
    return "".join(format(byte, "08b") for byte in b)

def bitstring_to_bytes(bits: str) -> bytes:
    if len(bits) % 8 != 0:
        bits = bits.ljust(len(bits) + (8 - len(bits) % 8), "0")
    return bytes(int(bits[i:i + 8], 2) for i in range(0, len(bits), 8))

def encode(input_path, output_pgn):
    with open(input_path, "rb") as f:
        file_bytes = f.read()

    ext = input_path.split(".")[-1] if "." in input_path else "bin"
    ext_bytes = ext.encode("ascii")[:255]
    header = len(file_bytes).to_bytes(8, "big") + bytes([len(ext_bytes)]) + ext_bytes
    full_data = header + file_bytes
    bits = bytes_to_bitstring(full_data)

    total_bits = len(bits)
    bit_index = 0
    board = chess.Board()
    pgn_games = []

    print(f"[+] Encoding {input_path} ({len(file_bytes)} bytes) → {output_pgn}")

    while bit_index < total_bits:
        legal_moves = list(board.legal_moves)
        n_legal = len(legal_moves)

        if n_legal <= 1:
            game = chess.pgn.Game()
            game.add_line(board.move_stack)
            pgn_games.append(str(game))
            board.reset()
            continue

        k = math.floor(math.log2(n_legal))
        if k <= 0:
            k = 1
        if bit_index + k > total_bits:
            k = total_bits - bit_index

        chunk = bits[bit_index:bit_index + k]
        idx = int(chunk, 2)
        move = list(board.legal_moves)[idx % n_legal]
        board.push(move)
        bit_index += k

        if board.is_game_over() or bit_index >= total_bits:
            game = chess.pgn.Game()
            game.add_line(board.move_stack)
            pgn_games.append(str(game))
            board.reset()

    with open(output_pgn, "w", encoding="utf-8") as f:
        f.write("\n\n".join(pgn_games))

    print(f"[✓] Encoding selesai — hasil disimpan di {output_pgn}\n")

def decode(pgn_path, output_noext):
    with open(pgn_path, "r", encoding="utf-8") as f:
        content = f.read()

    games = [g.strip() for g in content.strip().split("\n\n") if g.strip()]
    bitstream = ""
    header_done = False
    file_len = None
    ext_len = None
    ext = ""
    total_bits = None

    print(f"[+] Decoding file {pgn_path} ...")

    for game_text in games:
        game = chess.pgn.read_game(io.StringIO(game_text))
        board = chess.Board()

        for node in game.mainline():
            mv = node.move
            legal_moves = list(board.legal_moves)
            n_legal = len(legal_moves)
            k = int(math.log2(n_legal)) if n_legal > 1 else 1
            idx = [i for i, m in enumerate(legal_moves) if m == mv][0]
            bitstream += to_binary_string(idx, k)
            board.push(mv)

            # Baca header ketika cukup bit
            if not header_done and len(bitstream) >= (8 * 8 + 8):
                file_len_bytes = bitstring_to_bytes(bitstream[:64])
                file_len = int.from_bytes(file_len_bytes, "big")

                ext_len = bitstring_to_bytes(bitstream[64:72])[0]
                ext_bits = bitstream[72:72 + ext_len * 8]
                if len(ext_bits) >= ext_len * 8:
                    ext = bitstring_to_bytes(ext_bits).decode("ascii", errors="ignore")
                    total_bits = (8 + 1 + ext_len) * 8 + file_len * 8
                    header_done = True

            if header_done and len(bitstream) >= total_bits:
                break
        if header_done and len(bitstream) >= total_bits:
            break

    data_bits = bitstream[(8 + 1 + ext_len) * 8:(8 + 1 + ext_len) * 8 + file_len * 8]
    data_bytes = bitstring_to_bytes(data_bits)
    output_file = f"{output_noext}.{ext}" if ext else f"{output_noext}.bin"

    with open(output_file, "wb") as f:
        f.write(data_bytes)

    print(f"[✓] Decoding selesai — hasil disimpan di {output_file}\n")
    return output_file

def Hide_Image():
    if not os.path.exists("Examples/secret.png"):
        from PIL import Image
        img = Image.new("RGB", (64, 64), color=(120, 50, 220))
        img.save("Examples/secret.png")
        print("[i] File dummy 'secret.png' dibuat otomatis.")

    encode("Examples/secret.png", "Encoded/image_encoded_chess.pgn")

def extract_image():
    decode("Encoded/image_encoded_chess.pgn", "Decoded/image_decoded_output")

def Hide_text(msg):
    if not os.path.exists("Examples/secret.txt"):
        with open("Examples/secret.txt", "w", encoding="utf-8") as f:
            f.write(msg)
        print("[i] File dummy 'Examples/secret.txt' dibuat otomatis.")
    with open("Examples/secret.txt", "w", encoding="utf-8") as f:
        f.write(msg)

    encode("Examples/secret.txt", "Encoded/text_encoded_chess.pgn")

def extract_text():
    decode("Encoded/text_encoded_chess.pgn", "Decoded/text_decoded_output")

def menu():
    os.system('cls')
    print("Pilih menu mana yang mau digunakan : ")
    print("1. Sembunyikan gambar dan extract")
    print("2. Sembunyikan text dan extract")
    print("3. exit")

def submenu():
    print("Ingin mencoba lagi?")
    print("1. Ya")
    print("2. Tidak")


#####   Main  #####
i = 0
while i != 3:
    menu()
    i = int(input("Masukkan Pilihan : "))
    if i == 1:
        Hide_Image()
        extract_image()
        submenu()
        j=int(input("Masukkan pilihan : "))
        if j == 1:
            continue
        else :
            break
    elif i == 2:
        msg = input("Masukkan pesan : ")
        Hide_text(msg)
        extract_text()
        with open("Encoded/text_encoded_chess.pgn", "r") as f:
            text = f.read()
        print(f"Hasil encodenya adalah \n" + text)
        print()
        with open("Decoded/text_decoded_output.txt", "r") as f:
            text = f.read()
        print(f"Hasil decodenya adalah " + text)
        print()
        submenu()
        j=int(input("Masukkan pilihan : "))
        if j == 1:
            continue
        else :
            break
    elif i<1 or i>3 :
        print("Tidak ada dalam pilihan system error")
        break
        
        
    
