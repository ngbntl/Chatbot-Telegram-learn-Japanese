import os
import sys

# Thêm đường dẫn src vào sys.path
sys.path.append(os.path.join(os.path.dirname(__file__), "src"))

# Import từ src/app.py
import asyncio
from src.app import main

if __name__ == "__main__":
    asyncio.run(main())