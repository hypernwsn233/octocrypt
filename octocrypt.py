#!/usr/bin/env python3
"""
octocrypt: AES-256 file encryption with compression and digital signatures.

Features:
- AES-256-GCM encryption (password-based)
- Strong password enforcement
- zlib compression
- Ed25519 digital signature
- CLI + Tkinter GUI
"""

from __future__ import annotations

import argparse
import base64
import getpass
import hashlib
import json
import os
import secrets
import struct
import sys
import zlib
from pathlib import Path
from typing import Any

from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.ed25519 import (
    Ed25519PrivateKey,
    Ed25519PublicKey,
)
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt

MAGIC = b"OCTO"
VERSION = 1
DEFAULT_EXT = ".octo"
KEY_DIR = Path.home() / ".octocrypt"
PRIVATE_KEY_PATH = KEY_DIR / "ed25519_private.pem"
PUBLIC_KEY_PATH = KEY_DIR / "ed25519_public.pem"


class OctoCryptError(Exception):
    pass


def b64e(data: bytes) -> str:
    return base64.b64encode(data).decode("ascii")


def b64d(data: str) -> bytes:
    return base64.b64decode(data.encode("ascii"))


def enforce_strong_password(password: str) -> None:
    if len(password) < 12:
        raise OctoCryptError("Password must have at least 12 characters.")
    has_upper = any(c.isupper() for c in password)
    has_lower = any(c.islower() for c in password)
    has_digit = any(c.isdigit() for c in password)
    has_symbol = any(not c.isalnum() for c in password)
    if not (has_upper and has_lower and has_digit and has_symbol):
        raise OctoCryptError(
            "Password must include upper, lower, digit and symbol characters."
        )


def derive_key(password: str, salt: bytes, n: int = 2**15, r: int = 8, p: int = 1) -> bytes:
    kdf = Scrypt(salt=salt, length=32, n=n, r=r, p=p)
    return kdf.derive(password.encode("utf-8"))


def ensure_signing_keys() -> tuple[Ed25519PrivateKey, Ed25519PublicKey]:
    KEY_DIR.mkdir(parents=True, exist_ok=True)

    if PRIVATE_KEY_PATH.exists() and PUBLIC_KEY_PATH.exists():
        private_key = serialization.load_pem_private_key(
            PRIVATE_KEY_PATH.read_bytes(), password=None
        )
        if not isinstance(private_key, Ed25519PrivateKey):
            raise OctoCryptError("Invalid private key format.")

        public_key = serialization.load_pem_public_key(PUBLIC_KEY_PATH.read_bytes())
        if not isinstance(public_key, Ed25519PublicKey):
            raise OctoCryptError("Invalid public key format.")
        return private_key, public_key

    private_key = Ed25519PrivateKey.generate()
    public_key = private_key.public_key()

    PRIVATE_KEY_PATH.write_bytes(
        private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption(),
        )
    )
    PUBLIC_KEY_PATH.write_bytes(
        public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo,
        )
    )
    return private_key, public_key


def export_public_key_bytes() -> bytes:
    _, public_key = ensure_signing_keys()
    return public_key.public_bytes(
        encoding=serialization.Encoding.Raw,
        format=serialization.PublicFormat.Raw,
    )


def read_private_key() -> Ed25519PrivateKey:
    private_key, _ = ensure_signing_keys()
    return private_key


def sign_data(data: bytes) -> tuple[bytes, bytes]:
    private_key = read_private_key()
    public_key = private_key.public_key()
    signature = private_key.sign(data)
    pub_raw = public_key.public_bytes(
        encoding=serialization.Encoding.Raw,
        format=serialization.PublicFormat.Raw,
    )
    return signature, pub_raw


def verify_signature(data: bytes, signature: bytes, pub_raw: bytes) -> bool:
    try:
        pub = Ed25519PublicKey.from_public_bytes(pub_raw)
        pub.verify(signature, data)
        return True
    except InvalidSignature:
        return False


def build_container(metadata: dict[str, Any], ciphertext: bytes) -> bytes:
    meta_bytes = json.dumps(metadata, separators=(",", ":")).encode("utf-8")
    return MAGIC + struct.pack(">BBI", VERSION, 0, len(meta_bytes)) + meta_bytes + ciphertext


