# Cisco Type 7 password encrypt/decrypt tool

The `Cisco type 7` password is a legacy encryption method, that is used to obscure passwords. It is **NOT** secure and can be easily decrypted. Using tools like this small `Python` script you can encrypt and/or decrypt a `Cisco type 7` password. 

## How to check your config for a type 7 password

Use this Cisco command to find the password's in the running-config
```
show running-config | include password
```
If you see somthing like this, then then config is vulnerable
```
username admin privilege 15 password 7 02050D480809
```

## Using `cisco7decrypt.py`

```bash
git clone the repository
cd cisco7decrypt/
python3 cisco7decrypt.py --help
```

<details>
<summary>Expand to see full --help usage</summary>

```
usage: cisco7decrypt.py [-h] (--decrypt TYPE7 | --encrypt PLAINTEXT | --completion)

Cisco Type 7 password encrypt/decrypt tool

options:
  -h, --help           show this help message and exit
  --decrypt TYPE7      Decrypt a Cisco Type 7 password
  --encrypt PLAINTEXT  Encrypt plaintext to Cisco Type 7
  --completion         Output bash/zsh completion script

Examples:
  Decrypt a Type 7 string:
    cisco7decrypt.py --decrypt 020E104F1B15556E0349000D0D0210450F0B27640E27363E0E160A190D

  Encrypt plaintext:
    cisco7decrypt.py --encrypt cisco

  Enable bash/zsh completion:
    cisco7decrypt.py --completion | sudo tee /etc/bash_completion.d/cisco7decrypt
```
</details>

#### Example Output

```bash
:~$ python3 cisco7decrypt.py --decrypt 02050D480809
[*] Decrypting Cisco Type 7 string
[+] Plaintext: cisco
```
```bash
:~$ python3 cisco7decrypt.py --encrypt cisco       
[*] Encrypting plaintext
[+] Type 7: 02050D480809
```
---