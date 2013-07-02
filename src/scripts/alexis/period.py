# -*- coding:utf-8 -*-
#
# This file is part of OpenFisca.
# OpenFisca is a socio-fiscal microsimulation software
# Copyright © 2013 Alexis Eidelman, Clément Schaff, Mahdi Ben Jelloul
# Licensed under the terms of the GVPLv3 or later license
# (see openfisca/__init__.py for details)

# Script to compute the aggregates for all the referenced years

from src.lib.simulation import SurveySimulation 
from src.plugins.survey.aggregates import Aggregates
from src.plugins.survey.inequality import Inequality
from pandas import ExcelWriter, ExcelFile, HDFStore
import os

import pandas.rpy.common as com
import pdb

country = 'france'

from src.countries.france.data.sources.config import destination_dir


fname_all = "aggregates_inflated_loyers.xlsx"
fname_all = os.path.join(destination_dir, fname_all)              
num_output = None


def test_period():
    print "debut"
    writer = None
    years = range(2010,2011)
    filename = destination_dir+'output3.h5'
    store = HDFStore(filename)
    for year in years:        
        yr = str(year)
#        fname = "Agg_%s.%s" %(str(yr), "xls")
        simu = SurveySimulation()
        simu.set_config(year = yr, country = country)
        simu.set_param()
        import time
        
        tps = {}       
        deb_period = time.clock()           
        simu.set_config(survey_filename='C:\\Til\\output\\to_run_leg.h5', num_table=3, time_scale = 'month',
                        print_missing=False)
        simu.compute()
        tps['month'] = time.clock() - deb_period  
        
        print simu.output_table.table3['ind'].columns
        print simu.output_table.table3['ind'].ix[:10,['salbrut','salbrut01','salbrut02']]
        pdb.set_trace()
        agg3 = Aggregates()
        agg3.set_simulation(simu)
        agg3.compute()       
        df1 = agg3.aggr_frame
        print df1.to_string()
        
        deb_period = time.clock()       
        simu = SurveySimulation()
        simu.set_config(year = yr, country = country)
        simu.set_param()            
        simu.set_config(survey_filename='C:\\Til\\output\\to_run_leg.h5', num_table=3,
                        print_missing=False)
        simu.compute()
        tps['year'] = time.clock() - deb_period      
        
    
#             pdb.set_trace()
        agg3 = Aggregates()
        agg3.set_simulation(simu)
        agg3.compute()       
        df1 = agg3.aggr_frame
        print df1.to_string()

    print tps
    store.close()
    
if __name__ == '__main__':

    test_period()

