from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
import os

def generate_rent_receipt_image(receipt_number, payment_method, house, apartment, amount, balance, generated_on, tenant=None):
    # Create a new blank image (white background)
    img = Image.new('RGB', (400, 600), color=(255, 255, 255))
    d = ImageDraw.Draw(img)

    # Optional: Load a font (you can use a built-in or custom TTF file)
    try:
        font = ImageFont.truetype('arial.pil', 20)
    except IOError:
        font = ImageFont.load_default()

    # Header
    d.text((10, 10), "EstateManage Payment", font=font, fill=(0, 0, 10))
    d.text((10, 60), f"House: {house}", font=font, fill=(0, 0, 0))
    d.text((10, 80), f"Apartment: {apartment}", font=font, fill=(0, 0, 0))
    d.text((10, 120), f"Receipt Number: #{receipt_number}", font=font, fill=(0, 0, 0))
    d.text((10, 140), f"Date Received:{datetime.today().now()}", font=font, fill=(0, 0, 0))

    d.text((10, 160), "-----------------------------", font=font, fill=(0, 0, 0))

    if tenant:
        d.text((10, 180), "Paid by:", font=font, fill=(0, 0, 0))
        d.text((300, 180), f"{tenant}", font=font, fill=(0, 0, 0))

    d.text((10, 210 if tenant else 180), "Rent Amount for Apartment:", font=font, fill=(0, 0, 0))
    d.text((300, 210 if tenant else 180), f"$ {amount}", font=font, fill=(0, 0, 0))

    d.text((10, 240 if tenant else 210), "Rent Balance for Apartment:", font=font, fill=(0, 0, 0))
    d.text((300, 240 if tenant else 210), f"$ {balance}", font=font, fill=(0, 0, 0))

    d.text((10, 270 if tenant else 240), "Amount Paid Date:", font=font, fill=(0, 0, 0))
    d.text((300, 270 if tenant else 240), f"{generated_on}", font=font, fill=(0, 0, 0))

    d.text((10, 300 if tenant else 270), "Transaction Payment Method:", font=font, fill=(0, 0, 0))
    d.text((300, 300 if tenant else 270), f"{payment_method}", font=font, fill=(0, 0, 0))

    # Divider
    d.text((10, 320 if tenant else 290), "-----------------------------", font=font, fill=(0, 0, 0))

    # Footer
    d.text((10, 340 if tenant else 310), "Approved", font=font, fill=(0, 0, 0))
    d.text((10, 360 if tenant else 330), "Thank you for your payment!", font=font, fill=(0, 0, 0))

    # Get the user's Downloads directory
    downloads_path = os.path.expanduser(f"~/Downloads/#{receipt_number}_rent_receipt.jpg")

    # Save the image in the Downloads folder
    img.save(downloads_path)
