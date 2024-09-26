FROM prefecthq/prefect:3.0.1-python3.11

# Linux dependencies
RUN apt-get update && apt-get install -y git

# Prefect extras for Dask on Kubernetes
RUN pip install s3fs prefect-dask

# base Python dependencies for DPT
RUN pip install python-dotenv lxml requests loguru validify pandas pygtail

# additional Python dependencies for providerspecific scripts
RUN pip install fuzzywuzzy python-Levenshtein langcodes[data] openpyxl Pillow

# clone DPT Core Git repository
RUN mkdir /opt/prefect_flow_run_data
RUN mkdir -p /opt/prefect_flow_run_data/handle_transformation/dpt_core
RUN git clone https://github.com/olivergoetze/dpt-core.git /opt/prefect_flow_run_data/handle_transformation/dpt_core

RUN mkdir /.prefect
RUN chgrp -R 0 /.prefect && \
         chmod -R g=u /.prefect

RUN chgrp -R 0 /opt && \
         chmod -R g=u /opt

USER 1001