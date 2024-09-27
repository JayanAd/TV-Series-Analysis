import torch
import nltk
from transformers import pipeline
from nltk.tokenize import sent_tokenize
import numpy as np
import pandas as pd
import os
import sys
import pathlib

folder_path = pathlib.Path(__file__).parent.resolve()
sys.path.append(os.path.join((folder_path),"/.."))

from utils import load_subtitles_dataset
nltk.download("punkt")
nltk.download("punkt_tab")

class ThemeClassifier:
    def __init__(self,theme_list):
        self.model_name = "facebook/bart-large-mnli"
        self.device = 0 if torch.cuda.is_available() else "cpu"
        self.theme_list = theme_list
        self.theme_classifier = self.load_model(self.device)

    def load_model(self,device):
        theme_classifier = pipeline("zero-shot-classification",model=self.model_name,device=device)
        return theme_classifier
    
    def get_themes_inference(self,script):
        script_sentences = sent_tokenize(script)

        # Batch Sentence
        sentence_bath_size = 20
        script_batches = []

        for index in range(0,len(script_sentences),sentence_bath_size):
            sent = " ".join(script_sentences[index:index+sentence_bath_size])
            script_batches.append(sent)

        # Run Model
        theme_output = self.theme_classifier(
            script_batches[:2],
            # script_batches,
            self.theme_list,
            multi_label=True
            )
        
        # Wrangle Output
        themes = {}
        for output in theme_output:
            for label,score in zip(output["labels"],output["scores"]):
                if label not in themes:
                    themes[label] = []
            themes[label].append(score)

        themes = {key:np.mean(np.array(value)) for key,value in themes.items()}
        return themes
    
    def get_themes(self,dataset_path,save_path):
        # Read saved output if Exists

        if save_path is not None and os.path.exists(save_path):
            df = pd.read_csv(save_path)
            return df

        # load Dataset
        df = load_subtitles_dataset(dataset_path)

        # for test
        df = df.head(2)

        # Run Inference
        output_themes = df["script"].apply(self.get_themes_inference)

        themes_df = pd.DataFrame(output_themes.tolist())
        df[themes_df.columns] = themes_df

        # save output

        if save_path is not None:
            df.to_csv(save_path,index=False)

        return df