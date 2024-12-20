#!/bin/bash
mkdir -p ~/.streamlit/
echo "\
[server]\n\
headless = true\n\
port = $PORT\n\
enableCORS = false\n\
\n\
" > ~/.streamlit/config.toml
pip install -r requirements.txt
streamlit run Qualcomm_Stock.py  # Replace with your app's filename