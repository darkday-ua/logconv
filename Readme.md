### Test script for given format log conversion
Do not try to use it with differnet formats, better use goacces utility

* Usage:

cat <logfilename> | python logconv.py [OPTIONS] [> <outfile>]\
        or\
python logconv.py <logfilename> [OPTIONS] [> <outfile>]\
        or\
cat <logfilename> | docker run -i logconv logfilename [OPTIONS] [> <outfile>]\
               or\
docker run -i darkday443/logconv logfilename [OPTIONS] [> <outfile>]
        
OPTIONS:\
-v &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;verbose\
-h &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;show this help\
-o <fname>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;set <fname> as output file. IF no -o <fname> is set, the default stdout will be used\
-d <dirname>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;set <dirname> as output directory (must be present)\
-f <filter_string>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;using filter <filter_string>\
-s <column> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;sort by <column>\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;ip      &nbsp;&nbsp; ip address\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;dt      &nbsp;&nbsp; datetime\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;bs      &nbsp;&nbsp;bytes sent\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;status  &nbsp;&nbsp;status code\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<digit> &nbsp;&nbsp;by field number [0..17]

## Docker image
Could be obtained with
docker pull darkday443/logconv:latest
## Git publishing
Script tries to create Git repository at target location or uses existing one.
Then it commits previous states, adds converted file and commits new state
