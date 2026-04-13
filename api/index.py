import sys
import os

# Add parent directory to path so we can import app.py
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, parent_dir)

# Change working directory to parent so Flask finds templates/static
os.chdir(parent_dir)

# Env vars are set in Vercel dashboard — no secrets hardcoded here

from app import app

# Fix template and static paths for Vercel environment
app.template_folder = os.path.join(parent_dir, 'templates')
app.static_folder = os.path.join(parent_dir, 'static')

# Vercel expects the WSGI app
app = app
