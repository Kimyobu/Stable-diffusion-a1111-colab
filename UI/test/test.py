import argparse

parser = argparse.ArgumentParser(description='')

parser.add_argument('--use_google_drive', action='store_true')

args = parser.parse_args()

Use_drive = args.use_google_drive

if Use_drive is True:
    print('Mounting google drive...')