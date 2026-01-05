# Markdown Preview

Allow to create and preview markdown files directly in your editor.


## Requirements
uv>=0.9.21 and python>=3.10


## How to use

uv run markdown-preview --help
markdown-preview --help
mdp --help

You can convert in two ways:

1. Using terminal

```sh
uv sync

# 1
markdown-preview {file_path}

# 2
mdp {file_path}
```

```sh
uv tool install .
mdp
```


2. Using the browser

> Using this will allow you to process multiple files at once

```sh
uv sync

# 1
mdp --run-server

# 2
markdown-preview --run-server
```


3. Using playground version (WIP)

> Using this will allow you to process multiple files at once
