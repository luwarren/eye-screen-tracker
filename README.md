# Eye + Screen Tracker, Pupilometry

This code is split into two parts.

1. `start_recording.sh` is a script that records the webcam and screen of the user's computer.
2. `predict.py` is Python code that analyses **cropped** eye videos and analyses the level of pupil dilation in relation to cognitive load.

This code was created for [Richard Holden](https://richardholden.org/) - a Professor of Economics at the UNSW Business School, as part of a larger project on analysing standardised testing.

## Requirements

- `ffmpeg` installed on your system for `start_recording.sh`.
- Python 3+ installed on your system and `venv` for `predict.py`.

### Initalisation Instructions
```console
brew install ffmpeg
mkdir raw_videos
```

```python
python3 -m venv venv
python3 pip install -r requirement.txt
```
*This will only need to be completed once, on the initialisaton of this repository on a new device.*

### Usage Instructions
```python
source venv/bin/activate
```
The above will need to be completed on each new instance of usage.


```console
./start_recording.sh
```
This will begin recording the screen and webcam - press CTRL + C to stop



```python
python3 predict.py model/meye-2022-01-24.h5 [VIDEO SOURCE]
```
This will analyse cropped eye videos and output to pupilometry.csv.


## Output Requirements

Before running the `./start_recording.sh` script, ensure that a `raw_videos` directory has been created in the main project directory. Within the `raw_videos` directory, each activation of `./start_recording.sh` will create a new timestamped instance.

Running `predict.py` will output two items
1. `predictions.mp4` - The mp4 provides a visual representation of how accurately the pupil was tracked, which can be used for sense-checking and preparing for model tweaking.

2. `pupilometry.csv` - The CSV file provides data on the size of the pupil, which can be used for further analysis. 



## Usage
The program is designed to be split into two for several reasons. 
1. Cropping of output video to ensure eye is in frame for better pupilometry analysis.
2. Usage of different and tweaked models to ensure more accurate pupilometry.
3. Quick recording of multiple videos for later analysis.

## Acknowledgements

- [Fabio Carrara](https://github.com/fabiocarrara), for creating the initial model.
