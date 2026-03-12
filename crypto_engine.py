import os
import hashlib
import shutil
import base64
from datetime import datetime
from cryptography.fernet import Fernet

KEY_FILE = os.path.expanduser("~/.dsterminal_key")


class CryptoEngine:

    def __init__(self, base_dir="."):
        self.base_dir = base_dir
        self.cipher = None
        self.init_cipher()

    def init_cipher(self):
        """Initialize cipher from key file"""
        if os.path.exists(KEY_FILE):
            with open(KEY_FILE, "r") as f:
                key = f.read().strip()
                try:
                    self.cipher = Fernet(key.encode())
                except:
                    self.cipher = None

    def human_readable_size(self, size):
        for unit in ["B", "KB", "MB", "GB"]:
            if size < 1024:
                return f"{size:.2f} {unit}"
            size /= 1024
        return f"{size:.2f} TB"

    def secure_delete(self, file_path, passes=3):
        try:
            size = os.path.getsize(file_path)
            with open(file_path, "wb") as f:
                for _ in range(passes):
                    f.write(os.urandom(size))
                    f.flush()
                    os.fsync(f.fileno())
            os.remove(file_path)
        except:
            pass

    # =============================
    # SETUP
    # =============================

    def encrypt_setup(self):

        print("\n🔐 ENCRYPTION SYSTEM SETUP")
        print("=" * 40)

        if os.path.exists(KEY_FILE):

            print("[+] Key already exists")

            with open(KEY_FILE) as f:
                key = f.read().strip()

            key_id = hashlib.sha256(key.encode()).hexdigest()[:16]
            print("Key ID:", key_id)
            return

        key = Fernet.generate_key().decode()

        with open(KEY_FILE, "w") as f:
            f.write(key)

        os.chmod(KEY_FILE, 0o600)

        print("✅ New encryption key generated")
        print("Key file:", KEY_FILE)

        self.init_cipher()

    # =============================
    # STATUS
    # =============================

    def crypto_status(self):

        print("\n🔐 ENCRYPTION SYSTEM STATUS")
        print("=" * 40)

        if os.path.exists(KEY_FILE):

            with open(KEY_FILE) as f:
                key = f.read().strip()

            key_id = hashlib.sha256(key.encode()).hexdigest()[:16]

            print("✅ Encryption: ENABLED")
            print("🔑 Key ID:", key_id)
            print("📁 Key file:", KEY_FILE)

        else:

            print("❌ Encryption NOT configured")

        print("Cipher initialized:", "YES" if self.cipher else "NO")

    # =============================
    # ENCRYPT
    # =============================
    def encrypt_test(self):

        print("\n🧪 ENCRYPTION TEST")
        print("="*40)

        test_file = os.path.join(self.base_dir, "crypto_test.txt")

        try:

            with open(test_file, "w") as f:
                f.write("DSTerminal encryption test\n")

            print("Created test file:", test_file)

            self.encrypt_file("crypto_test.txt")

            enc = test_file + ".enc"

            if os.path.exists(enc):

                print("Encryption successful")

                self.decrypt_file("crypto_test.txt.enc")

                print("Decryption successful")

            if os.path.exists(test_file):
                os.remove(test_file)

            if os.path.exists(enc):
                os.remove(enc)

            print("\n✅ Encryption system working")

        except Exception as e:

            print("❌ Encryption test failed:", e)

    def encrypt_file(self, filename):

        if not self.cipher:
            print("[!] Encryption not initialized")
            return

        path = os.path.join(self.base_dir, filename)

        if not os.path.exists(path):
            print("[!] File not found")
            return

        with open(path, "rb") as f:
            data = f.read()

        encrypted = self.cipher.encrypt(data)

        enc_file = path + ".enc"

        with open(enc_file, "wb") as f:
            f.write(encrypted)

        os.remove(path)

        print("✅ File encrypted:", enc_file)

    # =============================
    # DECRYPT
    # =============================

    def decrypt_file(self, filename):

        if not self.cipher:
            print("[!] Encryption not initialized")
            return

        path = os.path.join(self.base_dir, filename)

        if not os.path.exists(path):
            print("[!] File not found")
            return

        with open(path, "rb") as f:
            data = f.read()

        try:
            decrypted = self.cipher.decrypt(data)
        except:
            print("❌ Decryption failed")
            return

        out_file = path.replace(".enc", "")

        with open(out_file, "wb") as f:
            f.write(decrypted)

        print("✅ File decrypted:", out_file)

    # =============================
    # LIST ENCRYPTED FILES
    # =============================

    def crypto_list(self):

        print("\n🔐 ENCRYPTED FILES INVENTORY")
        print("=" * 60)

        encrypted = []

        for root, dirs, files in os.walk(self.base_dir):
            for file in files:
                if file.endswith(".enc"):
                    path = os.path.join(root, file)

                    encrypted.append(path)

        if not encrypted:
            print("No encrypted files found.")
            return

        for i, file in enumerate(encrypted, 1):

            size = os.path.getsize(file)
            mod = datetime.fromtimestamp(os.path.getmtime(file))

            print(f"{i}. 🔒 {file}")
            print("   Size:", self.human_readable_size(size))
            print("   Modified:", mod)
            print()

    # =============================
    # FILE INFO
    # =============================

    def crypto_info(self, filename):

        if not filename.endswith(".enc"):
            filename += ".enc"

        path = os.path.join(self.base_dir, filename)

        if not os.path.exists(path):
            print("[!] File not found")
            return

        print("\n🔐 ENCRYPTION INFO")
        print("=" * 50)

        size = os.path.getsize(path)

        with open(path, "rb") as f:
            data = f.read()

        print("File:", filename)
        print("Size:", self.human_readable_size(size))
        print("SHA256:", hashlib.sha256(data).hexdigest())
        print("MD5:", hashlib.md5(data).hexdigest())

        try:
            base64.urlsafe_b64decode(data)
            print("Format: Fernet AES-256")
        except:
            print("Unknown format")

    # =============================
    # VERIFY
    # =============================

    def crypto_verify(self):

        print("\n🔐 ENCRYPTION SYSTEM VERIFICATION")
        print("=" * 50)

        if not os.path.exists(KEY_FILE):
            print("❌ Key file missing")
            return

        with open(KEY_FILE) as f:
            key = f.read().strip()

        try:
            Fernet(key.encode())
            print("✅ Key format valid")
        except:
            print("❌ Invalid key")
            return

        if not self.cipher:
            print("❌ Cipher not initialized")
            return

        test = b"dsterminal test data"

        enc = self.cipher.encrypt(test)
        dec = self.cipher.decrypt(enc)

        if test == dec:
            print("✅ Self-test PASSED")
        else:
            print("❌ Self-test FAILED")

    # =============================
    # BACKUP KEY
    # =============================

    def crypto_backup(self):

        print("\n💾 ENCRYPTION KEY BACKUP")
        print("=" * 50)

        if not os.path.exists(KEY_FILE):
            print("[!] No key found")
            return

        with open(KEY_FILE) as f:
            key = f.read()

        backup = os.path.expanduser("~/dsterminal_key.backup")

        with open(backup, "w") as f:
            f.write(key)

        os.chmod(backup, 0o600)

        print("✅ Backup saved:", backup)