choco install nodejs
refreshenv
poetry install
poetry run jupyter labextension install @krassowski/jupyterlab-lsp
poetry run jupyter labextension install @ryantam626/jupyterlab_code_formatter
poetry run jupyter serverextension enable --py jupyterlab_code_formatter
