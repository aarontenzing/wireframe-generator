# Generating wireframes
- A tool capable of generating wireframe images on a large scale, and saving their annotations
*Purpose: Wireframes can then be used to generate controlled stable diffusion images*

<p align="left" width="100%">
<img src="example.jpg">
</p>

# How to run this tool?
    This tool was created using Python 3.11.2
    1. pip install -r requirements.txt
    2. python generator.py 
  
# Controls
There are two ways of using this tool:
1. manual mode press "y"
2. automatic mode press "n"

## Manual Controls
- Enter: Generates a new wireframe with a different height, depth, and width.
- Right-arrow-key: Randomly rotates/translates the current wireframe, takes a screenshot, and writes annotations to a JSON file.
- Key a: Enables drawing the axis.
- Key s: Enables taking screenshots.

## Automatic Controls
- Specify the number of wireframes you want to generate.
- Define how screenshots should be taken for these wireframes in different positions.
