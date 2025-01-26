# Installation

To install the framework locally, run the following bash script in `Python3`.

=== "git"

    ``` bash
    git clone https://github.com/tonamatos/FerGroup.git
    ```
=== "pip"

    !!! failure "Not implemented yet."

A `requirements.txt` file is not provided but one can quickly be generated and then executed by running the following bash script from within the project relative path. The flag `#!bash --ignore venv` can be added for virtual enviroments.

``` bash
pip install pipreqs
pipreqs . --force
pip install requirements.txt
```

The database of precomputed Fer group generators can be accessed with the following bash script or downloaded manually from [this URL](https://drive.google.com/file/d/1D8tSlJNjp3q9ghrYdePF0Xui86J0MYZe/view) and placed in `\databases\`.

``` bash
mkdir -p databases
gdown --output ./databases/ 1D8tSlJNjp3q9ghrYdePF0Xui86J0MYZe
```
!!! info
    Access to the database is only necessary if using the cache functions to save on computation. Requirements will vary depending on the intended use.