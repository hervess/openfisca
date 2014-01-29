'''
Created on 9 juil. 2013

@author: benjello
'''

from __future__ import division

from src.lib.simulation import ScenarioSimulation
from src.lib.simulation import SurveySimulation
from src.plugins.survey.aggregates import Aggregates
from datetime import datetime

country = 'france'
# destination_dir = "c:/users/utilisateur/documents/"
# fname_all = "aggregates_inflated_loyers.xlsx"
# fname_all = os.path.join(destination_dir, fname_all)              

def test_case(year, save = False):

    country = 'france'
    salaires_nets = 1120.43*12
    nmen = 20
    nmax = 3
    
    for reforme in [False, True]:
        simulation = ScenarioSimulation()
        simulation.set_config(year = year, country = country, reforme=reforme,
                        nmen = nmen, maxrev = salaires_nets*nmax, xaxis = 'sali')
        
        # Adding a husband/wife on the same tax sheet (foyer)
        simulation.scenario.addIndiv(1, datetime(1975,1,1).date(), 'conj', 'part') 
    #     simulation.scenario.addIndiv(2, datetime(2000,1,1).date(), 'pac', 'enf')
    #     simulation.scenario.addIndiv(3, datetime(2000,1,1).date(), 'pac', 'enf')
        
        # Loyers set statut d'occupation
        simulation.scenario.menage[0].update({"loyer": 1120.43/3}) 
        simulation.scenario.menage[0].update({"so": 4})
    
        simulation.set_param()
        simulation.P.ir.autre.charge_loyer.active = 1
        simulation.P.ir.autre.charge_loyer.plaf = 1000
        simulation.P.ir.autre.charge_loyer.plaf_nbp = 0 
    
        reduc = 0
        print simulation.P.ir.bareme
        print simulation.P.ir.bareme.nb
        for i in range(2, simulation.P.ir.bareme.nb):
            simulation.P.ir.bareme.setSeuil(i, simulation.P.ir.bareme.seuils[i]*(1-reduc) )
    
        print simulation.P.ir.bareme
        print simulation.P.ir.bareme.nb
    
    
        df = simulation.get_results_dataframe()
        print df.to_string()
        
        #Save example to excel
        if save:
            destination_dir = "c:/users/utilisateur/documents/"
            fname = "Trannoy_reforme.%s" %"xls"    
            if reforme:
                df.to_excel(destination_dir  + fname, sheet_name="difference")
            else:
                df.to_excel(destination_dir  + fname, sheet_name="Trannoy")

        

def survey_case(year):

#        fname = "Agg_%s.%s" %(str(yr), "xls")
    simulation = SurveySimulation()
    simulation.set_config(year = year, country = country, num_table=1, reforme=True)
    simulation.set_param()
    simulation.P.ir.autre.charge_loyer.plaf = 833
    simulation.P.ir.autre.charge_loyer.active = 1
    simulation.P.ir.autre.charge_loyer.plaf_nbp = 0 
    
    # plaf=1000 plaf_nbp=0: -42160, =1: -41292
    # plaf=500  plaf_nbp=0: -43033, =1: -42292
    
    # Bareme threshold reduction in pct
    reduc = 0
    print simulation.P.ir.bareme
    print simulation.P.ir.bareme.nb
    for i in range(2, simulation.P.ir.bareme.nb):
        simulation.P.ir.bareme.setSeuil(i, simulation.P.ir.bareme.seuils[i]*(1-reduc) )

    print simulation.P.ir.bareme
    print simulation.P.ir.bareme.nb
    simulation.compute()
    
# Compute aggregates
    agg = Aggregates()
    agg.set_simulation(simulation)
    agg.compute()
    
    df1 = agg.aggr_frame
    print df1.to_string()    
    return


if __name__ == '__main__':
#    survey_case(2009)
    test_case(2011)
    
