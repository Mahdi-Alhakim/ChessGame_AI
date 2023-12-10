# Chess Game with Engine

This is a chess game created with python and tkinter, applying all the game mechanics. Additionally, an AI bot is implemented following the min-max algorithm with alpha-beta pruning.

#### Note: Possible Bugs after translating from python2.7 to python3

## Requirements:
- #### python 3.x
- #### Tkinter 8.6
- #### Pillow 10.10.0
- #### Thread6 0.2.0

## Setup:

1. Create a virtual environment using the latest release of virtualenv:

``` bash
> pip install virtualenv --upgrade
> virtualenv venv
```

_If there are problems with installing tkinter:_
- Install tkinter package. Ex: Homebrew:
``` bash
> brew install python-tk
```
- Then create the virtual environment as follows:
```
> virtualenv venv --system-site-packages
```

2. Access the virtual environment `./venv`
``` bash
> source ./venv/bin/activate
```

3. Install the requirements:
```bash
> pip install -r requirements.txt
```

## Execution:

#### _Choose whether to activate the AI bot or not in `./settings.json`:_

``` json
{
    "botOn": true
}
```

#### To run ther game, execute the following command:

``` bash
> python3 index.py
```
