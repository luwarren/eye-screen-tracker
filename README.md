# Eye + Screen Tracker, Pupilometry


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
python3 pip install -r requirements.txt
```
*This will only need to be completed once, on the initialisaton of this repository on a new device.*

### Usage Instructions
```python
source venv/bin/activate
python3 app.py
```
The above will need to be completed on each new instance of usage.



## Output Requirements

Before running the program ensure that a `raw_videos` & `processed_videos` directory has been created in the main project directory.

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
