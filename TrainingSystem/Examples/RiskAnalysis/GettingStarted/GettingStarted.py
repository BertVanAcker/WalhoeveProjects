from Evaluations.Utils import *

analyzer = RiskAnalyzer(excelSheet="input/Psychosociale_risicos.xlsx")

analyzer._analyzeQuestions()

analyzer.createAllPieCharts()

analyzer.generateDocument()

