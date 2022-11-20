# Steps to reproduce Identification
1. Get Bing Candidates.
Run: `python bing_results/bing_scrape.py` Outputs in `bing_results/bing_candidates.csv`
2. Get Google candidates `python google_results/google_scrape.py`
3. Filter Tranco List `python tranco_list/tranco_filter.py` Outputs in `tranco_list/tranco_candidates.csv`
4. List of sources from Cheng et. al. paper and Reaves et. al. are static csv files
5. Run `combine_sources.py`. Outputs into `combined_candidates.csv`
6. Run `labeling.py`. Outputs into `combined_labeled.csv`
7. Run `filter_labeled.py`. Outputs into `providers.csv`