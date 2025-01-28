# AudioLens
Simple flask server that uses wavesurfer.js to do quality checks on annotations

## Installation
Install Flask and Javascript

## Usage
You can set username and password for authentication in `main.py`

In the populate_data function in main.py, you need to configure the following:

1. `audio_root_dir`:
This is the path where all the audio data and corresponding reference text files are stored. Inside this directory:

Each subdirectory represents a single data sample.
Each subdirectory contains:
audio.mp3: A recording of the sample.
ref_text.txt: A text file containing the transcription of the audio.mp3 recording.

Example structure:

```
audio_root_dir/
├── 176542/           
│   ├── audio.mp3     
│   └── ref_text.txt  
```
2. `annotated_data_dir`:
This is the path where all the annotation files (in JSON format) are stored. Each JSON file contains manually annotated data corresponding to a subdirectory in audio_root_dir.

## Naming Convention:

The name of the annotation JSON file must match the name of the subdirectory in `audio_root_dir`.
For example, if you have a subdirectory named 176542 in `audio_root_dir`, the corresponding annotation file in `annotated_data_dir` must be named 176542.json.

Example structure:
```
annotated_data_dir/  
├── 176542.json  
```


Next, Run:

```
python main.py
```

Visit `http://127.0.0.1:30110` to open the app. 





