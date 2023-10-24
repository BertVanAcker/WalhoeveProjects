/*
  @brief: simple script to send an evaluation form on the last day of the training.
          Triggering this script once a day will automate the mailing.

  @version: External trainings


  @author: Bert Van Acker
  @contact: bva.bmkr@gmail.com
*/

function emailAlert() {
  /* Internal variables */
  var DEBUG = false;
  var courseName = 1;
  var notificationDataColumn = 5;
  var mailColumn = 6;
  var nameColumn = 1;
  var counter = 0;
  var adminMail = 'bva.bmkr@gmail.com'; /* TODO: change to admin mail address */

  /* Collect today info */
  var today = new Date();
  var todayMonth = today.getMonth() + 1;
  var todayDay = today.getDate();
  var todayYear = today.getFullYear();

  /* Collect spreadsheet info */
  var sheet = SpreadsheetApp.getActive().getSheetByName('Form Responses')
  var startRow = 2; // Ignore spreadsheet header
  var numRows = 200; //Increase if more training entries

  var dataRange = sheet.getRange(startRow, 1, numRows, 999);
  var data = dataRange.getValues();

  /* Process spreadsheet data */
  for (var i = 0; i < data.length; ++i) {
    var row = data[i];
    
    if (row[0]!=""){
      var notificationDates = row[notificationDataColumn]
      var mailAddresses = row[mailColumn]
      var mailList = [];
      var nameList = [];

      /* Fetch mail adres */
      //var mailAdres = row[1].toLowerCase()+"."+row[2].toLowerCase()+'@dewalhoeve.be' ;
      const mails = mailAddresses.split(/\r?\n/);
      
      /* fetch all emails */
      for (var j = 0; j < mails.length; j++) {
        var mail_raw = mails[j].split(", ");
        var name_raw = mail_raw[0].split("Werknemer: ");
        var function_raw = mail_raw[1].split("Functie: ");
        var evaluation_raw = mail_raw[2].split("Evaluatie?: ");
        /* append to mailing list */
        var mail_raw = name_raw[1].split(" ")
        if (evaluation_raw[1] == "Ja"){
          mailList.push(mail_raw[0].toLowerCase()+"."+mail_raw[1].toLowerCase()+'@dewalhoeve.be');
          nameList.push(mail_raw[0]);
        }
      }

      

      /* Fetch last course date */
      const result = notificationDates.split(/\r?\n/);
      var date_raw = result[result.length-1]
      var date_raw2 = date_raw.split("Dag: ").pop();
      var date = date_raw2.split(", Aantal uur: ");
      var notificationDate = date[0];


      var notificationDateMonth = new Date(notificationDate).getMonth() + 1;
      var notificationDateDay = new Date(notificationDate).getDate();
      var notificationDateYear = new Date(notificationDate).getFullYear();
      
      /* Send e-mail when today is last day of a training */

      if (DEBUG){Logger.log(mailList)};
      if (DEBUG){Logger.log(nameList)};
      
      if (
        notificationDateMonth === todayMonth &&
        notificationDateDay === todayDay &&
        notificationDateYear === todayYear
      ) {
        counter+=1;
        for (var k = 0; k < mailList.length; k++) {
          var subject = "Evaluatieformulier vorming";
          var message = 
		  'Dag '+ row[nameColumn] +',\n' +
		  '\n' +
		  'Je volgde net een opleiding "'+row[courseName]+'"(titel in te vullen op evaluatieformulier), vul je het evaluatieformulier in? Je kan dit door op onderstaande link te klikken:\n'+
		  '\n' + 
		  'Link: https://form.jotform.com/230486716561056 \n'+  
		  '\n'+
		  'Alvast bedankt'+
		  '\n'+
		  'Met vriendelijke groeten,\n'+
		  'vzw De Walhoeve'

          MailApp.sendEmail(mailList[k], subject, message);
          if (DEBUG){Logger.log('Notification send!')};
        }
      } 
    } 
  }

  /* Send admin mail for follow-up */
    var subject = "AUTO-SCRIPT - Mail alerter triggered ";
    var message = 
    '--------------------------------------------------------------------------------------------------------------------------------------------\n'+
    'Mail alerter triggered on ' + today + '\n' +
    '\n' +
    '--------------------------------------------------------------------------------------------------------------------------------------------\n'+
    'Number of send mails: '+ counter + 
    '\n'+
    '--------------------------------------------------------------------------------------------------------------------------------------------'
    MailApp.sendEmail(adminMail, subject, message);
    if (DEBUG){Logger.log('Notification send!')};

}
