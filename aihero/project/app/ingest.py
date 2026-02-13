import io
import json
import zipfile
import requests
import frontmatter
from minsearch import Index


def read_repo_data(repo_owner, repo_name, branch='main'):
    url = f'https://codeload.github.com/{repo_owner}/{repo_name}/zip/refs/heads/{branch}'
    resp = requests.get(url)
    repository_data = []
    zf = zipfile.ZipFile(io.BytesIO(resp.content))

    for file_info in zf.infolist():
        filename = file_info.filename.lower()

        if filename.endswith('.md') or filename.endswith('.mdx'):
            with zf.open(file_info) as f_in:
                content = f_in.read()
                post = frontmatter.loads(content)
                data = post.to_dict()
                _, filename_repo = file_info.filename.split('/', maxsplit=1)
                data['filename'] = filename_repo
                repository_data.append(data)

        elif filename.endswith('.ipynb'):
            with zf.open(file_info) as f_in:
                nb = json.loads(f_in.read())
                text = ''
                for cell in nb.get('cells', []):
                    source = ''.join(cell.get('source', []))
                    text += source + '\n\n'
                _, filename_repo = file_info.filename.split('/', maxsplit=1)
                data = {'content': text, 'filename': filename_repo}
                repository_data.append(data)

        elif filename.endswith('.rst'):
            with zf.open(file_info) as f_in:
                content = f_in.read().decode('utf-8', errors='ignore')
                _, filename_repo = file_info.filename.split('/', maxsplit=1)
                data = {'content': content, 'filename': filename_repo}
                repository_data.append(data)

    zf.close()
    return repository_data


def sliding_window(seq, size, step):
    if size <= 0 or step <= 0:
        raise ValueError("size and step must be positive")
    
    n = len(seq)
    result = []
    for i in range(0, n, step):
        batch = seq[i:i+size]
        result.append({'start': i, 'content': batch})
        if i + size > n:
            break
    return result


def chunk_documents(docs, size=2000, step=1000):
    chunks = []
    for doc in docs:
        doc_copy = doc.copy()
        doc_content = doc_copy.pop('content')
        doc_chunks = sliding_window(doc_content, size=size, step=step)
        for chunk in doc_chunks:
            chunk.update(doc_copy)
        chunks.extend(doc_chunks)
    return chunks


def index_data(repos, chunk=False, chunking_params=None):
    all_docs = []
    for repo_owner, repo_name, branch in repos:
        docs = read_repo_data(repo_owner, repo_name, branch=branch)
        all_docs.extend(docs)

    if chunk:
        if chunking_params is None:
            chunking_params = {'size': 2000, 'step': 1000}
        all_docs = chunk_documents(all_docs, **chunking_params)

    index = Index(text_fields=["content", "filename"])
    index.fit(all_docs)
    return index
