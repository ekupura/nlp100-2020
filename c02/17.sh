#!/bin/bash

cut ./popular-names.txt -f 1 | sort | uniq
