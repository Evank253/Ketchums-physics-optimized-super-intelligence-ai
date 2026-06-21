from setuptools import setup, find_packages

setup(
    name="ketchum-physics-intelligence",
    version="2.0.0",
    description="Ketchum's Physics Optimized Super Intelligence — 15 physics engines on classical hardware",
    author="Ketchum",
    packages=find_packages(),
    python_requires=">=3.10",
    install_requires=[
        "numpy>=1.24.0",
        "psutil>=5.9.0",
    ],
    extras_require={
        "dev": ["pytest>=7.0", "pytest-asyncio>=0.21"],
    },
)
