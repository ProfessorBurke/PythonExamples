#!/bin/bash

pyinstaller --onefile --clean --windowed --icon="tangram.ico" --add-data="large_triangle.png:." --add-data="large_triangle_shadow.png:." --add-data="rabbit_background.png:." --add-data="square.png:." --add-data="square_shadow.png:." tangram.py 2>&1 | tee build.log