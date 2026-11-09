import subprocess, http.server, socketserver
subprocess.Popen(["python","train.py"])
class H(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        try: body=open("/tmp/log.txt",encoding="utf-8").read()[-30000:]
        except Exception: body="starting..."
        b=("<meta http-equiv=refresh content=15><pre>"+body.replace("<","&lt;")+"</pre>").encode()
        self.send_response(200); self.send_header("Content-Type","text/html; charset=utf-8"); self.end_headers(); self.wfile.write(b)
    def log_message(self,*a): pass
socketserver.TCPServer(("0.0.0.0",7860),H).serve_forever()
