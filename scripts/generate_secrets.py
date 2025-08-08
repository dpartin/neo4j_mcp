#!/usr/bin/env python3
"""
Script to generate secure credentials for the Neo4j MCP server.
Run this script to generate secure passwords and keys for production use.
"""

import secrets
import string
import os
from pathlib import Path


def generate_secure_password(length: int = 32) -> str:
    """Generate a secure random password."""
    alphabet = string.ascii_letters + string.digits + "!@#$%^&*"
    return ''.join(secrets.choice(alphabet) for _ in range(length))


def generate_secret_key() -> str:
    """Generate a secure secret key."""
    return secrets.token_urlsafe(32)


def main():
    """Generate secure credentials and update .env file."""
    print("🔐 Generating secure credentials for Neo4j MCP Server")
    print("=" * 50)
    
    # Generate secure credentials
    neo4j_password = generate_secure_password(24)
    secret_key = generate_secret_key()
    
    print(f"📝 Generated credentials:")
    print(f"   Neo4j Password: {neo4j_password}")
    print(f"   Secret Key: {secret_key}")
    print()
    
    # Check if .env file exists
    env_file = Path(".env")
    if env_file.exists():
        print("⚠️  .env file already exists!")
        response = input("Do you want to update it with new credentials? (y/N): ")
        if response.lower() != 'y':
            print("❌ Aborted. Credentials not updated.")
            return
    else:
        print("📄 Creating new .env file...")
    
    # Read env.example as template
    example_file = Path("env.example")
    if not example_file.exists():
        print("❌ Error: env.example file not found!")
        return
    
    # Read template and replace placeholders
    with open(example_file, 'r') as f:
        content = f.read()
    
    # Replace placeholders with generated values
    content = content.replace("your-secure-password-here", neo4j_password)
    content = content.replace("your-secret-key-here-change-in-production", secret_key)
    
    # Write to .env file
    with open(env_file, 'w') as f:
        f.write(content)
    
    print("✅ .env file updated with secure credentials!")
    print()
    print("🔧 Next steps:")
    print("   1. Review the generated .env file")
    print("   2. Update Neo4j password in your database")
    print("   3. Keep the .env file secure and never commit it to version control")
    print("   4. Run: docker-compose up -d")
    print()
    print("⚠️  Security Notes:")
    print("   - Never commit .env file to version control")
    print("   - Use different credentials for each environment")
    print("   - Regularly rotate passwords and keys")


if __name__ == "__main__":
    main()
