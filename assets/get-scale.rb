require 'countries'
require 'csv'

# Create or open a CSV file for writing
CSV.open("countries_scales.csv", "w") do |csv|
  # Write the header row
  csv << ["Country Code", "Min lng", "Max lng", "Min lat", "Max lat", "axis", "value"]

  # Iterate through all countries
  ISO3166::Country.all.each do |country|
    # Get the country code
    country_code = country.alpha2

    min_lo = country.min_longitude
    min_la = country.min_latitude
    max_lo = country.max_longitude
    max_la = country.max_latitude

    # average latitude to calculate lo difference (yue)
    avg_la = country.latitude
    # convert averate latitude (degree) to radius
    rad_la = (avg_la.abs * Math::PI) / (180)

    # calcuate border to border distance in kilometers
    lo_diff_km = 111.320*Math.cos(rad_la)*((max_lo-min_lo).abs) # Longitude: 1 deg = 111.320*cos(latitude radius) km
    la_diff_km = 110.574*((max_la-min_la).abs)

    # if a country crosses the day line at pacific side, the longitude needs to be calculated differently
    if min_lo > 0 and max_lo < 0
        lo_diff_km = 111.320*Math.cos(rad_la)*(180-min_lo+180+max_lo)
    end

    axis = "lat"
    value = la_diff_km

    # decide whether to use longitude or latitude as scale (decide whether country is wider or longer)
    if lo_diff_km > la_diff_km
        axis = "lng"
        value = lo_diff_km
    end

    # Write the country code and info to the CSV file
    csv << [country_code, min_lo, max_lo, min_la, max_la, axis, value]
  end
end