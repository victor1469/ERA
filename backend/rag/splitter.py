def split_text(
    text,
    chunk_size=500,
    overlap=100
):
    """
    文本切分

    chunk_size:
        每个chunk长度

    overlap:
        重叠长度
    """

    chunks = []

    start = 0

    text_length = len(text)


    while start < text_length:

        end = start + chunk_size

        chunk = text[start:end]


        chunks.append(chunk)


        start = end - overlap


    return chunks