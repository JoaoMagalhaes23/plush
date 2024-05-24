#!/bin/bash

docker build . -t plush:latest
docker run -it --rm -v $(pwd)/compiler:/compiler -w /compiler plush:latest # plush $@