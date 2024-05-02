from transformers import pipeline
import pandas as pd
from tqdm.notebook import tqdm

tqdm.pandas()
pipe = pipeline("text2text-generation", model="ilsilfverskiold/tech-keywords-extractor")


def add_keywords(df, logging=False) -> pd.DataFrame:
    """
    Add keywords to DataFrame
    :param df: DataFrame with papers
    :return: DataFrame with keywords added
    """
    df['title_abstract'] = df['title'] + ' ' + df['abstract'][:400]
    df['title_abstract'] = df['title_abstract'].astype(str)
    try:
        if logging:
            df['keywords'] = df['title_abstract'].progress_apply(
                lambda x: pipe(x)[0]['generated_text'].lower().split(', '))
        else:
            df['keywords'] = df['title_abstract'].apply(lambda x: pipe(x)[0]['generated_text'].lower().split(', '))
    except:
        df['keywords'] = []
        if logging:
            print('Error in extracting keywords')

    df.drop('title_abstract', axis=1, inplace=True)
    return df
