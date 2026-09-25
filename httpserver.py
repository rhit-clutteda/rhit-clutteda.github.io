import socket
import time
import signal
import traceback
import os

BINARY_FILETYPES = {".png"  : "image/png",
                    ".jpeg" : "image/jpeg",
                    ".jpg" : "image/jpeg",
                    ".ico"  : "image/x-icon",
}
TEXT_FILETYPES = {".html"   : "text/html; charset=utf-8",
                  ".css"    : "text/css; charset=utf-8",
                   ".js"    : "text/javascript; charset=utf-8",
}

def get_requested_filename(request):
    words = request.split(" ")
    return "./" + words[1]

def get_file_type(file):
    # split string around (last) period, then add period back
    return "." + file.rpartition(".")[2]

def get_content_type(file):
    type = get_file_type(file)
    if type in BINARY_FILETYPES:
        return BINARY_FILETYPES[type]
    if type in TEXT_FILETYPES:
        return TEXT_FILETYPES[type]
    return "UNKOWN"

def load_content(filename):
    filetype = get_file_type(filename)
    file_contents = None
    if filetype in TEXT_FILETYPES:
        with open(filename, encoding="utf-8") as f:
            file_contents = f.read().encode("utf-8")
    elif filetype in BINARY_FILETYPES:
        with open(filename, "rb") as f:
            file_contents = f.read()
    else:
        print("UNKOWN FILETYPE: " + filetype)
    return file_contents

def main():

    server = create_connection(port = 8080)

    while True:
        # 1. Wait for the browser to send a HTTP Request
        connection_to_browser = accept_browser_connection_to(server)

        # 2. Read the HTTP Request from the browser
        reader_from_browser = connection_to_browser.makefile(mode='rb')
        try:
            request_line = reader_from_browser.readline().decode("utf-8") # decode converts from bytes to text
            request_file = get_requested_filename(request_line)
            print()
            print('Request:')
            print(request_line)
            print("Request file:")
            print(request_file)
        except Exception as e:
            print("Error while reading HTTP Request:", e)
            traceback.print_exc() # Print what line the server crashed on.
            shutdown_connection(connection_to_browser)
            continue

        # Check for shutdown
        if request_file == "./public/shutdown":
            print("SHUTTING DOWN!")
            shutdown_connection(connection_to_browser)
            quit()
        
        # 3. Write the HTTP Response back to the browser
        writer_to_browser = connection_to_browser.makefile(mode='wb')
        try:

            content_type = get_content_type(request_file)
            response_body = load_content(request_file)


            response_headers = "\r\n".join([
                'HTTP/1.1 200 OK',
                f'Content-Type: {content_type}',
                f'Content-length: {len(response_body)}',
                'Connection: close',
                '\r\n'
            ]).encode("utf-8") # encode converts strings to raw bytes

            # These lines just PRINT the HTTP Response to your Terminal.
            print()
            print('Response headers:')
            print(response_headers)
            print()
            #print('Response body:')
            #print(response_body)
            #print()

            # These lines do the real work; they WRITE the HTTP Response to the Browser.
            writer_to_browser.write(response_headers)
            writer_to_browser.write(response_body)
            writer_to_browser.flush()
        except Exception as e:
            print("Error while writing HTTP Response:", e)
            traceback.print_exc() # print what line the server crashed on
    
        shutdown_connection(connection_to_browser)



# Don't worry about the details of the rest of the code below.
# It is VERY low-level code for creating the underlying connection to the browser.

def create_connection(port):
    addr = ("", port)  # "" = all network adapters; usually what you want.
    server = socket.create_server(addr, family=socket.AF_INET6, dualstack_ipv6=True) # prevent rare IPV6 softlock on localhost connections
    server.settimeout(2)
    print(f'Server started on port {port}. Try: http://localhost:{port}/index.html')
    return server

def accept_browser_connection_to(server):
    while True:
        try:
            (conn, address) = server.accept()
            conn.settimeout(2)
            return conn
        except socket.timeout:
            print(".", end="", flush=True)
        except KeyboardInterrupt:
            exit(0)

def shutdown_connection(connection_to_browser):
    connection_to_browser.shutdown(socket.SHUT_RDWR)
    connection_to_browser.close()


if __name__ == "__main__":
    print()
    main()

print("TODO: replace httpserver.py with YOUR web server. Serve files from './public'")

