import pandas as pd   
from duckduckgo_search import DDGS 

search_query = 'balkonphotovoltaikanlage'

results = DDGS().videos(
    keywords = search_query,
    region= 'wt-wt',
    safesearch= 'off',
    timelimit='7d',
    max_results=50      
)


print(results)
results_df = pd.DataFrame(results)
results_df.to_csv('datei.csv', index=False)

