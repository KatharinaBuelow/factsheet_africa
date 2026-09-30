# How to contribute

Before starting to edit the documentation create an environment to install you software

## Install conda and python

### Check if you have python
        
        python3 --version

If not, 
go to the official Python download page: https://www.python.org/downloads/macos/

Download the latest macOS installer.

Open the downloaded .pkg file. 

Follow the installer prompts and finish the setup.

Open Terminal and verify:

    python3 --version


### Check if you have conda:

    conda --version

Exact macOS steps for Miniforge.

Open Terminal and check your Mac type:
    
    uname -m

arm64 = Apple Silicon
x86_64 = Intel

Download the right installer from the official Miniforge releases page:
https://github.com/conda-forge/miniforge/releases
Choose one of these:

**Apple Silicon: Miniforge3-MacOSX-arm64.sh**

Intel: Miniforge3-MacOSX-x86_64.sh

In Terminal, go to your Downloads folder:
    
    cd ~/Downloads

Run the installer:

    bash Miniforge3-MacOSX-arm64.sh

Press Enter to scroll through the license, then type yes to accept.

Use the default install location unless you specifically want another one.

When it finishes, activate Conda:

    source ~/miniforge3/bin/activate

Initialize your shell:

    conda init

Close Terminal completely and reopen it.

Verify it worked:

    conda --version

## Create environment

    conda create --name documentation python==3.13

**documentation** is just an example, you can chose what ever you like.
Next you activate your environment and install mkdocs:

    conda activate documentation
  
    pip install mkdocs
  
    pip install mkdocs-material

now you can start and test with if everything works fine:

    mkdocs --version

If you like to look at your documentation,go to main directory, where the mkdocs.yml file is stored.

    mkdocs serve

Open http://127.0.0.1:8000/ in your browser.

Later if you like to publish the finished pages:

    mkdocs gh-deploy


## Structure of the documentation

In your home directory is the file which contains the document structure
    
    mkdocs.yml

if you change the name or directoryname of your *.md files, make sure, you also change it in mkdocs.yml

In this case we changed the design a little bit, so we need
    
    stylesheets/extra.css

All your individual directories and files need to be stored in the directory 
    
    docs
