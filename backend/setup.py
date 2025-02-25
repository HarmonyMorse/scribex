from setuptools import setup, find_packages

setup(
    name="scribex-api",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "fastapi",
        "uvicorn",
        "sqlalchemy",
        "pydantic",
        "pydantic-settings",
        "pytest",
        "pytest-asyncio",
        "httpx",
    ],
) 