from setuptools import setup, find_packages

setup(
    name="cura-framework",
    version="0.1.0",
    description="CURA: Code Understanding & Reasoning Agent framework",
    author="Mark Chen",
    author_email="mark@mindifyai.dev",
    packages=find_packages(),
    install_requires=[
        "requests",
        "pydantic",
        "typing-extensions",
        "bigcodebench",
        "langgraph",
        "fire",
        "tqdm",
        "dotenv"
    ],
    entry_points={
        "console_scripts": [
            "cura-cli=cli:main"
        ]
    },
    python_requires=">=3.9",
    include_package_data=True,
    zip_safe=False,
)
