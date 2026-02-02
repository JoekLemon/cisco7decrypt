#!/usr/bin/env python3

"""
Cisco Type 7 password encrypt/decrypt tool.

Description: A small script to encrypt/decrypt Cisco Type 7 password's
Version: 2.0

Usage:
    cisco7decrypt.py [-h] (--decrypt TYPE7 | --encrypt PLAINTEXT | --completion)

Notes:
    
"""
__version__ = "2.0"

import argparse
import sys
import re

# =========================
# Constants
# =========================

KEY = "dsfd;kfoA,.iyewrkldJKDHSUBsgvca69834ncxv9873254k;fg87"

# ANSI colors
GREEN = "\033[92m"
CYAN = "\033[96m"
YELLOW = "\033[93m"
RESET = "\033[0m"

# Exit codes
EXIT_OK = 0
EXIT_INVALID_INPUT = 2
EXIT_RUNTIME_ERROR = 3
EXIT_INTERRUPTED = 130

# =========================
# Crypto Functions
# =========================

def decrypt_type7(enc: str) -> str:
    if len(enc) < 4 or not enc[:2].isdigit():
        raise ValueError("Invalid Type 7 string (bad index)")

    if not re.fullmatch(r"\d{2}[0-9A-Fa-f]+", enc):
        raise ValueError("Invalid Type 7 string (non-hex characters)")

    index = int(enc[:2])
    enc_pw = enc[2:]

    if len(enc_pw) % 2 != 0:
        raise ValueError("Invalid Type 7 string (odd hex length)")

    cleartext = []
    for i in range(0, len(enc_pw), 2):
        key_char = KEY[index % len(KEY)]
        val = int(enc_pw[i:i + 2], 16)
        cleartext.append(chr(val ^ ord(key_char)))
        index += 1

    return "".join(cleartext)


def encrypt_type7(cleartext: str, index: int = 2) -> str:
    result = f"{index:02d}"

    for char in cleartext:
        key_char = KEY[index % len(KEY)]
        result += f"{ord(char) ^ ord(key_char):02X}"
        index += 1

    return result

# =========================
# Completion Generator
# =========================

def print_bash_completion():
    script = sys.argv[0].split("/")[-1]
    print(f"""# Bash/Zsh completion for {script}
_{script}() {{
    local cur
    cur="${{COMP_WORDS[COMP_CWORD]}}"
    COMPREPLY=( $(compgen -W "--decrypt --encrypt --completion --help" -- "$cur") )
}}
complete -F _{script} {script}
""")

# =========================
# Main
# =========================

def main():
    parser = argparse.ArgumentParser(
        description="Cisco Type 7 password encrypt/decrypt tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  Decrypt a Type 7 string:
    cisco7decrypt.py --decrypt 02050D480809

  Encrypt plaintext:
    cisco7decrypt.py --encrypt cisco

  Enable bash/zsh completion:
    cisco7decrypt.py --completion | sudo tee /etc/bash_completion.d/cisco7decrypt

"""
    )

    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--decrypt", metavar="TYPE7", help="Decrypt a Cisco Type 7 password")
    mode.add_argument("--encrypt", metavar="PLAINTEXT", help="Encrypt plaintext to Cisco Type 7")
    mode.add_argument("--completion", action="store_true", help="Output bash/zsh completion script")

    args = parser.parse_args()

    try:
        if args.completion:
            print_bash_completion()
            sys.exit(EXIT_OK)

        if args.decrypt:
            decrypted = decrypt_type7(args.decrypt)
            print(f"{CYAN}[*] Decrypting Cisco Type 7 string{RESET}")
            print(f"{GREEN}[+] Plaintext:{RESET} {decrypted}")

        elif args.encrypt:
            encrypted = encrypt_type7(args.encrypt)
            print(f"{CYAN}[*] Encrypting plaintext{RESET}")
            print(f"{GREEN}[+] Type 7:{RESET} {encrypted}")

        sys.exit(EXIT_OK)

    except ValueError as e:
        print(f"{YELLOW}[!] Error:{RESET} {e}", file=sys.stderr)
        sys.exit(EXIT_INVALID_INPUT)

    except Exception as e:
        print(f"{YELLOW}[!] Unexpected error:{RESET} {e}", file=sys.stderr)
        sys.exit(EXIT_RUNTIME_ERROR)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{YELLOW}[!] Interrupted by user{RESET}")
        sys.exit(EXIT_INTERRUPTED)
