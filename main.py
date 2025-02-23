import os
import asyncio
import argparse
import aiofiles
import logging

# Налаштуйте логування помилок.
logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')

async def copy_file(source_file, destination_file):
    try:
        async with aiofiles.open(source_file, 'rb') as src_file:
            content = await src_file.read()
        async with aiofiles.open(destination_file, 'wb') as dest_file:
            await dest_file.write(content)
    except Exception as e:
        logging.error(f"Error copying {source_file} to {destination_file}: {e}")

async def read_folder(source_folder, output_folder):
    for root, _, files in os.walk(source_folder):
        for file in files:
            source_file = os.path.join(root, file)
            file_extension = os.path.splitext(file)[1][1:]
            destination_folder = os.path.join(output_folder, file_extension)
            os.makedirs(destination_folder, exist_ok=True)
            destination_file = os.path.join(destination_folder, file)
            await copy_file(source_file, destination_file)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Organize files by extension.")
    parser.add_argument("source_folder", help="The source folder to read files from.")
    parser.add_argument("output_folder", help="The output folder to save organized files.")
    args = parser.parse_args()

    asyncio.run(read_folder(args.source_folder, args.output_folder))