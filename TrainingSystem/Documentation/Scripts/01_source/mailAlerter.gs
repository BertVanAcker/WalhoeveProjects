/*
  @brief: simple script to send an evaluation form on the last day of the training.
          Triggering this script once a day will automate the mailing.


  @author: Bert Van Acker
  @contact: bva.bmkr@gmail.com
*/

function emailAlert() {
  /* Internal variables */
  var DEBUG = false;
  var notificationDataColumn = 13;
  var mailColumn = 14;
  var nameColumn = 1;
  var counter = 0;
  var adminMail = 'bva.bmkr@gmail.com'; /* TODO: change to admin mail address */

  /* Collect today info */
  var today = new Date();
  var todayMonth = today.getMonth() + 1;
  var todayDay = today.getDate();
  var todayYear = today.getFullYear();

  /* Collect spreadsheet info */
  var sheet = SpreadsheetApp.getActive().getSheetByName('Formulierreacties 1')
  var startRow = 2; // Ignore spreadsheet header
  var numRows = 200; //Increase if more training entries

  var dataRange = sheet.getRange(startRow, 1, numRows, 999);
  var data = dataRange.getValues();

  /* Process spreadsheet data */
  for (var i = 0; i < data.length; ++i) {
    var row = data[i];
    var notificationDate = row[notificationDataColumn]
    if (DEBUG){Logger.log(notificationDate)};

    var notificationDateMonth = new Date(notificationDate).getMonth() + 1;
    var notificationDateDay = new Date(notificationDate).getDate();
    var notificationDateYear = new Date(notificationDate).getFullYear();

    /* Send e-mail when today is last day of a training */
    if (
      notificationDateMonth === todayMonth &&
      notificationDateDay === todayDay &&
      notificationDateYear === todayYear
    ) {
      counter+=1;
      var subject = "Evaluatieformulier vorming";
      var message = 
      'Dag '+ row[nameColumn] +',\n' +
      '\n' +
      'Je volgde net een opleiding, vul je het evaluatieformulier in? Je kan dit door op onderstaande link te klikken:\n'+
      '\n' + 
      'Link: https://forms.gle/aWUZcmEKPTBUNvfQ8 \n'+  
      '\n'+
      'Alvast bedankt'+
      '\n'+
      'Met vriendelijke groeten,\n'+
      'De Walhoeve'

      MailApp.sendEmail(row[mailColumn], subject, message);
      if (DEBUG){Logger.log('Notification send!')};
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
