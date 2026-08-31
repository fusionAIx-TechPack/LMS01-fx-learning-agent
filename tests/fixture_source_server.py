#!/usr/bin/env python3
from __future__ import annotations

import sys
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse


port_file = Path(sys.argv[1])
log_file = Path(sys.argv[2])


class Handler(BaseHTTPRequestHandler):
    def log_message(self, format: str, *args: object) -> None:
        return

    def _respond(self, include_body: bool) -> None:
        with log_file.open("a", encoding="utf-8") as log:
            log.write(f"{self.command} {self.path}\n")
        path = urlparse(self.path).path
        if (
            path.startswith("/sources/")
            or path.startswith("/videos/")
            or path.startswith("/paths/")
        ):
            status = 404 if path.endswith("/unavailable") else 200
            body = b"fixture source"
            self.send_response(status)
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            if include_body and status == 200:
                self.wfile.write(body)
            return
        self.send_response(404)
        self.end_headers()

    def do_HEAD(self) -> None:
        self._respond(False)

    def do_GET(self) -> None:
        self._respond(True)


server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
port_file.write_text(str(server.server_port), encoding="utf-8")
server.serve_forever()
