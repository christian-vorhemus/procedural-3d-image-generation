# Procedural 3D Image Generation with Blender
This is a PoC repository demonstrating how Blender can be leveraged to create synthetic machine learning training data for computer vision tasks.

<img src="sample.png" width="800" />

## How To

### Prerequisites
Make sure the following sofftware installed on your computer:

- <a href="https://www.python.org/downloads/" target="_blank">Python</a> >= 3.6 (including pip)
- <a href="https://www.blender.org/download/">Blender</a> >= 2.83

Install python dependencies by opening up your command prompt or terminal and type in

  ```
  pip install -r requirements.txt
  ```

Next open open `pipeline.py` in a text editor and change the output path (`file_base_path`) and the number of images (`num_images`) that should be produced. NOTE: Rendering images can take time, start with 1 or 2 to see if the result meets your expectations.

### Run Pipeline

Run 
  ```
  python pipeline.py
  ```
  
 to start the pipeline. This will do the following:
 
 1) 
