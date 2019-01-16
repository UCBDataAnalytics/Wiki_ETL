Extract:

Titles of english wikipedia pages: https://dumps.wikimedia.org/enwiki/20181001/. A text file with list of titles (14M Records).
WikiPedia API to read info, pageviews info: https://en.wikipedia.org/wiki/Special:ApiSandbox#action=query&format=json&prop=info%7Cpageviews%7Ccategories&list=&meta=&titles=Albert_Einstein. The API returns a JSON data and we wrote that to a mongoDB.
Wikipedia page scraping to get the categories and table of contents on the page. The scraped data is written again into mongoDB.

Transform:

Read data from 3 mongodb collections, and loaded into their data frames.
Aggregate the total page views for the month of Dec, using the per day page views.
Filled null values on the views with 0’s. 
Merge the 3 dataframes into one by the column page_title.

Load:
Write the dataframe into a relational database MYSQL.
