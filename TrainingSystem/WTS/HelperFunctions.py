import pandas


class Importer():
    """
            Module: Class representing an importer module
             :param string Name: Name of the User
             :param string Role: Role of the User
        """

    def __init__(self, Name=""):
        self.Name = Name

    def importTrainings(self,excelSheet=None,googleSheet=None):
        entries=[]

        if excelSheet is not None:
            df = pandas.read_excel(excelSheet)

            submission=df['Submission Date'].values
            firstName = df['First Name'].values
            lastName = df['Last Name'].values
            function = df['Functie'].values
            content = df['Inhoud'].values
            location = df['Locatie'].values
            dates = df['Datums'].values
            ID = df['Submission ID'].values

        #generate entries
        entry = []
        for i in range(0,len(submission),1):
            # ---- interpret dates ----
            dateString=""
            for date in dates[i]:
                _date = date.strip()
                dateString+=_date

            _dateList = []
            _timingList = []
            x=dateString.split("Dag:")
            for i in range(1,len(x),1):
                y=x[i].split(",Aantaluur:")
                _date=y[0]
                _time=y[1]
                _dateList.append(_date)
                _timingList.append(_time)

            entry.append([submission[i].__str__(),firstName[i],lastName[i],function[i],content[i],location[i],_dateList,_timingList,ID[i]])
            entries.append(entry)
        return entries
