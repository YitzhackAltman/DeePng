from enum import Enum


class ChunkType(Enum):
    IHDR = b'IHDR'
    IDAT = b'IDAT'
    IEND = b'IEND'
    pHYs = b'pHYs'
    iCCP = b'iCCP'
    cHRM = b'cHRM'


class PNG_Chunk:
    def __init__(self, chunkType: ChunkType, data: bytes):
        self.chunkType = chunkType
        self.chunkData = data
        self.chunkLength = len(data)

    def __str__(self):
        return f"{self.chunkType}"


class PNG_Format:
    def __init__(self):
        self._png_chunks = []

    def append_chunk(self, chunk: PNG_Chunk):
        self._png_chunks.append(chunk)


# PNG Sig  |  IHDR  |  IDAT  |   IEND
# IHDR
# Width
# Height

def validate_png_signature(file):
    expected_signature = b'\x89PNG\r\n\x1a\n'
    signature = file.read(len(expected_signature))
    return signature == expected_signature


def read_chunk(file) -> PNG_Chunk | None:
    chunk_size = file.read(4)
    if len(chunk_size) < 4:
        return None

    chunk_type = file.read(4)
    crc = file.read(4)

    if chunk_type in (ChunkType.IHDR.value, ChunkType.IDAT.value,
                      ChunkType.IEND.value, ChunkType.pHYs.value, ChunkType.iCCP.value, ChunkType.cHRM.value):
        total_size = int.from_bytes(chunk_size)
        data = file.read(total_size)
        return PNG_Chunk(ChunkType(chunk_type), data)
    return None


def png_file(file_path: str):
    format = PNG_Format()
    try:
        with open(file_path, 'rb') as f:
            assert (validate_png_signature(f))
            while True:
                chunk = read_chunk(f)
                if chunk is None:
                    print("Unsupported chunk")
                    break

                format.append_chunk(chunk)
                if chunk.chunkType == ChunkType.IEND:
                    break
    except FileNotFoundError:
        print("Could not find file {0}".format(file_path))
    except Exception as e:
        print(f"ERROR: {e}")

    for chunk in format._png_chunks:
        print(chunk)


if __name__ == '__main__':
    png_file('whatsapp.png')