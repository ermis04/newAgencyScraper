from bs4 import BeautifulSoup
import pandas as pd
import requests

# The base URL
main_link = "https://www.shopify.com/partners/directory/plus?sort=AVERAGE_RATING&page="
all_links = []

# #%% get all the agency links
for i in range(1, 2):
    url = main_link + str(i)
    # Request the page
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")

        # Find all <a> tags with the specific class
        a_tags = soup.find_all("a",
                               class_="w-full pt-4 pr-6 pb-4 pl-4 bg-transparent grid xs:grid-cols-[80px_1fr] md:grid-cols-[91px_1fr] grid-rows-[auto_auto]")

        # Extract and store the href attributes
        page_links = [a["href"] for a in a_tags if "href" in a.attrs]
        print(page_links)
        for link in page_links:
            link = "https://www.shopify.com" + link
            all_links.append(link)
        print(all_links)
    else:
        print(f"Failed to fetch the page. Status code: {response.status_code}")


#%% Get data for each agency

# Initialize the dataframe
df = pd.DataFrame(columns=['Name', 'email', 'Country'])

name_class="richtext text-t4"
email_class="hover:underline focus:underline"
country_class = "flex flex-col gap-y-1"

for link in all_links:
    try:
        page = requests.get(link)
        soup = BeautifulSoup(page.content, 'html.parser')

        name = soup.find(class_=name_class)
        email = soup.find_all(class_=email_class)
        country_dirty = soup.find_all(class_=country_class)

        name = name.get_text().lstrip().rstrip()


        email = email[-1].get_text().lstrip().rstrip()

        country = ""
        for cc in country_dirty:
            if "Primary location" in cc.get_text():
                country = cc.get_text()[16:] # 16 is the length of "Primary location: "

        df.loc[len(df)] = [name, email, country]

        print('\n--------------\n', df)
    except Exception as e:
        print(f"Error: {str(e)}")

#%% Save the data to a CSV file

print("Saving the data to a CSV file...")
df.to_csv("shopify_agencies.csv", index=False)