import pandas as pd
from glob import glob

def load_subtitles_dataset(dataset_path):
  subtitles_path = glob(f"{dataset_path}/*.ass")
  scripts=[]
  episode_num=[]

  for path in subtitles_path:

    # read lines
    with open(path,"r") as file:
      lines = file.readlines()
      lines = lines[27:]
      lines = [",".join(line.split(",")[9:]) for line in lines]

    lines = [line.strip() for line in lines]
    script = " ".join(lines)

    episode = int(path.split("-")[-1].split(".")[0].strip())
    scripts.append(script)
    episode_num.append(episode)
  
  df = pd.DataFrame.from_dict({"episode":episode_num,"script":scripts})
  return df
  