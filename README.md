[![PyPI Version](https://img.shields.io/pypi/v/Encryptionsuite)](https://pypi.org/project/Encryptionsuite)
[![License: GPL-3.0](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://opensource.org/licenses/GPL-3.0)
[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![Build Status](https://img.shields.io/github/actions/workflow/status/skye-cyber/Encryptionsuite/ci.yml?branch=main)](https://github.com/skye-cyber/Encryptionsuite/actions)

# Encryptionsuite (File Encryption and Decryption)
This is a CLI tool for encrypting and decrypting files and folders.
Be carefull on how you use, irresponsible use can lead user to turning their data into chunks
if encryption keys are miss-handled.
For every encrypte file an Encryption key used is save in filename.xml file
where filename is name of the input file to be encrypted.
## Name variations
```shell
   Encryptionsuite -h
   encryptionsuite -h
   ENCRYPTIONSUITE -h
```
## Installation

1. Install via pip:

   ```shell
   pip install Encryptionsuite
      ```
2. Install from github:

   ```shell
   pip install git+https://github.com/skye-cyber/Encryptionsuite.git
   ```


## Usage

To run the CLI app, use the following command:

 ```shell
   Encryptionsuite [options]
 ```

Replace `[options]` with the appropriate command-line options based on the functionality you want to execute.

## Available Options
`1`.``-m/--mode`` operation to be performed(encryption or Decryption) value ```[encrypt, decrypt]```

`2`.``-i/--input_file``

`3`.``-k/--key`` only when decrypting

## Examples

1. Example command 1:

   ```shell
   Encryptionsuite -m encrypt -i example.txt or ```FED --mode encrypt -input_file example.txt```
   ```
in this case the output file will be 'example.txt.encrypted'

2. Example command 2:
   ```shell
   Encryptionsuite -m decrypt -i example.txt.encrypted -k xxxx where xxxx is the encryption key used
   ```
2. Example command 3 using key file inplace of the key itself:
    ```shell
    Encryptionsuite -m decrypt -i example.txt.encrypted -k file where file is the file containing the key
    ```

## Contributing

Contributions are welcome! If you encounter any issues or have suggestions for improvements, please open an issue or submit a pull request.

## License

This project is an open source software Licensed under `GNU GENERAL PUBLIC LICENSE Version 3`


Feel free to modify and customize this template according to your specific project requirements and add any additional sections or information that you think would be helpful for users.



## Acknowledgements

[Shields.io](https://shields.io/) – Status badges 

GitHub’s README guidelines 
