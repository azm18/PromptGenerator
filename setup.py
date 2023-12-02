from huggingface_hub import snapshot_download

download_path = snapshot_download(repo_id="intfloat/multilingual-e5-large", 
                                  local_dir="model-e5-large")

#download_path = snapshot_download(repo_id="intfloat/multilingual-e5-base", 
#                                  local_dir="model-e5-base")

#download_path = snapshot_download(repo_id="intfloat/multilingual-e5-small", 
#                                  local_dir="model-e5-small")