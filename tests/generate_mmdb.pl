#!perl

use MaxMind::DB::Writer::Tree;

my %city_types = (
    city                 => 'map',
    code                 => 'utf8_string',
    continent            => 'map',
    country              => 'map',
    en                   => 'utf8_string',
    is_in_european_union => 'boolean',
    iso_code             => 'utf8_string',
    latitude             => 'double',
    location             => 'map',
    longitude            => 'double',
    metro_code           => 'utf8_string',
    names                => 'map',
    postal               => 'map',
    subdivisions         => ['array', 'map'],
    region               => 'utf8_string',
    time_zone            => 'utf8_string',
);

my $city_tree = MaxMind::DB::Writer::Tree->new(
    ip_version            => 6,
    record_size           => 24,
    database_type         => 'GeoLite2-City',
    languages             => ['en'],
    description           => { en => 'Test database of IP city data' },
    map_key_type_callback => sub { $city_types{ $_[0] } },
);

$city_tree->insert_network(
    '44.55.66.77/32',
    {
        city                 => { names => {en => 'San Diego'} },
        continent            => { code => 'NA', names => {en => 'North America'} },
        country              => { iso_code => 'US', names => {en => 'United States'} },
        is_in_european_union => false,
        location             => {
            latitude => 37.751,
            longitude => -97.822,
            metro_code => 'custom metro code',
            time_zone => 'America/Los Angeles',
        },
        postal               => { code => 'custom postal code' },
        subdivisions         => [
            { iso_code => 'ABC', names => {en => 'Absolute Basic Class'} },
        ],
    },
);

my $outfile = ($ENV{'DATA_DIR'} || '/data/') . ($ENV{'CITY_FILENAME'} || 'test_city.mmdb');
open my $fh, '>:raw', $outfile;
$city_tree->write_tree($fh);



my %country_types = (
    country  => 'map',
    iso_code => 'utf8_string',
    names    => 'map',
    en       => 'utf8_string',
);

my $country_tree = MaxMind::DB::Writer::Tree->new(
    ip_version            => 6,
    record_size           => 24,
    database_type         => 'GeoLite2-Country',
    languages             => ['en'],
    description           => { en => 'Test database of IP country data' },
    map_key_type_callback => sub { $country_types{ $_[0] } },
);

$country_tree->insert_network(
    '8.8.8.8/32',
    {
        country => {
            iso_code => 'US',
            names    => {
                en => 'United States',
            },
        },
    },
);

my $outfile = ($ENV{'DATA_DIR'} || '/data/') . ($ENV{'COUNTRY_FILENAME'} || 'test_country.mmdb');
open my $fh, '>:raw', $outfile;
$country_tree->write_tree($fh);
