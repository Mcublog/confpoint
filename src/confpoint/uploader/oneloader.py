import argparse
import logging
import os
import sys
from pathlib import Path
from typing import List

from colorama import Fore as Clr

import confpoint.shareup as shareup
from confpoint.version import VERSION

logging.basicConfig(level=logging.INFO)
log = logging.getLogger("oneloader")

DESCRIPTION = f'{Clr.GREEN}The SharePoint {Clr.YELLOW}uploader{Clr.GREEN} v{VERSION}{Clr.RESET}'

DEFAULT_CONNECTION_TIMEOUT_S = 15

def main():
    parser = argparse.ArgumentParser(
        prog='uploader', description=DESCRIPTION)
    parser.add_argument('-u', '--user', type=str, help='User name (usually mail address)', required=True)
    parser.add_argument('-p',
                        '--password',
                        type=str,
                        help='Your password for uploading file to the OneDrive',
                        required=True)
    parser.add_argument('-r', '--remote', type=str, help='OneDrive path like: Projects/BMS3', required=True)
    parser.add_argument('-g',
                        '--group',
                        type=str,
                        help='OneDrive shared group, root directory for all documents and files',
                        required=True)
    parser.add_argument('-f', '--file', type=str, help='The file which you need to send')
    parser.add_argument('-d', '--directory', type=str, help='The directory with files which you need to send')
    parser.add_argument('-l',
                        '--link',
                        type=str,
                        help='Your shrarepoint site, like https://xxxx.sharepoint.com',
                        required=True)
    parser.add_argument(
        '-t',
        '--timeout',
        type=int,
        help=
        f'Connection timeout, usually need to increase on big files (default: {DEFAULT_CONNECTION_TIMEOUT_S} seconds)',
        required=False,
        default=DEFAULT_CONNECTION_TIMEOUT_S)
    try:
        args = parser.parse_args()
    except:
        sys.exit(os.EX_SOFTWARE)
    log.info(DESCRIPTION)
    files_to_send: List[Path] = []
    if args.file:
        file = Path(args.file)
        if file.exists():
            files_to_send.append(file)
        else:
            log.error(f'File: {file} is not exist')
            sys.exit(os.EX_SOFTWARE)
    elif args.directory:
        directory = Path(args.directory)
        if directory.exists():
            files_to_send = [f for f in directory.iterdir() if f.is_file()]
        else:
            log.error(f'Directory: {directory} is not exist')
            sys.exit(os.EX_SOFTWARE)

        log.info(f"{Clr.CYAN}List of sending files{Clr.RESET}")
        log.info("-" * 10)
        for f in files_to_send:
            log.info(f.name)
        log.info("-" * 10)
    for f in files_to_send:
        if shareup.file_upload(username=args.user,
                               password=args.password,
                               file_to_load=f,
                               public_group=args.group,
                               path=args.remote,
                               fileraw=bytes(),
                               sharesite=args.link,
                               timeout=args.timeout):
            log.info(f"File: {f} uploading: {Clr.GREEN}SUCCESSFULLY{Clr.RESET}")
        else:
            log.error(f"File: {f} {Clr.GREEN}NOT SENT{Clr.RESET}")
            sys.exit(os.EX_SOFTWARE)


if __name__ == "__main__":
    main()
