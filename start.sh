#!/bin/bash
pyenv activate cilibox-venv
uvicorn shifty.main:app --reload