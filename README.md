![py31016](https://img.shields.io/badge/python-3.10.16-brightgreen.svg)

# AudioLens
Simple flask server that uses wavesurfer.js to visualize and check for quality of annotations of your audio data. The interface looks like the image shown below. 
![Sample Image](data/image.png)
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
   ```

5. **Run the Server**:
   ```bash
   python main.py
   ```

## Data Directory Setup
Set `audio_root_dir` in the `.env` file. The structure of the `audio_root_dir` should look like this:

- This is the path where all the audio data, corresponding reference text and annotation files are stored. Inside this directory:
- Each subdirectory represents a single data sample.
- Each subdirectory contains: 
   - `audio.mp3`: A recording of the sample.
   - `ref_text.txt`: (optional) A text file containing the reference text of the audio.mp3 recording. This is relevant for audios captured in a read aloud setting where the speaker is given a text to read.
   - `annotation.json`: A json file containing annotations corresponding to the `audio.mp3` recording.

Example structure:

```
audio_root_dir/
├── sample_1/
│   ├── audio.mp3
│   └── ref_text.txt
│   └── annotation.json
```
