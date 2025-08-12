import os
import sys

# Ensure backend package root is importable with precedence over repo root for backend tests
BACKEND_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
REPO_ROOT = os.path.abspath(os.path.join(BACKEND_ROOT, ".."))

# Put backend root first so `import app.*` resolves to backend/app
if BACKEND_ROOT in sys.path:
    sys.path.remove(BACKEND_ROOT)
sys.path.insert(0, BACKEND_ROOT)

# Keep repo root also available, but after backend root
if REPO_ROOT not in sys.path:
    sys.path.append(REPO_ROOT)