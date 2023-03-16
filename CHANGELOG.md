# Changelog

## V1.3.1.0

**2023-03-13**

#### Backend

- Added weekly and monthly stats for total of aircraft for a day, most flown aircraft during that week or month, and average activity.
- Day validation to ensure correct amount of days are queried from MongoDB.

#### Frontend

- Transitioned to SASS instead of vanilla CSS.
- Added pages instead of scrolling.
- Initial work on supporting stats added for the backend.

## V1.3.1.1

**2023-03-13**

#### Frontend

-Added date.ts which is used to EOW and EOM queries.

#### Misc

- Added stats.jsonc

## V1.3.1.2

**2023-03-13**

#### Frontend

-Finished support for EOW and EOM

#### Backend

-Updated formatting of EOM and EOW to allow for easier frontend intergration

## V1.3.2.0

#### Frontend

**2023-03-16**

-Completely refactored frontend to allow for better mobile support as well as a better maintainablity.

-Redid pagination.

#### Misc

-Updated package.json to depreciate the need to cd into client.

-Updated docs.
