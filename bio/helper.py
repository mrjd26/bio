

def fbuffer(f, size=10240):
  while True:
    chunk = f.read(size)
    if not chunk: break
    yield chunk
