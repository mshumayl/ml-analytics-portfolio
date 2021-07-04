# Data on Malaysia COVID-19 (coronavirus) vaccinations 

All data are collected from [JKJAV Social Media](https://www.facebook.com/jkjavmy/photos) and updated daily. 

## Population Data

The [population data](https://github.com/khvmaths/Malaysia-Vaccination-Progress/blob/main/Malaysia_Population_18yo.csv) are calculated from the daily registration infographic percentage, and rounded to the nearest number.

## Registered Data

The [registered data](https://github.com/khvmaths/Malaysia-Vaccination-Progress/blob/main/Registered.csv) consists of daily registered data, starting 7 March 2021. 

## Vaccination Data

The [vaccination data](https://github.com/khvmaths/Malaysia-Vaccination-Progress/blob/main/Vaccination.csv) consists of daily vaccination data, starting 3 March 2021. Every states has two column, namely `dose1_<state>` and `dose2_<state>`, representing the number of citizen who received one or two doses respectively.

## GeoJSON file

The [GeoJSON](https://github.com/khvmaths/Malaysia-Vaccination-Progress/blob/main/Malaysia.geojson) file consists of every states' boundary. There is one special key in `properties`, named `short`, which represents the short name used in the registered and vaccination data to represent every state. The short and real name is shown below.

| `short` | State Name |
| :---: | :---: |
| `perlis` | Perlis |
| `kedah` | Kedah |
| `penang` | Penang |
| `perak` | Perak |
| `selangor` | Selangor |
| `kl` | Federal Territory of Kuala Lumpur |
| `putrajaya` | Federal Territory of Putrajaya |
| `ns` | Negeri Sembilan |
| `melaka` | Melaka |
| `kelantan` | Kelantan |
| `terengganu` | Terengganu |
| `pahang` | Pahang |
| `johor` | Johor |
| `sabah` | Sabah |
| `labuan` | Federal Territory of Labuan |
| `sarawak` | Sarawak |

---

This **Malaysian Vaccination Progress Dataset** is made available under the Public Domain Dedication and License v1.0 whose full text can be found at: http://opendatacommons.org/licenses/pddl/1.0/
