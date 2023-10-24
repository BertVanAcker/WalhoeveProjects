from Evaluations.Utils import *

analyzer = EvaluationAnalyzer(excelSheet="input/Evaluations_24_10_2023.xlsx")

# --- get RAW entries ---
entries = analyzer.RAWentries
# --- get number of entries ---
print(analyzer.entryCount)
# --- get unique training names ---
print(analyzer.trainingList)

# --- generate radar chart of single training ---
#analyzer.generateRadarChart(title="intervisie Cross Link ivm AD (verblijf) op vraag",visualize=True,export=False)

# --- generate all radar charts ---
#analyzer.generateRadarChart(title="ALL",export=True)

# --- map different trainings on single chart
trainings = ["Intervisie crosslink Veurne","vertrouwenspersoon","Workshop Wildplukken"]
#analyzer.compareTrainings(trainings,visualize=True,export=True)

# --- compare all trainings ---
trainings = analyzer.trainingList
analyzer.compareTrainings(trainings,visualize=True,export=True)


#for entry in entries:
#    print(entry)