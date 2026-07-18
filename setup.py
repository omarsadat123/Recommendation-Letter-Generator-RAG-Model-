from setuptools import find_packages, setup

setup(
    name="recommendation-letter-generator-rag",
    version="0.1.0",
    description="RAG-based recommendation letter generator",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    include_package_data=True,
    install_requires=[
        "faiss-cpu>=1.8.0",
        "numpy>=1.26.0",
        "requests>=2.32.0",
        "sentence-transformers>=3.0.0",
        "streamlit>=1.37.0",
    ],
    python_requires=">=3.10",
)
