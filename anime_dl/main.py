import os
import math
import wget
import argparse
from colorama import init, Fore, Style, deinit

from anime_dl.scraper import dllink_scraper


def get_download_path():
    """Returns the default downloads path for linux or windows"""
    if os.name == 'nt':
        import winreg
        sub_key = r'SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders'
        downloads_guid = '{374DE290-123F-4565-9164-39C4925E467B}'
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, sub_key) as key:
            location = winreg.QueryValueEx(key, downloads_guid)[0]
        return location
    else:
        return os.path.join(os.path.expanduser('~'), 'Downloads')


def bar_custom(current, total, width=40):
    width = 40
    avail_dots = width-2
    shaded_dots = int(math.floor(float(current) / total * avail_dots))
    return f'Downloading: {int(math.floor(current / total * 100))}% ' + Fore.BLUE + '▓'*shaded_dots + '░'*(avail_dots-shaded_dots) + Fore.RESET + f' [{current/1000000:.2f} / {total/1000000:.2f}] MB'


def main():
    init()
    sc = dllink_scraper()
    parser = argparse.ArgumentParser(description='A simple command-line tool to download anime.',
                                     prog='anime_dl', formatter_class=lambda prog: argparse.HelpFormatter(prog, max_help_position=40))
    parser.add_argument("-s", "--search", dest="keyword", required=True,
                        help="search for an anime", type=str)

    args, unknown = parser.parse_known_args()

    kw = args.keyword + ' ' + ' '.join(unknown)
    links = sc.search(kw)
    index = int(input(Style.BRIGHT + Fore.RED +
                      'Enter your selection: ' + Fore.RESET + Style.RESET_ALL))
    name = links[index-1].split("/")[-1]
    eps = input(Style.BRIGHT + Fore.RED + 'Enter episode no. or range(ex: 1-5)' +
                Fore.RESET + Style.RESET_ALL + '(* for all): ')
    epl = eps.split("-")
    if epl[0] == '*':
        eplinks = sc.get_eplinks(links[index - 1])

    else:
        epr = int(epl[0]), int(epl[1]) if len(epl) == 2 else int(epl[0])
        eplinks = sc.get_eplinks(links[index - 1], epr, dlall=False)

    des = os.path.join(os.sep, get_download_path(), name)
    try:
        os.mkdir(des)
    except Exception as e:
        pass

    print(Style.BRIGHT + Fore.GREEN + '\nDownload started.' +
          Fore.RESET + Style.RESET_ALL)
    for link in eplinks:
        lsplit = link.split('-')
        epname = f'{name}-episode-{lsplit[-1]}.mp4'
        dllink = sc.get_dllink(link)
        print(f'\n{epname}')
        wget.download(dllink, os.path.join(
            os.sep, des, epname), bar=bar_custom)

    print(f'\nDownload completed at location {des}')
    deinit()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
