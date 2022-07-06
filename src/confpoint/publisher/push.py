import argparse
import logging
import os
import sys
from distutils.log import ERROR

import markdown
import requests
from atlassian import Confluence
from colorama import Fore as Clr
from confpoint.version import VERSION

logging.basicConfig(level=logging.INFO)
log = logging.getLogger("push")

WATERAMARK = "\n*This page created by* **[ConfPoint©](https://github.com/Mcublog/confpoint)** *script*"
DESCRIPTION =  f'{Clr.GREEN}The Confluence {Clr.YELLOW}publisher{Clr.GREEN} for submitting or deleting pages v{VERSION}{Clr.RESET}'

def convert_to_html(filename: str = "CHANGELOG.MD", watermark: str = "", watermark_default: bool = True) -> str:
    global WATERAMARK
    lines = ""
    try:
        with open(filename, 'r') as f:
            lines = f.read()
    except:
        log.error("file %s was not found" % filename)
        return ""
    if watermark_default:
        lines += WATERAMARK
    elif watermark:
        lines += watermark
    lines = markdown.markdown(lines, extensions=['markdown.extensions.fenced_code', 'markdown.extensions.tables'])
    return lines


def push(html_page: str, username, token: str, space: str, parent_title: str = "", title: str = "", url: str = ""):
    parent_id = None
    confluence = Confluence(url=url, username=username, password=token, cloud=True)
    try:
        page_id = confluence.get_page_id(space=space, title=title)
    except requests.HTTPError as e:
        log.error(e)
        return os.EX_SOFTWARE
    if parent_title:
        parent_id = confluence.get_page_id(space=space, title=parent_title)
        if parent_id == None:
            log.error("Parent page not found -- check it name: %s" % (parent_title))
            return os.EX_SOFTWARE
    try:
        log.info("Try to create page: %s | %s" % (space, title))
        confluence.create_page(space=space, parent_id=parent_id, title=title, body=html_page)
        log.info("Page create successfully")
    except requests.HTTPError as e:
        log.error(e)
        return os.EX_SOFTWARE
    if page_id != None:
        log.info("Page id: " + page_id)
        try:
            confluence.update_page(parent_id=parent_id, page_id=page_id, title=title, body=html_page)
        except Exception as e:
            log.error(e)
            return os.EX_SOFTWARE
        return os.EX_OK


def remove(username, token: str, space: str, title: str, url: str):
    confluence = Confluence(url=url, username=username, password=token, cloud=True)
    try:
        page_id = confluence.get_page_id(space=space, title=title)
        if page_id != None:
            confluence.remove_page(page_id, status=None, recursive=False)
            log.info("Page in space: %s with title: %s -- has been removed" % (space, title))
        else:
            log.info("Page in space: %s with title: %s -- does not exist" % (space, title))
    except requests.HTTPError as e:
        log.error(e)
        return os.EX_SOFTWARE


def main():
    parser = argparse.ArgumentParser(prog='push', description=DESCRIPTION)
    parser.add_argument('-u', '--user', type=str, help='User name in Confluence (usually mail address)', required=True)
    parser.add_argument('-a', '--apikey', type=str, help='Your API key, check README.MD', required=True)
    parser.add_argument('-s', '--space', type=str, help='Space name in Confluence (Some like OBLT)', required=True)
    parser.add_argument('-p',
                        '--parent',
                        type=str,
                        help='Parent page title, non required if you want to remove page',
                        default=None)
    parser.add_argument('-t',
                        '--title',
                        type=str,
                        help='Title of the page which you are getting to publish or update',
                        required=False,
                        default=None)
    parser.add_argument('-f', '--file', type=str, help='The file which content you need to send')
    parser.add_argument('-r',
                        '--remove',
                        help='Removing page from Confluence with help space and title',
                        action='store_true',
                        default=False)
    parser.add_argument('-l', '--link', type=str, help='Link to atlassian site', required=True)
    parser.add_argument('-w', '--watermark', type=str, help='Watermark in below of published page', required=False)
    parser.add_argument('-wd',
                        '--watermark_default',
                        help='Using default watermark',
                        action="store_true",
                        required=False,
                        default=False)
    try:
        args = parser.parse_args()
    except:
        sys.exit(os.EX_SOFTWARE)

    log.info(DESCRIPTION)
    if args.remove:
        remove(username=args.user, token=args.apikey, space=args.space, title=args.title, url=args.link)
        sys.exit(os.EX_SOFTWARE)
    page = convert_to_html(filename=args.file, watermark=args.watermark, watermark_default=args.watermark_default)
    if not page:
        log.warning("Page is empty -- nothing to send")
        sys.exit(os.EX_SOFTWARE)
    if not args.title:
        log.warning("Title is empty, check it")
        sys.exit(os.EX_SOFTWARE)
    ret = push(html_page=page,
         username=args.user,
         token=args.apikey,
         space=args.space,
         parent_title=args.parent,
         title=args.title,
         url=args.link)
    sys.exit(ret)


if __name__ == "__main__":
    main()
