# Food Queue Time Study
![Static Badge](https://img.shields.io/badge/Python-3.12-gray?style=for-the-badge&logo=python&logoColor=white&labelColor=%233671a2) ![Static Badge](https://img.shields.io/badge/Nix-24.11-gray?style=for-the-badge&logo=nixos&logoColor=white&labelColor=%237eb7e1) ![Static Badge](https://img.shields.io/badge/License-MIT%2FApache-gray?style=for-the-badge&logo=gitbook&logoColor=white&labelColor=blue)

## Setup
Enter the developement shell on the provided flake.

You'l need to grab the files needed for the pre-trained models:
```bash
cd models
curl -lO https://github.com/patrick013/Object-Detection---Yolov3/raw/refs/heads/master/model/yolov3.weights
curl -lO https://raw.githubusercontent.com/pjreddie/darknet/refs/heads/master/cfg/yolov3.cfg
curl -lO https://raw.githubusercontent.com/pjreddie/darknet/refs/heads/master/data/coco.names
```

## Run
The project can be run with the following command:
```bash
python src/main.py
```
