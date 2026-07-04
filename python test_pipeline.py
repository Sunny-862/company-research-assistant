from services.serper_service import (
    find_official_website,
    research_company_search,
)

from services.crawler import crawl_website

from services.openrouter_service import analyze_company

from services.competitor_service import find_competitors


company_name = input("Enter company name: ")


print("\n[1/5] Finding official website...")

website = find_official_website(company_name)

if not website:
    raise RuntimeError(
        "Official website could not be found."
    )

print("Official Website:", website)


print("\n[2/5] Crawling company website...")

crawled_pages = crawl_website(website)

print(
    f"Successfully crawled {len(crawled_pages)} pages."
)


print("\n[3/5] Collecting public research...")

search_results = research_company_search(
    company_name
)

print(
    f"Collected {len(search_results)} search results."
)


print("\n[4/5] Generating AI analysis...")

analysis = analyze_company(
    company_name=company_name,
    website=website,
    crawled_pages=crawled_pages,
    search_results=search_results,
)


print("\n[5/5] Finding competitors...")

competitors = find_competitors(
    company_name=analysis["company_name"],
    company_website=analysis["website"],
    industry=analysis["industry"],
    country=analysis["country"],
    products_services=analysis["products_services"],
)

print(
    f"Found {len(competitors)} competitors."
)


print("\nCOMPANY ANALYSIS\n")

for key, value in analysis.items():

    print(f"{key}: {value}")


print("\nCOMPETITORS\n")

for competitor in competitors:

    print(
        "Company:",
        competitor["company_name"],
    )

    print(
        "Website:",
        competitor["website"],
    )

    print("-" * 60)