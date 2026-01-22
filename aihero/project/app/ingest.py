"""
Data Ingestion Module - Day 1-2 Concepts
Handles downloading, processing, and chunking of GitHub repository data
"""

import io
import zipfile
import requests
import frontmatter
from minsearch import Index


def read_repo_data(repo_owner: str, repo_name: str, branch: str = 'main'):
    """
    Download and parse all markdown files from a GitHub repository.

    Args:
        repo_owner: GitHub username or organization
        repo_name: Repository name
        branch: Branch name (default: 'main')

    Returns:
        List of dictionaries containing file content and metadata
    """
    url = f'https://codeload.github.com/{repo_owner}/{repo_name}/zip/refs/heads/{branch}'
    resp = requests.get(url, timeout=30)

    if resp.status_code != 200:
        raise Exception(f"Failed to download repository: {resp.status_code}")

    repository_data = []
    zf = zipfile.ZipFile(io.BytesIO(resp.content))

    for file_info in zf.infolist():
        filename = file_info.filename
        filename_lower = filename.lower()

        if not (filename_lower.endswith('.md') or filename_lower.endswith('.mdx')):
            continue

        try:
            with zf.open(file_info) as f_in:
                content = f_in.read().decode('utf-8', errors='ignore')
                post = frontmatter.loads(content)
                data = post.to_dict()

                # Strip the repo prefix from filename for cleaner references
                _, filename_repo = file_info.filename.split('/', maxsplit=1)
                data['filename'] = filename_repo
                repository_data.append(data)
        except Exception as e:
            print(f"Error processing {filename}: {e}")
            continue

    zf.close()
    return repository_data


def sliding_window(seq: str, size: int, step: int):
    """
    Split text into overlapping chunks using sliding window.

    Args:
        seq: Text to chunk
        size: Size of each chunk
        step: Step size between chunks

    Returns:
        List of dictionaries with chunk content and position
    """
    if size <= 0 or step <= 0:
        raise ValueError("size and step must be positive")

    n = len(seq)
    result = []
    for i in range(0, n, step):
        chunk = seq[i:i+size]
        result.append({'start': i, 'content': chunk})
        if i + size >= n:
            break

    return result


def chunk_documents(docs: list, size: int = 2000, step: int = 1000):
    """
    Chunk large documents into smaller pieces.

    Args:
        docs: List of document dictionaries
        size: Chunk size in characters
        step: Step size for sliding window

    Returns:
        List of chunked documents with preserved metadata
    """
    chunks = []

    for doc in docs:
        doc_copy = doc.copy()
        doc_content = doc_copy.pop('content')
        doc_chunks = sliding_window(doc_content, size=size, step=step)

        for chunk in doc_chunks:
            chunk.update(doc_copy)

        chunks.extend(doc_chunks)

    return chunks


def index_data(
    repo_owner: str,
    repo_name: str,
    filter_func=None,
    chunk: bool = False,
    chunking_params: dict = None,
    branch: str = 'main'
):
    """
    Download repository data and create a search index.

    Args:
        repo_owner: GitHub repository owner
        repo_name: GitHub repository name
        filter_func: Optional function to filter documents
        chunk: Whether to chunk large documents
        chunking_params: Parameters for chunking (size, step)
        branch: Git branch to download

    Returns:
        Configured minsearch Index
    """
    # Download repository data
    docs = read_repo_data(repo_owner, repo_name, branch)

    # Apply filter if provided
    if filter_func is not None:
        docs = [doc for doc in docs if filter_func(doc)]

    # Chunk documents if requested
    if chunk:
        if chunking_params is None:
            chunking_params = {'size': 2000, 'step': 1000}
        docs = chunk_documents(docs, **chunking_params)

    # Create and fit the index
    index = Index(
        text_fields=["content", "filename", "title"],
        keyword_fields=[]
    )

    index.fit(docs)
    return index
