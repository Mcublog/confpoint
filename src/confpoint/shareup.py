import logging
import os
import sys
from pathlib import Path
from typing import Any, Tuple, Union

from colorama import Fore as Clr
from shareplum import Office365, Site
from shareplum.site import Version, _Folder

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__.split('.')[-1])


def __error_msg(message) -> bool:
    log.error(f"{Clr.RED}{message}{Clr.RESET}")
    sys.exit(os.EX_SOFTWARE)


def __connect_to_site(username: str,
                      password: str,
                      path: str = "",
                      sharesite: str = "",
                      public_group: str = "") -> Tuple[bool, Any, Union[_Folder, Any]]:
    res, site, folder = True, None, None
    try:
        authcookie = Office365(sharesite, username=username, password=password).GetCookies()
        site: Any = Site(sharesite + public_group, authcookie=authcookie, version=Version.v2016)
        folder = site.Folder(path)
    except Exception as e:
        res = __error_msg(f"{e}")
    return (res, site, folder)


def __download_all_files_from_folder(folder: _Folder, outpath: Path):
    outpath.mkdir(parents=True, exist_ok=True)
    for number, file in enumerate(folder.files):
        filename = file["Name"]
        log.info(f'Downloading {number}: {Clr.YELLOW}{filename}{Clr.RESET}')
        with outpath.joinpath(filename).open("wb+") as f:
            f.write(folder.get_file(filename))


def file_upload(username: str,
                password: str,
                fileraw: bytes,
                file_to_load: Path,
                path: str = "",
                sharesite: str = "",
                public_group: str = "",
                filename: str = "",
                timeout:int = 15) -> bool:
    res, _, folder = __connect_to_site(username=username,
                                       password=password,
                                       path=path,
                                       public_group=public_group,
                                       sharesite=sharesite)
    if res is False:
        return False
    content = ''
    name: str = filename
    if fileraw:
        content = fileraw
    else:
        if file_to_load.exists() is False:
            log.error(f'{Clr.RED}Check filepath:{Clr.RESET} {file_to_load.absolute()}')
            return False
        with open(file_to_load, 'rb') as f:
            content = f.read()
        name = file_to_load.name
    log.info("Loading ...")
    folder.timeout = timeout
    folder.upload_file(content, name)
    return True


def file_download(username: str, password: str, outpath: Path, remote_folder: str, file_to_download: str,
                  sharesite: str, public_group: str) -> bool:
    res, _, folder = __connect_to_site(username=username,
                                       password=password,
                                       path=remote_folder,
                                       public_group=public_group,
                                       sharesite=sharesite)
    if res is False:
        return False
    outpath.mkdir(parents=True, exist_ok=True)
    with outpath.joinpath(file_to_download).open("wb+") as f:
        f.write(folder.get_file(file_to_download))
    return True


def dowload_directory(username: str, password: str, outpath: Path, remote_folder: str, recursive: bool, sharesite: str,
                      public_group: str) -> bool:
    res, site, folder = __connect_to_site(username=username,
                                          password=password,
                                          path=remote_folder,
                                          public_group=public_group,
                                          sharesite=sharesite)
    if res is False:
        return False
    __download_all_files_from_folder(folder, outpath)
    if recursive is False:
        return True
    for dir in folder.folders:
        log.info(f"Downloading from folder: {Clr.CYAN}{dir}{Clr.RESET}")
        try:
            __download_all_files_from_folder(site.Folder(f"{remote_folder}/{dir}"), outpath.joinpath(dir))
        except Exception as e:
            log.error(f"{Clr.RED}{e}{Clr.RESET}")
            sys.exit(os.EX_SOFTWARE)
    return True