def parse_container(blob: bytes) -> tuple[dict[str, Any], bytes]:
    if len(blob) < 10 or blob[:4] != MAGIC:
        raise OctoCryptError("Invalid file format.")

    version, _flags, meta_len = struct.unpack(">BBI", blob[4:10])
    if version != VERSION:
        raise OctoCryptError(f"Unsupported version: {version}")

    if len(blob) < 10 + meta_len:
        raise OctoCryptError("Corrupted file (metadata length mismatch).")

    meta_bytes = blob[10 : 10 + meta_len]
    ciphertext = blob[10 + meta_len :]

    try:
        metadata = json.loads(meta_bytes.decode("utf-8"))
    except json.JSONDecodeError as exc:
        raise OctoCryptError("Corrupted metadata.") from exc

    return metadata, ciphertext


def encrypt_file(input_path: Path, output_path: Path, password: str, compress_level: int = 9) -> None:
    enforce_strong_password(password)

    data = input_path.read_bytes()
    compressed = zlib.compress(data, level=compress_level)

    salt = secrets.token_bytes(16)
    nonce = secrets.token_bytes(12)
    key = derive_key(password, salt)

    aes = AESGCM(key)
    ciphertext = aes.encrypt(nonce, compressed, None)

    signed_payload = salt + nonce + ciphertext
    signature, sign_pubkey = sign_data(signed_payload)

    metadata = {
        "alg": "AES-256-GCM",
        "kdf": "scrypt",
        "kdf_n": 2**15,
        "kdf_r": 8,
        "kdf_p": 1,
        "salt": b64e(salt),
        "nonce": b64e(nonce),
        "compression": "zlib",
        "original_name": input_path.name,
        "sha256_plain": hashlib.sha256(data).hexdigest(),
        "signature_alg": "Ed25519",
        "signature": b64e(signature),
        "sign_pubkey": b64e(sign_pubkey),
    }

    container = build_container(metadata, ciphertext)
    output_path.write_bytes(container)


def decrypt_file(input_path: Path, output_path: Path | None, password: str, verify: bool = True) -> Path:
    blob = input_path.read_bytes()
    metadata, ciphertext = parse_container(blob)

    salt = b64d(metadata["salt"])
    nonce = b64d(metadata["nonce"])

    if verify:
        signature = b64d(metadata["signature"])
        pub_raw = b64d(metadata["sign_pubkey"])
        if not verify_signature(salt + nonce + ciphertext, signature, pub_raw):
            raise OctoCryptError("Digital signature verification failed.")

    key = derive_key(
        password,
        salt,
        n=int(metadata.get("kdf_n", 2**15)),
        r=int(metadata.get("kdf_r", 8)),
        p=int(metadata.get("kdf_p", 1)),
    )

    aes = AESGCM(key)
    try:
        compressed = aes.decrypt(nonce, ciphertext, None)
    except Exception as exc:
        raise OctoCryptError("Decryption failed. Wrong password or corrupted file.") from exc

    data = zlib.decompress(compressed)

    expected_hash = metadata.get("sha256_plain")
    current_hash = hashlib.sha256(data).hexdigest()
    if expected_hash and expected_hash != current_hash:
        raise OctoCryptError("Integrity check failed (SHA-256 mismatch).")

    if output_path is None:
        original_name = metadata.get("original_name") or input_path.stem
        output_path = input_path.with_name(original_name)

    output_path.write_bytes(data)
    return output_path


def ask_password(confirm: bool = False) -> str:
    p1 = getpass.getpass("password: ")
    if not confirm:
        return p1
    p2 = getpass.getpass("confirm password: ")
    if p1 != p2:
        raise OctoCryptError("Passwords do not match.")
    return p1


def cmd_encrypt(args: argparse.Namespace) -> int:
    src = Path(args.input)
    if not src.exists() or not src.is_file():
        raise OctoCryptError(f"Input file not found: {src}")

    if args.output:
        dst = Path(args.output)
    else:
        dst = src.with_suffix(DEFAULT_EXT)

    password = args.password or ask_password(confirm=True)
    encrypt_file(src, dst, password=password, compress_level=args.compress_level)
    print(f"file encrypted -> {dst}")
    return 0


def cmd_decrypt(args: argparse.Namespace) -> int:
    src = Path(args.input)
    if not src.exists() or not src.is_file():
        raise OctoCryptError(f"Input file not found: {src}")

    password = args.password or ask_password(confirm=False)
    dst = Path(args.output) if args.output else None

    out = decrypt_file(src, dst, password=password, verify=not args.no_verify)
    print(f"file decrypted -> {out}")
    return 0


