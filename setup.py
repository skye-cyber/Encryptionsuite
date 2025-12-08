from setuptools import setup
from
DESCRIPTION = "CLI tool for encrypting and decrypting files and folders"
EXCLUDE_FROM_PACKAGES = ["build", "dist", "test", "src"]

setup(
    name="encryptionsuite",
    version="1.0.7",
    author="Wambua aka skye-cyber",
    email="swskye17@gmail.com",
    packages=["Encryptionsuite"],
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    entry_points={
        "console_scripts": [
            "Encryptionsuite=Encryptionsuite:main",
            "encryptionsuite=Encryptionsuite:main",
            "encryptor=Encryptionsuite:main",
        ],
    },
    python_requires=">=3.0",
    install_requires=["argparse", "cryptography"],
    include_package_data=True,
    license="GNU v3",
    keywords=[
        "Encryptionsuite",
        "FED",
        "File-encryptor",
        "File-decryptor",
        "encrypt-files",
        "decrypt-files",
        "encrypt",
        "decrypt",
        "cryptography",
        "ciphers",
    ],
    classifiers=[
        "Environment :: Console",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.11",
    ],
)
