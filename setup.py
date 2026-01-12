from setuptools import setup, find_packages

setup(
    name="AIS_annotator_project",
    version="0.1.0",
    description="AIS annotator and audio processing utilities",
    packages=find_packages(),  # Automatically find all packages in the directory
    install_requires=[
        "pandas",
        "tqdm",
        "numba",
        "pydub",
        "lifewatch-pypam",
        "matplotlib",
        "xarray",
        "numpy",
    ],
    python_requires='>=3.7',
)
