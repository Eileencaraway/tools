lammpsOperation.py is the code written by joyjit, which I keep it as original version. 
While it only works for dump in one file, thus I made few changings to apply his functions in 
lammpsOperationnp.py code 
 
to run computeMSD.py 

can use the following sentense: 

python2.7 computeMSD.py -com -dt 0.00001 11 12 13

-com means minus the center of mass 
-dt is the intergration timesteps 
11 12 13 is the columns that I wish to input, 
can put x y z , can put tx ty tz

