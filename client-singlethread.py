#!/usr/bin/env python3
"""
Client untuk mencoba server single-thread.
Client tetap melakukan 10 request secara bersamaan (concurrent), server akan memproses satu-per-satu.
Default target host=127.0.0.1 port=5001
"""
import socket
import threading
import time
import argparse

def worker(i, host, port, results, timeout=10.0):
    start = time.time()
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(timeout)
            s.connect((host, port))
            msg = f"request-{i}\n"
            s.sendall(msg.encode())
            data = s.recv(1024).decode().strip()
            elapsed = time.time() - start
            results[i] = (True, data, elapsed)
    except Exception as e:
        elapsed = time.time() - start
        results[i] = (False, str(e), elapsed)

def run_client(host, port, concurrency=10):
    threads = []
    results = [None] * concurrency
    start_all = time.time()
    for i in range(concurrency):
        t = threading.Thread(target=worker, args=(i, host, port, results))
        t.start()
        threads.append(t)
    for t in threads:
        t.join()
    total = time.time() - start_all
    print(f"\n[client-single] Total time for {concurrency} requests: {total:.3f}s")
    for i, r in enumerate(results):
        ok, info, elapsed = r
        status = "OK" if ok else "ERR"
        print(f"  [{i}] {status} - time={elapsed:.3f}s - resp={info}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Client to test single-thread server (10 concurrent requests)")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=5001)
    parser.add_argument("--n", type=int, default=10, help="Number of concurrent requests")
    args = parser.parse_args()
    run_client(args.host, args.port, args.n)
