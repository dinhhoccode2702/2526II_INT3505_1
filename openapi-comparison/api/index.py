from server import app

# Vercel Python ("@vercel/python") will use the WSGI `app` object
# exported from this module. We simply import the Flask `app`
# defined in the repository root `server.py`.

# Ensure `server.py` does not call app.run() on import (it already is guarded)


# Export `app` for the builder
__all__ = ["app"]
