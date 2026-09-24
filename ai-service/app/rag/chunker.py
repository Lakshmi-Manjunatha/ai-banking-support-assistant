def load_chunks(fileText: str, chunk_size: int,
                chunk_overlap: int) -> list[str]:
    chunks = []
    start = 0

    while start < len(fileText):
        end = min(start + chunk_size, len(fileText))

        chunk = fileText[start:end]
        chunks.append(chunk)

        if end == len(fileText):
            break

        start = end - chunk_overlap

    return chunks
