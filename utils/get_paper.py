import requests
import pandas as pd


def get_papers_to_keyword(keyword: str, max_papers=-1, min_citation_count=50, sort_by_reference=True, logging=False) -> pd.DataFrame:
    """
    Get papers from CrossRef API based on keyword
    :param min_citation_count: minimum number of citations
    :param sort_by_reference:  whether to sort by number of references
    :param keyword: keyword to search for
    :param max_papers: maximum number of papers to return
    :param logging: whether to print progress
    :return: DataFrame with papers
    """
    base = 'https://api.crossref.org/works'
    cursor = '*'
    papers = []
    num_rows = max_papers if -1 < max_papers < 1000 else 1000
    num_rows_returned = num_rows

    if logging:
        print(f'Querying for {keyword}...')
    while (num_rows_returned == num_rows) and (len(papers) < max_papers or max_papers == -1):
        params = {
            'query': keyword,
            # 'facet': 'published:*',
            'select': 'title,author,is-referenced-by-count,created,abstract,DOI',
            'filter': 'type:journal-article',
            'rows': num_rows,
            'cursor': cursor
        }
        if sort_by_reference:
            params['sort'] = 'is-referenced-by-count'
            params['order'] = 'desc'

        response = requests.get(base, params=params)
        data = response.json()
        papers.extend(data['message']['items'])
        num_rows_returned = len(data['message']['items'])
        if logging:
            print(
                f'\tNumber of papers found: {len(papers)},\tcitation count (last): {papers[-1]["is-referenced-by-count"]}')
        cursor = data['message']['next-cursor']

        if papers[-1]["is-referenced-by-count"] < min_citation_count:
            if logging:
                print('Citation count below 50, stopping...')
            break
        if len(papers) >= max_papers > 0:
            if logging:
                print(f'Maximum number of papers reached ({max_papers}), stopping...')
            break
    df = pd.DataFrame(papers)

    # cleaning up DataFrame
    df['title'] = df['title'].str[0]

    # filtering if keyword is longer than 1 word
    if len(keyword.split()) > 1:
        df = df[df['title'].str.contains(keyword, case=False) | df['abstract'].str.contains(keyword, case=False)]

    # continue cleaning up DataFrame
    df['abstract'] = df['abstract'].fillna('')
    df = df.dropna(subset=['title'])
    df['found_by_keyword'] = keyword

    if logging:
        print(f'Done! Found {len(df)} papers.')
    return df