def cmd_keygen(_args: argparse.Namespace) -> int:
    ensure_signing_keys()
    print(f"private key -> {PRIVATE_KEY_PATH}")
    print(f"public key  -> {PUBLIC_KEY_PATH}")
    return 0


def launch_gui() -> int:
    import tkinter as tk
    from tkinter import filedialog, messagebox

    root = tk.Tk()
    root.title("OctoCrypt")
    root.geometry("560x360")

    selected_file = tk.StringVar()
    output_file = tk.StringVar()
    password_var = tk.StringVar()
    mode_var = tk.StringVar(value="encrypt")

    def choose_input() -> None:
        path = filedialog.askopenfilename()
        if path:
            selected_file.set(path)

    def choose_output() -> None:
        path = filedialog.asksaveasfilename()
        if path:
            output_file.set(path)

    def run_action() -> None:
        try:
            src = Path(selected_file.get())
            if not src.exists():
                raise OctoCryptError("Select a valid input file.")

            pwd = password_var.get()
            if not pwd:
                raise OctoCryptError("Enter password.")

            out = Path(output_file.get()) if output_file.get() else None

            if mode_var.get() == "encrypt":
                if out is None:
                    out = src.with_suffix(DEFAULT_EXT)
                encrypt_file(src, out, pwd)
                messagebox.showinfo("OctoCrypt", f"Encrypted:\n{out}")
            else:
                result = decrypt_file(src, out, pwd)
                messagebox.showinfo("OctoCrypt", f"Decrypted:\n{result}")
        except Exception as exc:
            messagebox.showerror("OctoCrypt", str(exc))

    padding = {"padx": 10, "pady": 8}

    tk.Label(root, text="Mode:").grid(row=0, column=0, sticky="e", **padding)
    tk.OptionMenu(root, mode_var, "encrypt", "decrypt").grid(row=0, column=1, sticky="we", **padding)

    tk.Label(root, text="Input file:").grid(row=1, column=0, sticky="e", **padding)
    tk.Entry(root, textvariable=selected_file, width=46).grid(row=1, column=1, sticky="we", **padding)
    tk.Button(root, text="Browse", command=choose_input).grid(row=1, column=2, **padding)

    tk.Label(root, text="Output file:").grid(row=2, column=0, sticky="e", **padding)
    tk.Entry(root, textvariable=output_file, width=46).grid(row=2, column=1, sticky="we", **padding)
    tk.Button(root, text="Browse", command=choose_output).grid(row=2, column=2, **padding)

    tk.Label(root, text="Password:").grid(row=3, column=0, sticky="e", **padding)
    tk.Entry(root, textvariable=password_var, width=46, show="*").grid(row=3, column=1, sticky="we", **padding)

    tk.Button(root, text="Run", command=run_action, height=2).grid(row=4, column=1, sticky="we", **padding)

    help_text = (
        "AES-256-GCM + scrypt + zlib + Ed25519\n"
        "Tip: use a strong password (12+ chars, upper/lower/digit/symbol)."
    )
    tk.Label(root, text=help_text, justify="left").grid(row=5, column=0, columnspan=3, **padding)

    root.grid_columnconfigure(1, weight=1)
    root.mainloop()
    return 0


def cmd_gui(_args: argparse.Namespace) -> int:
    return launch_gui()


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="octocrypt", description="AES-256 file encryption tool")
    sub = parser.add_subparsers(dest="command", required=True)

    p_enc = sub.add_parser("encrypt", help="Encrypt a file")
    p_enc.add_argument("input", help="Input file path")
    p_enc.add_argument("-o", "--output", help="Output encrypted file")
    p_enc.add_argument("--password", help="Password (unsafe in shell history)")
    p_enc.add_argument("--compress-level", type=int, default=9, choices=range(1, 10))
    p_enc.set_defaults(func=cmd_encrypt)

    p_dec = sub.add_parser("decrypt", help="Decrypt a file")
    p_dec.add_argument("input", help="Input encrypted file path")
    p_dec.add_argument("-o", "--output", help="Output decrypted file")
    p_dec.add_argument("--password", help="Password (unsafe in shell history)")
    p_dec.add_argument("--no-verify", action="store_true", help="Skip digital signature verification")
    p_dec.set_defaults(func=cmd_decrypt)

    p_key = sub.add_parser("keygen", help="Generate signing keys")
    p_key.set_defaults(func=cmd_keygen)

    p_gui = sub.add_parser("gui", help="Launch GUI")
    p_gui.set_defaults(func=cmd_gui)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        return args.func(args)
    except OctoCryptError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
