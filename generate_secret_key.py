"""
Script pour générer une SECRET_KEY aléatoire pour Flask
"""
import secrets

def generate_secret_key():
    """Génère une clé secrète aléatoire de 64 caractères"""
    key = secrets.token_hex(32)
    print("=" * 60)
    print("SECRET_KEY générée:")
    print("=" * 60)
    print(key)
    print("=" * 60)
    print("\nCopiez cette clé dans votre fichier .env:")
    print(f"SECRET_KEY={key}")
    print("=" * 60)
    return key

if __name__ == "__main__":
    generate_secret_key()

