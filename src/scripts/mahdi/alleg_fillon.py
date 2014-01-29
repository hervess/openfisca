# -*- coding:utf-8 -*-
# Created on 22 janv. 2014
# This file is part of OpenFisca.
# OpenFisca is a socio-fiscal microsimulation software
# Copyright © #2014 Clément Schaff, Mahdi Ben Jelloul
# Licensed under the terms of the GVPLv3 or later license
# (see openfisca/__init__.py for details)


from src.lib.simulation import SurveySimulation
from src.plugins.survey.aggregates import Aggregates


def survey_case(year):
     
    country = 'france'
#        fname = "Agg_%s.%s" %(str(yr), "xls")
    simulation = SurveySimulation()
    simulation.set_config(year = year, country = country)
    simulation.set_param()

#    Ignore this
#    inflator = get_loyer_inflator(year)
#    simulation.inflate_survey({'loyer' : inflator})

    simulation.compute()
    
#    Saving aggregates
#    if writer is None:
#        writer = ExcelWriter(str(fname)
#    agg.aggr_frame.to_excel(writer, yr, index= False, header= True)


# Displaying a pivot table    
    from src.plugins.survey.distribution import OpenfiscaPivotTable
    pivot_table = OpenfiscaPivotTable()
    pivot_table.set_simulation(simulation)
    df2 = pivot_table.get_table(by ='type_sal', entity="ind", vars=['alleg_fillon']) 
    print df2.to_string()
    output = simulation.output_table.table
    input = simulation.input_table.table
    
    print (output["alleg_fillon"]*input["wprm"]).sum()/1e9
    import pdb
    pdb.set_trace()

if __name__ == '__main__':
    survey_case(2009)
