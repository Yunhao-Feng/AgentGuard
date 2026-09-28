#!/usr/bin/env python3
"""Local static preview with byte ranges for video seeking. No dependencies.
Usage: python scripts/serve.py [--port 4173] [--directory .]
"""
import argparse, os, re
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

class Handler(SimpleHTTPRequestHandler):
    def send_head(self):
        self.byte_range = None
        path = self.translate_path(self.path)
        if not os.path.isfile(path) or not self.headers.get('Range'):
            return super().send_head()
        file = open(path, 'rb')
        stat = os.fstat(file.fileno()); size = stat.st_size
        match = re.fullmatch(r'bytes=(\d*)-(\d*)', self.headers['Range'].strip())
        try:
            if not match or not any(match.groups()): raise ValueError()
            first,last = match.groups()
            if first:
                start = int(first); end = min(int(last),size-1) if last else size-1
            else:
                count = int(last)
                if count <= 0: raise ValueError()
                start = max(0,size-count); end = size-1
            if start >= size or start < 0 or end < start: raise ValueError()
        except ValueError:
            file.close(); self.send_response(416)
            self.send_header('Content-Range',f'bytes */{size}'); self.send_header('Content-Length','0'); self.end_headers(); return None
        self.send_response(206)
        self.send_header('Content-type',self.guess_type(path))
        self.send_header('Content-Range',f'bytes {start}-{end}/{size}')
        self.send_header('Content-Length',str(end-start+1))
        self.send_header('Last-Modified',self.date_time_string(stat.st_mtime))
        self.end_headers();file.seek(start);self.byte_range=(start,end);return file

    def end_headers(self):
        self.send_header('Accept-Ranges','bytes')
        super().end_headers()

    def copyfile(self, source, outputfile):
        try:
            if self.byte_range is None:
                return super().copyfile(source,outputfile)
            remaining=self.byte_range[1]-self.byte_range[0]+1
            while remaining:
                chunk=source.read(min(65536,remaining))
                if not chunk:break
                outputfile.write(chunk);remaining-=len(chunk)
        except (BrokenPipeError,ConnectionResetError):
            pass  # Browsers routinely cancel preloads when seeking.

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--port',type=int,default=4173)
    p.add_argument('--directory',type=Path,default=Path(__file__).resolve().parents[1])
    a=p.parse_args()
    server=ThreadingHTTPServer(('127.0.0.1',a.port),partial(Handler,directory=str(a.directory.resolve())))
    print(f'Preview: http://127.0.0.1:{a.port}',flush=True)
    try:server.serve_forever()
    except KeyboardInterrupt:server.server_close()
