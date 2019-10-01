# googleflights
Google flights scraper

This script allows you to find the cheapest individiual roundtrip ticket from one airport to another - this includes price and itinerary. It also allows you to 1. specify your departing destination and 2. pull price/itinerary flight info based on a list of the faa's top US airports (https://www.faa.gov/airports/planning_capacity/passenger_allcargo_stats/passenger/). This webpage contains an xlsx file that, when 'Answer' variable = Yes, downloads to your local device. Once downloaded, the script looks at the index value variables, 'start_point' and 'end_point', and pulls those from the list of IATA airport codes contained in the xlsx file.

# Definitions of variables contained in the script:

Where do you want to go? These are you departing/arriving flight city parameter (Required)
# dep_city = ('San Francisco')
# arv_city = ('Denver') 

Do you want to choose the arrival destination based on the top US airports? Note: inputes required - 'yes' or 'no'. Inputtting 'no' will return the cheapest roundtrip flight for airports listed above

# Answer = ('yes')

If 'Answer' = yes, then choose your starting/ender points. For example, if you set start_point = 0 and end_point = 20, then you'll pull the top 21 airports by air traffic in 2017. Also, the main limitation here is that the max range of airports that can be scraped at once is: 55 airports. In short, the script will throw an error if the 'end_point' - 'start_point' exceeds a search of >55 airports

# start_point = 0
# end_point   = 50 

When do you want to leave? Departure/arrival flight date parameters (Required)
# dep_date = '7/11/2019'
# arv_date = '7/14/2019'

How many stops do you want to have? Put 0 for a non-stop flight search { 2 is the max number of stops }
# num_stops = '2'

For your departing flight, what time do you want to leave at? NOTE: Must be at least a 3 hour window! (Required)
# dep_leave_time_1 = '6:15AM'
# dep_leave_time_2  = '8:45pM'

Do you want to download your data?
# csv_file_download = 'Yes'

Is there a different airport displaying in the results? Change airport by adjusting the list index (0 is default). Note: you will see these IATA codes printed in the command line. This is a way to debug every time the script executes
# dep_IATA_index = '0'
# arv_IATA_index = '0'
