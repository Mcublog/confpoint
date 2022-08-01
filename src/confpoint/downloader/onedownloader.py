import argparse
import logging
import os
import sys
from pathlib import Path

import confpoint.shareup as shareup
from colorama import Fore as Clr
from confpoint.version import VERSION

logging.basicConfig(level=logging.INFO)
log = logging.getLogger("onedownloader")

DESCRIPTION = f'{Clr.GREEN}The SharePoint {Clr.YELLOW}downloader{Clr.GREEN} v{VERSION}{Clr.RESET}'

def download_file(args):
    try:
        outputdir: Path = Path(args.outputdir)
    except:
        log.error(f"Uncorrect path to downloading dir {args.outputdir}")
        sys.exit(os.EX_SOFTWARE)
    log.info(f"{Clr.CYAN}Downloading...{Clr.RESET}")
    log.info(f"file: {args.file}")
    log.info(f"group: {args.group}")
    log.info(f"remote path: {args.remote}")
    log.info(f"download directory: {outputdir}")
    log.info(f"{Clr.CYAN}{'-' * 10}{Clr.RESET}")
    if shareup.file_download(username=args.user,
                                password=args.password,
                                outpath=outputdir,
                                remote_folder=args.remote,
                                file_to_download=args.file,
                                public_group=args.group,
                                sharesite=args.link):
        log.info(f"Downloading: {Clr.GREEN}SUCCESSFULLY{Clr.RESET}")
        return os.EX_OK
    log.error(f"Downloading: {Clr.RED}FAILED{Clr.RESET}")
    return os.EX_SOFTWARE


def download_from_directory(args):
    try:
        outputdir: Path = Path(args.outputdir)
    except:
        log.error(f"Uncorrect path to downloading dir {args.outputdir}")
        sys.exit(os.EX_SOFTWARE)
    log.info(f"{Clr.CYAN}Downloading from directory{Clr.RESET}")
    log.info(f"group: {args.group}")
    log.info(f"remote path: {args.remote}")
    log.info(f"download directory: {outputdir}")
    log.info(f"downloading recursive: {Clr.CYAN}{args.recursive}{Clr.RESET}")
    log.info(f"{Clr.CYAN}{'-' * 10}{Clr.RESET}")
    if shareup.dowload_directory(username=args.user,
                                    password=args.password,
                                    outpath=outputdir,
                                    remote_folder=args.remote,
                                    recursive=args.recursive,
                                    public_group=args.group,
                                    sharesite=args.link):
        log.info(f"Downloading: {Clr.GREEN}SUCCESSFULLY{Clr.RESET}")
        return os.EX_OK
    log.error(f"Downloading: {Clr.RED}FAILED{Clr.RESET}")
    return os.EX_SOFTWARE


def main():
    parser = argparse.ArgumentParser(prog='downloader', description=DESCRIPTION)
    parser.add_argument('-u', '--user', type=str, help='User name (usually mail address)', required=True)
    parser.add_argument('-p',
                        '--password',
                        type=str,
                        help='Your password for downloding file from the OneDrive',
                        required=True)
    parser.add_argument('-r', '--remote', type=str, help='OneDrive path like: Projects/BMS3', required=True)
    parser.add_argument('-g',
                        '--group',
                        type=str,
                        help='OneDrive shared group, root directory for all documents and files',
                        required=True)
    parser.add_argument('-f',
                        '--file',
                        type=str,
                        help=f'The file which you need to download.' +
                        f'{Clr.YELLOW} If not use, then will be download all content from remote path{Clr.RESET}',
                        required=False)
    parser.add_argument('-o', '--outputdir', type=str, help='Output directory with downloaded content')
    parser.add_argument("--recursive",
                        action='store_true',
                        help='Recursive downloading content from the OneDrive directory')
    parser.add_argument('-l',
                        '--link',
                        type=str,
                        help='Your shrarepoint site, like https://xxxx.sharepoint.com',
                        required=True)
    log.info(DESCRIPTION)
    try:
        args = parser.parse_args()
    except:
        sys.exit(os.EX_SOFTWARE)
    sys.exit(download_file(args) if args.file else download_from_directory(args))

if __name__ == "__main__":
    main()
