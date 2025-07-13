#!/usr/bin/env python3
"""
Script to download sample product images for Holoholo e-commerce website
"""

import os
import requests
from urllib.parse import urlparse

# Sample product images (using placeholder services)
sample_images = {
    'smartphone': 'https://via.placeholder.com/400x400/007bff/ffffff?text=Smartphone',
    'laptop': 'https://via.placeholder.com/400x400/28a745/ffffff?text=Laptop',
    'headphones': 'https://via.placeholder.com/400x400/dc3545/ffffff?text=Headphones',
    'tshirt': 'https://via.placeholder.com/400x400/ffc107/000000?text=T-Shirt',
    'dress': 'https://via.placeholder.com/400x400/17a2b8/ffffff?text=Dress',
    'shoes': 'https://via.placeholder.com/400x400/6f42c1/ffffff?text=Shoes',
    'tools': 'https://via.placeholder.com/400x400/fd7e14/ffffff?text=Tools',
    'book': 'https://via.placeholder.com/400x400/20c997/ffffff?text=Book'
}

def download_image(url, filename):
    """Download an image from URL and save it to filename"""
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        with open(filename, 'wb') as f:
            f.write(response.content)
        print(f"✅ Downloaded: {filename}")
        return True
    except Exception as e:
        print(f"❌ Failed to download {filename}: {e}")
        return False

def main():
    """Main function to download sample images"""
    upload_dir = 'static/uploads'
    
    # Create uploads directory if it doesn't exist
    os.makedirs(upload_dir, exist_ok=True)
    
    print("🖼️  Downloading sample product images...")
    
    success_count = 0
    for product_type, url in sample_images.items():
        filename = os.path.join(upload_dir, f"{product_type}.jpg")
        if download_image(url, filename):
            success_count += 1
    
    print(f"\n🎉 Downloaded {success_count}/{len(sample_images)} sample images!")
    print(f"📁 Images saved to: {upload_dir}")
    print("\n💡 You can now add products with these images in the admin panel!")

if __name__ == "__main__":
    main() 