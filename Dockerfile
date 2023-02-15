FROM prefecthq/prefect:latest-python3.8

# Linux dependencies
RUN apt-get update && apt-get install -y git

# Prefect extras for Dask on Kubernetes
RUN pip install "prefect[kubernetes]==1.*"

# base Python dependencies for DPT
RUN pip install python-dotenv lxml requests loguru validify pandas

# additional Python dependencies for providerspecific scripts
RUN pip install fuzzywuzzy python-Levenshtein langcodes[data] openpyxl Pillow

# clone DPT Core Git repository
RUN git clone https://github.com/olivergoetze/dpt-core.git dpt_core