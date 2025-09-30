import pandas as pd
from utils import *

medication_data = pd.read_excel("data/Table_1.xls", dtype="string")
medication_data = rename_columns(medication_data)
medication_data = clean_data(medication_data, "Total % (n) (n=402)")
medication_data = clean_data(medication_data, "With Polypharmacy % (n) (n=344)")
medication_data = clean_data(medication_data, "Without Polypharmacy % (n) (n=58)")
plot_medicines(medication_data, "output/medications.jpg")

drp_data = pd.read_excel("data/Table_2.xls", dtype="string")
drp_data = rename_columns(drp_data)
drp_data = clean_data(drp_data, 'Total % (n) (n=316)')
drp_data = clean_data(drp_data, 'With Polypharmacy % (n) (n=280)')
drp_data = clean_data(drp_data, 'Without Polypharmacy % (n) (n=36)')
plot_drp(drp_data, "output/drp.jpg")

intervention_data = pd.read_excel("data/Table_3.xls", dtype="string")
intervention_data = rename_columns(intervention_data)
intervention_data = clean_data(intervention_data, 'Total % (n) (n=307)')
intervention_data = clean_data(intervention_data, 'Therapeutic goal achieved % (n) (n=202)')
intervention_data = clean_data(intervention_data, 'Therapeutic goal not achieved % (n) (n=40)')
plot_interventions(intervention_data, "output/interventions.jpg")

clinical_outcomes = pd.read_csv("data/clinical_outcomes.csv", dtype="string")
clinical_outcomes = clinical_outcomes.fillna("0")
plot_polypharmacy_heatmap(clinical_outcomes, "output/clinical_outcomes")

drp_causes = pd.read_csv("data/drp_causes.csv", dtype="string")
plot_drp_causes_pie(drp_causes)

plot_conditions_pie("output/patient_conditions.jpg")

breakpoint()

