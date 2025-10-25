#!/usr/bin/env python3
"""
Server single-thread sederhana.
Menerima koneksi dan memprosesnya secara sekuensial (tidak membuat thread baru).
Default: host=127.0.0.1 port=5001
"""
import socket
import time
import argparse

def handle_client(conn, addr, processing_time):
    try:
        data = conn.recv(1024).decode().strip()
        if not data:
            return
        print(f"[single-server] Received from {addr}: {data}")
        time.sleep(processing_time)
        resp = f"Processed '{data}' (single-thread)\n"
        conn.sendall(resp.encode())
        print(f"[single-server] Responded to {addr}")
    except Exception as e:
        print(f"[single-server] Error handling {addr}: {e}")
    finally:
        conn.close()

def run_server(host, port, processing_time):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((host, port))
        s.listen(50)
        print(f"[single-server] Listening on {host}:{port}")
        try:
            while True:
                conn, addr = s.accept()
                # Proses secara langsung (blocking) -> server single-thread
                handle_client(conn, addr, processing_time)
        except KeyboardInterrupt:
            print("\n[single-server] Shutting down")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Single-thread server")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=5001)
    parser.add_argument("--delay", type=float, default=1.0, help="Simulated processing time (seconds)")
    args = parser.parse_args()
    run_server(args.host, args.port, args.delay)
