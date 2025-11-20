#!/usr/bin/env python
"""
Quick script to create Admin user
Run: python create_admin.py
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ocmsproject.settings')
django.setup()

from adminapp.models import Admin

username = input("Enter admin username (default: admin): ").strip() or "admin"
password = input("Enter admin password (default: admin123): ").strip() or "admin123"

if Admin.objects.filter(username=username).exists():
    print(f"❌ Admin user '{username}' already exists!")
else:
    Admin.objects.create(username=username, password=password)
    print(f"✅ Admin user created successfully!")
    print(f"   Username: {username}")
    print(f"   Password: {password}")
    print(f"\n👉 Now login at: http://127.0.0.1:8000/login")

