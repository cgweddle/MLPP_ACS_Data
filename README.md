# README

## Data
Data is taken from the csnsu.gov API
ACCS5 data from 2019

## Variables Chosen
I chose to look at variables that break people down by gender according to the block groups. I also have variables that specify thhe place of birth of the respondants. Included in this data is information for the number of respondants that answered the question for both questions. Having the full population that answered the question allows us to get percentage for both of these groups.

Knowing where people are born gives us information about the immigrant population in an area at the block level. We can use this information to know where immigrants coming into the US are living, and what proportion of each area are immigrants. It can also tell us where people who move into a state choose to live. This can tell us where the desirable neighborhoods to live in are. 

Knowing which of the total population is male and female can tell us if there is any difference as to where men and women choose to live. This can be combined with other attributes to tell us what their different preferences are. At the block level, we can combine this with the immigrant information to tell us if there are more immigrants of a certain gender.


## API Call
`variables`: list of variables names, of type  `String`

get: String of variable names for the API call

API call: get `get` string, specify the state, for all counties, at the block group level

## Data Cleaning
I clean this data by getting the variable names associated with the variable identifiers with API calls to the census.gov API. These names are used as the columns of the table instead of the numerical identifiers.

## Place into Database
The program loops through every list in the API output, and places the data in a new row in the database.

