import wget
import requests
from tqdm import tqdm
import json
from pathlib import Path
import multiprocessing as mp
from joblib import Parallel, delayed, parallel_backend
import re

#pip install wget


class Downloader(object):
  def __init__(self, metaurl):
    self.datajson = json.load(open(wget.download(url=metaurl, out="datajson.json"),"rb"))['distribution']
  
  @staticmethod
  def writefile(target, r):
    with open(target, "wb") as f:
      status = f.write(r.content)
    return status
  
  @staticmethod
  def writereport(data):
    with open("report.json","w") as f:
      json.dump(data,f)
  
  @staticmethod
  def writevideo(video, override = False):
    url = video['contentUrl']
    name = video['name']
    status = contentSize = video['contentSize']
    r = requests.get(url, allow_redirects=True)
    content_length = int(r.headers.get('content-length'))

    acv,acn = Downloader.get_activity_action(name)
    target  = f"egok360/{acv}/{acn}/{name}"

    if override or (not Path(target).exists()):
      status = Downloader.writefile(target, r)
    if not status == contentSize == content_length:
      video.update({'status':'fail'})
    else:
      video.update({"status":"success"})
    return video
  
  @staticmethod
  def getdirs(videolist):
    dirpaths  = []
    for d in tqdm(videolist):
      acv, acn = Downloader.get_activity_action(d['name'])
      pths = f"egok360/{acv}/{acn}"
      if pths not in dirpaths:
        dirpaths.append(pths)
    return dirpaths
    
  @staticmethod
  def makedirs(dirpaths):
    for dirpath in dirpaths:  
      Path(dirpath).mkdir(parents=True, exist_ok=True)
  
  @staticmethod
  def get_activity_action(v):
    v = v.partition("-")[-1][::-1].partition("-")[-1][::-1]
    indices = [m.start(0) for m in re.finditer(r"\b-\b", v)]  
    activity, action = v[:indices[len(indices)//2]], v[indices[len(indices)//2]+1:]
    return activity, action

  def __call__(self, chunks = 100, override = False):
    results = []
    dirpaths = Downloader.getdirs(self.datajson)
    print("FOLDER CREATED")
    Downloader.makedirs(dirpaths)
    data = [self.datajson[i*chunks:i*(chunks+1)] for i in range(len(self.datajson)//chunks + 1)]
    print("")
    print("#"*20)
    print("DOWNLOAD STARTED")
    for d in tqdm(data):
      with parallel_backend("loky", inner_max_num_threads=mp.cpu_count()):
        results.extend(Parallel(n_jobs=mp.cpu_count()*2)(delayed(self.writevideo)(vid, override) for vid in d))
    self.writereport(results)
    return results

if __name__ == "__main__":
  D = Downloader(metaurl="https://dataverse.tdl.org/api/datasets/export?exporter=schema.org&persistentId=doi%3A10.18738/T8/L64SHD")
  # If you want to override please use override = True
  D()
