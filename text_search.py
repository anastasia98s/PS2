import pandas as pd   
from duckduckgo_search import DDGS 


def search_web(keyword):
    search_query = keyword

    results = DDGS().text(
        keywords = search_query,
        region= 'wt-wt',
        safesearch= 'off',
        timelimit='7d',
        max_results=50       
    )


    results_df = pd.DataFrame(results)
    results_df.to_csv('datei.csv', index=False)
    return results

results= search_web('wetter heute berlin')
print(results)