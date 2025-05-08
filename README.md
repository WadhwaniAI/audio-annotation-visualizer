![py3919](https://img.shields.io/badge/python-3.9.19-brightgreen.svg)

# AudioLens
Simple flask server that uses wavesurfer.js to do quality checks on annotations

## Setup

1. **Clone the Repository**:
   Clone the repository to your local machine using the following command:
   ```bash
   git clone https://github.com/WadhwaniAI/AudioLens.git
   cd AudioLens
   ```

2. **Create and activate a Conda Environment**:
   Run the following command to create a conda environment named `audiolens` using Python 3.10:
   ```bash
   conda create -n audiolens python=3.10
   ```
   ```bash
   conda activate audiolens
   ```

3. **Install Dependencies**:
   Use the `requirements.txt` file to install all necessary dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set Environment Variables**:
   Copy the `.env.example` file to `.env` and set the following environment variables:
   ```bash
   USERNAME=<username>
   PASSWORD=<password>
   AUDIO_ROOT_DIR=<path_to_audio_data>
   ANNOTATED_DATA_DIR=<path_to_annotated_data>
   ```

5. **Run the Server**:
   ```bash
   python main.py
   ```

## Usage
You can set username and password for authentication in `main.py`

In the populate_data function in main.py, you need to configure the following:

1. `audio_root_dir`:
This is the path where all the audio data and corresponding reference text files are stored. Inside this directory:

Each subdirectory represents a single data sample.
Each subdirectory contains: 

`audio.mp3`: A recording of the sample.
`ref_text.txt`: A text file containing the transcription of the audio.mp3 recording.

Example structure:

```
audio_root_dir/
├── sample_1/           
│   ├── audio.mp3     
│   └── ref_text.txt  
```
2. `annotated_data_dir`:
This is the path where all the annotation files (in JSON format) are stored. Each JSON file contains manually annotated data corresponding to a subdirectory in audio_root_dir.

## Naming Convention:

The name of the annotation JSON file must match the name of the subdirectory in `audio_root_dir`.
For example, if you have a subdirectory named `sample_1` in `audio_root_dir`, the corresponding annotation file in `annotated_data_dir` must be named `sample_1.json`.

Example structure:
```
annotated_data_dir/  
├── sample_1.json  
```


Next, Run:

```
python main.py
```

Visit `http://127.0.0.1:30110` to open the app. 





