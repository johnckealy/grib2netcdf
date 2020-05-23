# Grib 2 NetCDF 

*An online meteorological file conversion tool*

I created grib2netcdf to address the frustrations that myself and others in the atmospheric science community have felt with converting betweem the Grib and the NetCDF file formats (which should be an easy thing to do!).

It's a simple tool, the user uploads a Grib file, and the fields are parsed and displayed. You can select which fields you want, and then simply submit to create your NetCDF file. 

#### Grib? NetCDF? 

Grib is a standard file format of the World Meteorological Organization (WMO). If you've ever used an online weather forecast,
it almost certainly came from a Grib file (which was then processed by the weather app's owner). 

Grib is lightweight and comprehensive, but sometimes it can be a little overwhelming. Another very common data format
in meteorology is NetCDF. NetCDF is friendlier, and can be inspected at a glance using tools like `ncdump`. This makes
NetCDF a common choice for many scientists. 

#### Code

Grib2NetCDF is written in Python's Django framework. 
