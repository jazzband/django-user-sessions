from netaddr import IPSet

from mmdb_writer import MMDBWriter


city_writer = MMDBWriter()

city_writer.insert_network(
    IPSet(["44.55.66.77/32"]),
    {
        "city": {
            "names": {
                "en": "San Diego",
            },
        },
        "continent": {
            "code": "NA",
            "names": {
                "en": "North America",
            },
        },
        "country": {
            "iso_code": "US",
            "names": {
                "en": "United States",
            },
        },
        "is_in_european_union": False,
        "location": {
            "latitude": 37.751,
            "longitude": -97.822,
            "metro_code": "custom metro code",
            "time_zone": "America/Los Angeles",
        },
        "postal": {
            "code": "custom postal code",
        },
        "subdivisions": [
            {
                "iso_code": "ABC",
                "names": {
                    "en": 'Absolute Basic Class',
                },
            },
        ],
    },
)

city_writer.to_db_file("tests/test_city.mmdb")

# country_writer = MMDBWriter(
#     IPSet(["8.8.8.8/32"]),
#     {
#         "country": {
#             "iso_code": "US",
#             "names": {
#                 "en": "United States",
#             },
#         },
#     },
# )

# country_writer.to_db_file("tests/test_country.mmdb")
