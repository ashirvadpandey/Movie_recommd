mkdir -p ~/.streamlit/credentials.toml

echo "\
[server]\n\
port = $PORT\N\
enableCORS = false\n\
headless = true\n\
\n\
" > ~/.streamlit/config.toml
