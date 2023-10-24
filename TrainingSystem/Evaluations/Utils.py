import pandas
import plotly.express as px
import plotly.graph_objects as go


class EvaluationAnalyzer():
    """
            Module: Class representing an importer module
             :param string Name: Name of the User
             :param string Role: Role of the User
        """

    def __init__(self, Name="",excelSheet=None):
        self.Name = Name
        self.RAWentries = []

        if excelSheet is not None:
            self._inputFile = excelSheet
            self.importEvaluations(excelSheet=self._inputFile)
        else:
            self._inputFile = ""


    @property
    def entriesRAW(self):
        return self.RAWentries

    @property
    def entryCount(self):
        return len(self.RAWentries)

    @property
    def trainingList(self):
        trainingList = []
        #determine unique trainings
        for entry in self.RAWentries:
            title = entry["title"]
            if title not in trainingList:
                trainingList.append(title)
        return trainingList

    def importEvaluations(self,excelSheet=None,googleSheet=None):
        entries=[]

        if excelSheet is not None:
            df = pandas.read_excel(excelSheet)

            submission=df['Submission Date'].values
            firstName = df['First Name'].values
            lastName = df['Last Name'].values
            topic = df['Onderwerp en inhoud van de opleiding'].values
            topicRemarks = df['De opleiding voldeed aan mijn verwachtingen'].values
            teacher = df['Lesgever(s)'].values
            teacherRemarks = df['Lesgever(s) 2'].values
            location = df['Locatie'].values
            locationRemarks = df['Locatie 2'].values
            duration = df['Duur van de opleiding'].values
            ldurationRemarks = df['Duur van de opleiding 2'].values
            improvement = df['Ik kan mijn job nu beter uitvoeren'].values
            improvementRemark = df['Ik kan mijn job nu beter uitvoeren 2'].values
            expectation = df['De opleiding voldeed aan mijn verwachtingen 2'].values
            expectationRemark = df['De opleiding voldeed aan mijn verwachtingen 3'].values
            title = df['Titel opleiding'].values

        #generate entries
        for i in range(0,len(submission),1):
            entries.append({"Date":submission[i].__str__(),"title":title[i],"firstName":firstName[i],"lastName":lastName[i],"topicScore":topic[i],"teacherScore":teacher[i],"locationScore":location[i],"durationScore":duration[i],"improvementScore":improvement[i],"expectationScore":expectation[i]})

        self.RAWentries = entries
        return entries

    def _createBarChart(self,title="",inputData=None,visualize=False,export=True):

        df = pandas.DataFrame(dict(
            r=[inputData["topicScore"], inputData["teacherScore"], inputData["locationScore"], inputData["improvementScore"],
               inputData["expectationScore"]],
            theta=['Onderwerp', 'Lesgever(s)', 'Locatie','Bruikbaarheid', 'Verwachtingen']))
        fig = px.line_polar(df, r='r', theta='theta', line_close=True)
        fig.update_traces(fill='toself')
        if export:
            fig.write_image("output/static/" + title + "_spiderchart.png")
            fig.write_html("output/dynamic/" + title + "_spiderchart.png")
        if visualize:
            fig.show()

    def compareTrainings(self,list=[],visualize=False,export=True):

        chartInput = []
        for training in list:
            count = 0
            scores = {'topicScore': 0.0, 'teacherScore': 0.0, 'locationScore': 0.0, 'durationScore': 0.0,
                      'improvementScore': 0.0, 'expectationScore': 0.0}
            # loop over all entries and calculate mean()
            for entry in self.RAWentries:
                if entry["title"] == training:
                    count = count + 1
                    scores["topicScore"] = scores["topicScore"] + entry["topicScore"]
                    scores["teacherScore"] = scores["teacherScore"] + entry["teacherScore"]
                    scores["locationScore"] = scores["locationScore"] + entry["locationScore"]
                    scores["improvementScore"] = scores["improvementScore"] + entry["improvementScore"]
                    scores["expectationScore"] = scores["expectationScore"] + entry["expectationScore"]
            # post-process mean
            scores["topicScore"] = scores["topicScore"] / count
            scores["teacherScore"] = scores["teacherScore"] / count
            scores["locationScore"] = scores["locationScore"] / count
            scores["improvementScore"] = scores["improvementScore"] / count
            scores["expectationScore"] = scores["expectationScore"] / count

            chartInput.append(scores)

        categories = ['Onderwerp', 'Lesgever(s)', 'Locatie','Bruikbaarheid', 'Verwachtingen']

        fig = go.Figure()
        for i in range(0,len(list),1):
            fig.add_trace(go.Scatterpolar(
                r=[chartInput[i]["topicScore"], chartInput[i]["teacherScore"], chartInput[i]["locationScore"], chartInput[i]["improvementScore"], chartInput[i]["expectationScore"]],
                theta=categories,
                fill='toself',
                name=list[i]
            ))
        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 5]
                )),
            showlegend=True
        )
        if export:
            fig.write_image("output/static/comparison.png")
            fig.write_html("output/dynamic/comparison.html")

        if visualize:
            fig.show()

    def generateRadarChart(self,title=None,visualize=False,export=True):
        _uniqueTrainingNames = self.trainingList

        if title is None:
            #TODO: generate the radar charts of all trainings and map them in a single chart
            x = 10
        elif title == "ALL":
            # TODO: generate the radar charts of all trainings in a seperate chart
            for training in _uniqueTrainingNames:
                count = 0
                scores = {'topicScore': 0.0, 'teacherScore': 0.0, 'locationScore': 0.0, 'durationScore': 0.0,
                          'improvementScore': 0.0, 'expectationScore': 0.0}
                # loop over all entries and calculate mean()
                for entry in self.RAWentries:
                    if entry["title"] == training:
                        count = count + 1
                        scores["topicScore"] = scores["topicScore"] + entry["topicScore"]
                        scores["teacherScore"] = scores["teacherScore"] + entry["teacherScore"]
                        scores["locationScore"] = scores["locationScore"] + entry["locationScore"]
                        scores["improvementScore"] = scores["improvementScore"] + entry["improvementScore"]
                        scores["expectationScore"] = scores["expectationScore"] + entry["expectationScore"]
                # post-process mean
                scores["topicScore"] = scores["topicScore"] / count
                scores["teacherScore"] = scores["teacherScore"] / count
                scores["locationScore"] = scores["locationScore"] / count
                scores["improvementScore"] = scores["improvementScore"] / count
                scores["expectationScore"] = scores["expectationScore"] / count

                self._createBarChart(title=training, inputData=scores, visualize=False, export=export)
        else:
            count=0
            scores = {'topicScore': 0.0, 'teacherScore': 0.0, 'locationScore': 0.0, 'durationScore': 0.0,
                      'improvementScore': 0.0, 'expectationScore': 0.0}
            # loop over all entries and calculate mean()
            for entry in self.RAWentries:
                if entry["title"]== title:
                    count = count + 1
                    scores["topicScore"] = scores["topicScore"] + entry["topicScore"]
                    scores["teacherScore"] = scores["teacherScore"] + entry["teacherScore"]
                    scores["locationScore"] = scores["locationScore"] + entry["locationScore"]
                    scores["improvementScore"] = scores["improvementScore"] + entry["improvementScore"]
                    scores["expectationScore"] = scores["expectationScore"] + entry["expectationScore"]
            #post-process mean
            scores["topicScore"] = scores["topicScore"] / count
            scores["teacherScore"] = scores["teacherScore"] / count
            scores["locationScore"] = scores["locationScore"] / count
            scores["improvementScore"] = scores["improvementScore"] / count
            scores["expectationScore"] = scores["expectationScore"] / count

            self._createBarChart(title=title,inputData=scores,visualize=visualize,export=export)
