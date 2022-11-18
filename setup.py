import setuptools


setuptools.setup(
    name="CloverHacker", 
    version="0.0.1",
    install_requires=[
        "numpy",
    ],
    entry_points={
        'console_scripts': [
            'CloverHacker=CloverHacker:main',
        ],
    },
    author="kazulagi",
    description="Controller of CloverTech M-A352",
    url="https://github.com/kazulagi/CloverHacker",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)