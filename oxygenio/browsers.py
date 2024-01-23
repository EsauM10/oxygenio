from subprocess import Popen, PIPE


class Chrome:
    def __init__(self) -> None:
        self.path = 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe'

    def run(self, url: str):
        Popen(
            [self.path, f'--app={url}', '--disable-http-cache'], 
            stdout=PIPE, stderr=PIPE, stdin=PIPE
        )