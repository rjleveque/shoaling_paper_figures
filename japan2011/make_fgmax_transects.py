"""
Create fgmax_grid.txt input files 

Set up to make fgmax points at cell centers of finest grid level,
as specified in setrun.py.  Assumes coarse grid has 2 degree resolution
and refinement by factors 3 and 4.  If you change setrun.py, you need to 
adjust things here too.

"""

from clawpack.geoclaw import fgmax_tools

min_level_check = 4

dx_fine = 1./(5*6*4.)  # grid resolution at finest level

fg = fgmax_tools.FGmaxGrid()
fg.point_style = 1       # will specify a 1d transect of points
fg.x1 = -127.1 + dx_fine/2.
fg.x2 = -124. - dx_fine/2.
fg.y1 = 44.4
fg.y2 = 44.4
fg.dx = dx_fine
fg.tstart_max =  8.5*3600.     # when to start monitoring max values
fg.tend_max = 1.e10       # when to stop monitoring max values
fg.dt_check = 60.         # target time (sec) increment between updating 
                           # max values
fg.min_level_check = min_level_check    # which levels to monitor max on
fg.arrival_tol = 1.e-2    # tolerance for flagging arrival

fg.input_file_name = 'fgmax_transect_1.txt'
fg.write_input_data()

fg = fgmax_tools.FGmaxGrid()
fg.point_style = 1       # will specify a 1d transect of points
fg.x1 = -127.1 + dx_fine/2.
fg.x2 = -124. - dx_fine/2.
fg.y1 = 44.2
fg.y2 = 44.2
fg.dx = dx_fine
fg.tstart_max =  8.5*3600.     # when to start monitoring max values
fg.tend_max = 1.e10       # when to stop monitoring max values
fg.dt_check = 60.         # target time (sec) increment between updating 
                           # max values
fg.min_level_check = min_level_check    # which levels to monitor max on
fg.arrival_tol = 1.e-2    # tolerance for flagging arrival

fg.input_file_name = 'fgmax_transect_2.txt'
fg.write_input_data()

