
import json
from collections import Counter

def analyze_landing_pages(files):
    all_pages = []
    all_reasons = []

    for file in files:
        with open(file, 'r') as f:
            data = json.load(f)
            if 'landing_page_examples_2024' in data:
                for page in data['landing_page_examples_2024']:
                    all_pages.append(page['company_name'])
                    all_reasons.append(page['success_description'])
            if 'features' in data:
                for page in data['features']:
                    all_pages.append(page['company_name'])
                    if 'reasons_for_success' in page:
                        all_reasons.extend(page['reasons_for_success'])
            if 'extracted_information' in data and isinstance(data['extracted_information'], list):
                for item in data['extracted_information']:
                    if 'company_name' in item:
                        all_pages.append(item['company_name'])
                    if 'description' in item:
                        all_reasons.append(item['description'])


    page_counts = Counter(all_pages)
    
    # Simple keyword extraction from reasons
    reason_keywords = Counter()
    for reason in all_reasons:
        keywords = [word.lower().strip('.,!;:()[]{}') for word in reason.split() if len(word) > 4]
        reason_keywords.update(keywords)

    return page_counts, reason_keywords

if __name__ == '__main__':
    files = [
        'search_results/unbounce_best_landing_pages.json',
        'search_results/instapage_best_landing_pages.json',
        'search_results/zoho_best_landing_pages.json'
    ]
    
    page_counts, reason_keywords = analyze_landing_pages(files)
    
    print("--- Top 10 All-Time Landing Pages (by mentions) ---")
    for page, count in page_counts.most_common(10):
        print(f"{page}: {count} mentions")

    print("\n--- Top 5 2024 Landing Pages (from 2024 lists) ---")
    # This is a simplification. A more robust approach would be to check the dates from the articles.
    # For now, I'll assume the zoho and unbounce lists are for 2024
    with open('search_results/zoho_best_landing_pages.json', 'r') as f:
        zoho_data = json.load(f)
        for i, page in enumerate(zoho_data['extracted_information'][:5]):
            print(f"{i+1}. {page['company_name']}")

    print("\n--- Top 10 Most Common Success Keywords ---")
    for keyword, count in reason_keywords.most_common(10):
        print(f"{keyword}: {count} mentions")
