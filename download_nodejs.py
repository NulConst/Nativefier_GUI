from rich.console import Console
from noneprompt import CancelledError, ListPrompt, Choice

console = Console()
import requests
with console.status("Getting the latest NodeJS version......") as status:
    version_raw = requests.get(url="https://cdn.npmmirror.com/binaries/node/index.json")
    version = version_raw.json()
    #console.print(version[0])
    console.print(f"Version: {version[0]['version']}",style="bold green")
    choice_list = [Choice("win-x86.zip"),Choice("win-x64.zip")]
try:
    bit = ListPrompt("64bit or 32bit", choices=choice_list).prompt()
except CancelledError:
    exit()
#rich_downloader.download(f"https://cdn.npmmirror.com/binaries/node/{version[0]['version']}/node-{version[0]['version']}-{bit.name}","./temp")