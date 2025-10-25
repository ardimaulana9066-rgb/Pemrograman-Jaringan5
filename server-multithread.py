#!/usr/bin/env python3
"""
Server multithread sederhana (I/O-bound simulation).
Menangani setiap koneksi client di thread terpisah.
Default: host=127.0.0.1 port=5000
"""
import socket
import threading
import time
import argparse

def handle_client(conn, addr, processing_time):
    thread_name = threading.current_thread().name
    try:
        data = conn.recv(1024).decode().strip()
        if not data:
            return
        print(f"[{thread_name}] Received from {addr}: {data}")
        # Simulasi kerja (I/O atau pemrosesan)
        time.sleep(processing_time)
        resp = f"Processed '{data}' by {thread_name}\n"
        conn.sendall(resp.encode())
        print(f"[{thread_name}] Responded to {addr}")
    except Exception as e:
        print(f"[{thread_name}] Error handling {addr}: {e}")
    finally:
        conn.close()

def run_server(host, port, processing_time):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((host, port))
        s.listen(50)
        print(f"[multi-server] Listening on {host}:{port}")
        try:
            while True:
                conn, addr = s.accept()
                t = threading.Thread(target=handle_client, args=(conn, addr, processing_time), daemon=True)
                t.start()
        except KeyboardInterrupt:
            print("\n[multi-server] Shutting down")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Multithread server")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=5000)
    parser.add_argument("--delay", type=float, default=1.0, help="Simulated processing time (seconds)")
    args = parser.parse_args()
    run_server(args.host, args.port, args.delay)
