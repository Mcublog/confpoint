#!/usr/bin/env python

import argparse
import logging
import os
import sys
import time
from dataclasses import dataclass

import markdown
import requests
from atlassian import Confluence
from colorama import Fore as Clr

import confpoint.utils as utils
from confpoint.image_tag import ImageTag
from confpoint.version import VERSION

logging.basicConfig(level=logging.INFO)
log = logging.getLogger("push")

WATERAMARK = "\n*This page created by* **[ConfPoint©](https://github.com/Mcublog/confpoint)** *script*"
DESCRIPTION = f'{Clr.GREEN}The Confluence {Clr.YELLOW}publisher{Clr.GREEN} for submitting or deleting pages v{VERSION}{Clr.RESET}'

@dataclass
class ConfSession:
    confluence: Confluence
    space: str
    title: str
    page_id: str


def convert_to_html(filename: str = "CHANGELOG.MD",
                    watermark: str = "",
                    watermark_default: bool = True) -> str:
    global WATERAMARK
    lines = ""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            lines = f.read()
    except Exception as _:
        log.error(f"file {filename} was not found")
        return ""
    if watermark_default:
        lines += WATERAMARK
    elif watermark:
        lines += watermark
    lines = markdown.markdown(lines,
                              extensions=[
                                  'markdown.extensions.fenced_code',
                                  'markdown.extensions.tables'
                              ])
    return lines


def attach_images(session: ConfSession, tags: tuple[ImageTag]):
    for t in tags:
        session.confluence.attach_file(filename=str(t.file.absolute()),
                                       name=t.file.name,
                                       content_type=None,
                                       page_id=session.page_id,
                                       comment=None)
        log.info(f'attached file: {t.file.name}')


def push(session: ConfSession, html_page: str, parent_title: str = "") -> int:
    parent_id = None
    try:
        session.page_id = session.confluence.get_page_id(space=session.space, title=session.title)
    except requests.HTTPError as e:
        log.error(e)
        return os.EX_SOFTWARE

    if session.page_id:
        log.info(f"Page id: {session.page_id}")
        try:
            session.confluence.update_page(parent_id=parent_id,
                                           page_id=session.page_id,
                                           title=session.title,
                                           body=html_page)
        except Exception as e:
            log.error(e)
            return os.EX_SOFTWARE
        return os.EX_OK

    if parent_title:
        parent_id = session.confluence.get_page_id(space=session.space,
                                                   title=parent_title)
        if parent_id is None:
            log.error(
                f"Parent page not found -- check it name: {parent_title}")
            return os.EX_SOFTWARE
    try:
        log.info(f"Try to create page: {session.space} | {session.title}")
        session.confluence.create_page(space=session.space,
                                       parent_id=parent_id,
                                       title=session.title,
                                       body=html_page)
        log.info("Page create successfully")
    except requests.HTTPError as e:
        log.error(e)
        return os.EX_SOFTWARE
    try:
        session.page_id = session.confluence.get_page_id(space=session.space, title=session.title)
    except Exception as e:
        log.error(e)
        return os.EX_SOFTWARE

    return os.EX_OK


def remove(username, token: str, space: str, title: str, url: str):
    confluence = Confluence(url=url,
                            username=username,
                            password=token,
                            cloud=True)
    try:
        page_id = confluence.get_page_id(space=space, title=title)
        if not page_id is None:
            confluence.remove_page(page_id, status=None, recursive=False)
            log.info(
                f"Page in space: {space} with title: {title} -- has been removed"
            )
        else:
            log.info(
                f"Page in space: {space} with title: {title} -- does not exist"
            )
    except requests.HTTPError as e:
        log.error(e)
        return os.EX_SOFTWARE


def main():
    parser = argparse.ArgumentParser(prog='push', description=DESCRIPTION)
    parser.add_argument('-u',
                        '--user',
                        type=str,
                        help='User name in Confluence (usually mail address)',
                        required=True)
    parser.add_argument('-a',
                        '--apikey',
                        type=str,
                        help='Your API key, check README.MD',
                        required=True)
    parser.add_argument('-s',
                        '--space',
                        type=str,
                        help='Space name in Confluence (Some like OBLT)',
                        required=True)
    parser.add_argument(
        '-p',
        '--parent',
        type=str,
        help='Parent page title, non required if you want to remove page',
        default=None)
    parser.add_argument(
        '-t',
        '--title',
        type=str,
        help='Title of the page which you are getting to publish or update',
        required=False,
        default=None)
    parser.add_argument('-f',
                        '--file',
                        type=str,
                        help='The file which content you need to send')
    parser.add_argument(
        '-r',
        '--remove',
        help='Removing page from Confluence with help space and title',
        action='store_true',
        default=False)
    parser.add_argument('-l',
                        '--link',
                        type=str,
                        help='Link to atlassian site',
                        required=True)
    parser.add_argument('-w',
                        '--watermark',
                        type=str,
                        help='Watermark in below of published page',
                        required=False)
    parser.add_argument('-wd',
                        '--watermark_default',
                        help='Using default watermark',
                        action="store_true",
                        required=False,
                        default=False)
    try:
        args = parser.parse_args()
    except Exception as e:
        print(e)
        sys.exit(os.EX_SOFTWARE)

    log.info(DESCRIPTION)
    if args.remove:
        remove(username=args.user,
               token=args.apikey,
               space=args.space,
               title=args.title,
               url=args.link)
        sys.exit(os.EX_SOFTWARE)
    page = convert_to_html(filename=args.file,
                           watermark=args.watermark,
                           watermark_default=args.watermark_default)
    if not page:
        log.warning("Page is empty -- nothing to send")
        sys.exit(os.EX_SOFTWARE)
    if not args.title:
        log.warning("Title is empty, check it")
        sys.exit(os.EX_SOFTWARE)

    session = ConfSession(confluence=Confluence(url=args.link,
                                                username=args.user,
                                                password=args.apikey,
                                                cloud=True),
                          space=args.space,
                          title=args.title,
                          page_id="")

    tags = utils.get_image_tags(page)
    page = utils.replace_imgage_tag_for_confluence(page, tags)
    if (ret := push(session=session, html_page=page, parent_title=args.parent)) != 0:
        sys.exit(ret)

    if not tags:
        sys.exit(ret)

    try:
        attach_images(session=session, tags=tags)
    except Exception as e:
        log.error(e)
        sys.exit(os.EX_SOFTWARE)

    sys.exit(ret)

if __name__ == "__main__":
    main()
