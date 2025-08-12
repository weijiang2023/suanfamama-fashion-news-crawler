import os
import sys

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
BACKEND_ROOT = os.path.join(REPO_ROOT, "backend")

# Ensure repo root is present and ahead of backend root for resolving `app`
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

if BACKEND_ROOT in sys.path:
    # If backend is before repo root, move it after
    try:
        repo_idx = sys.path.index(REPO_ROOT)
        backend_idx = sys.path.index(BACKEND_ROOT)
        if backend_idx < repo_idx:
            sys.path.pop(backend_idx)
            sys.path.insert(repo_idx + 1, BACKEND_ROOT)
    except ValueError:
        pass