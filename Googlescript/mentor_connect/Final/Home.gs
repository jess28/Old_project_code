function doGet() {
  var html = HtmlService.createTemplateFromFile('Search').evaluate()
       .setTitle('Frogs and Human Health')
       .setSandboxMode(HtmlService.SandboxMode.NATIVE);
  return html;
}

function findDisease(searchTerm) {
  var disObj = getDiseaseData();
  for (var i = 0; i < disObj.length; i++) {
    if (disObj[i].disease == searchTerm) { //needs exact match to info in table
      var matchSheet = SpreadsheetApp.openByUrl(disObj[i].url).getSheets()[0];
      var url = disObj[i].url;
      var results = getDiseaseResults(matchSheet); 
      var msg = 'direct';
      var term = disObj[i].realName;
        for (var x = 0; x < results.length; x++) {
        var eSplit = String(results[x].eVal).split('e')
        if (eSplit[0].length > 4) {
          eSplit[0] = parseFloat(eSplit[0]).toFixed(1)
          results[x].eVal = eSplit.join('e')
        }
       }
      return [msg, results, term, url];
    }
  }
}

function searchDisease(searchTerm, words) {
  //searches the human information sheet to get genes related to searched disease
  var disObj = getDiseaseData();
  var longWords = [];
  var choiceList = [];
  var choiceObj = {};
  var found = {};
  words.sort(function(a,b) {
    return b.length - a.length;
  });
  if (words.length > 3) {
    var longWords = words.slice(0,4);
    var choices = fuzzySearch(longWords);
    for (var m = 0; m < disObj.length; m++) {
      for (var n = 0; n < choices.length; n++) {
        if (choices[n] == disObj[m].disease) {
          var insert = {'realName': disObj[m].realName, 'disease': choices[n]}
          if (!(disObj[m].realName in found)) {
            found[disObj[m].realName] = disObj[m].realName;
            choiceList.push(insert);
          }
        }
      }
    }
  }else{
    var choices = fuzzySearch(words);
    for (var m = 0; m < disObj.length; m++) {
      for (var n = 0; n < choices.length; n ++) {
        if (choices[n] == disObj[m].disease) {
          var insert = {'realName': disObj[m].realName, 'disease': choices[n]}
          if (!(disObj[m].realName in found)) {
            found[disObj[m].realName] = disObj[m].realName;
            choiceList.push(insert);
          }
        }
      }
    }
  }
  var msg = 'fuzzy';
  return [msg, choiceList];
}
        
    
function searchGene(searchTerm) {
  //searches the human information sheet to get diseases related to searched gene
  var geneObj = getGeneData();
  Logger.log('now');
  var diseaseList = [];
  var genes = [searchTerm];
  var success = false;
  for (var i = 0; i < geneObj.length; i++) {
    Logger.log('loop');
    if (searchTerm == geneObj[i].gene.toUpperCase()) {
      Logger.log('please?');
      var matchSheet = SpreadsheetApp.openByUrl(geneObj[i].url).getSheets()[0];
      var url = geneObj[i].url;
      Logger.log('hello?');
      var results = getGeneResults(matchSheet); 
      Logger.log('third');
      var term = geneObj[i].gene;
      for (var x = 0; x < results.length; x++) {
        var eSplit = String(results[x].eVal).split('e')
        if (eSplit[0].length > 4) {
          eSplit[0] = parseFloat(eSplit[0]).toFixed(1)
          results[x].eVal = eSplit.join('e')
        }
      }
      return [results, term, url];
    }
  }
  throw "Unable to find gene in our database. Either the gene does not have a frog homolog, or the spelling needs to be checked.";
}

function getDiseaseResults(sheet, disease) {
  var range = sheet.getDataRange();
  var data = range.getValues();
  var keys = ['frog', 'hGene', 'fGene', 'cleanDis', 'origDis', 'perId', 'alLen', 'eVal', 'bit'];
  var resObj = getObjects(data, keys);
  for (var x = 0; x < resObj.length; x++) {
    resObj[x].disease = disease;
  }
  return resObj;
}

function getGeneResults(sheet) {
  Logger.log('second');
  var range = sheet.getDataRange();
  var data = range.getValues();
  var keys = ['frog', 'fGene', 'cleanDis', 'origDis', 'perId', 'alnLen', 'eVal', 'bit'];
  var resObj = getObjects(data, keys);
  return resObj;
}

function fuzzySearch(testWords) {
  var wordObjects = getWordData();
  Logger.log(wordObjects[0]);
  var posDis = [];
  var success = false;
  for (i = 0; i < wordObjects.length; i++) {
    for (j = 0; j < testWords.length; j++) {
      var delta = testWords[j].length - wordObjects[i].total
      if (testWords[j] == wordObjects[i].word) {
        return wordObjects[i].diseases.split(', ');
      } else if (Math.abs(delta) <= 3 && testWords[j].length >= 10) {
        var match = matchLetters(testWords[j], wordObjects[i]);
        if (match == true) {
          var dis = wordObjects[i].diseases.split(', ');
          success = true;
          for(var x = 0; x < dis.length; x++) {
            posDis.push(dis[x]);
          }
        }
      } else if (Math.abs(delta) <= 1 && testWords[j].length < 10) {
        var match = matchLetters(testWords[j], wordObjects[i]);
        if (match == true) {
          var dis = wordObjects[i].diseases.split(', ');
          success = true;
          for(var x = 0; x < dis.length; x++) {
            posDis.push(dis[x]);
          }
        }
      }
    }
  }
  if (success == true) {
    return posDis;
  }else {
    throw "Unable to find disease in our database. Either the disease does not have a frog gene homolog association, or the spelling needs to be checked.";
  }
}

function matchLetters(word, wordObject) {
  var lett = word.split('');
  var char = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 
              'y', 'z', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', ',', '.']
  var wordArr = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
  var objArr = [wordObject.a, wordObject.b, wordObject.c, wordObject.d, wordObject.e, wordObject.f, wordObject.g, wordObject.h, 
                wordObject.i, wordObject.j, wordObject.k, wordObject.l, wordObject.m, wordObject.n, wordObject.o, wordObject.p, 
                wordObject.q, wordObject.r, wordObject.s, wordObject.t, wordObject.u, wordObject.v, wordObject.w, wordObject.x, 
                wordObject.y, wordObject.z, wordObject.zero, wordObject.one, wordObject.two, wordObject.three, wordObject.four, 
                wordObject.five, wordObject.six, wordObject.seven, wordObject.eight, wordObject.nine, wordObject.comma, wordObject.period]
  var comp = 0
  for (var c = 0; c < char.length; c++) {
    for (var l = 0; l < lett.length; l++) {
      if (lett[l] == char[c]) {
        wordArr[c]++;
      }
    }
  }
  for (var i = 0; i < objArr.length; i++) {
    var dif = parseInt(objArr[i]) - parseInt(wordArr[i]);
    comp = comp + Math.abs(dif);
  }
  if (comp < 0.25*word.length || comp <= 2) {
    return true;
  }else{
    return false;
  }
}
  
function getGeneData() {
  var gm = SpreadsheetApp.openByUrl('https://docs.google.com/a/malonelab.com/spreadsheets/d/1KzTXsk0-niK6zYVp0fiy4DMJv3-2I5yBbw7oTTyaWr4/edit#gid=0');
  var geneSheet = gm.getSheets()[0];
  Logger.log('first');
  var geneRange = geneSheet.getDataRange();
  var geneKeys = ['gene', 'url']
  var geneObj = getObjects(geneRange.getValues(), geneKeys);
  Logger.log(geneObj[0]);
  return geneObj;    
}

function getDiseaseData() {
  var dm = SpreadsheetApp.openByUrl('https://docs.google.com/a/malonelab.com/spreadsheets/d/1v6OcFCJb92-jqLcNQFALeCHZZWOEO5SUkZBxSd7JUbQ/edit?usp=drive_web');
  var disSheet = dm.getSheets()[0];
  var disRange = disSheet.getDataRange();
  var disKeys = ['disease', 'url', 'realName'];
  var disObj = getObjects(disRange.getValues(), disKeys);
  return disObj;
}

function getWordData() {
  //connects to the word sheet and sends the info to getRowsData
  Logger.log('first');
  var ss = SpreadsheetApp.openByUrl('https://docs.google.com/a/malonelab.com/spreadsheets/d/1Ao-QDb_9m0jQdXnYpTeat86r504zCJ4urOu-cxP6qGA/edit#gid=1282959752');
  Logger.log('second');
  var wordSheet = ss.getSheets()[0];
  Logger.log('third');
  var wordRange = wordSheet.getDataRange();
  Logger.log('fourth');
  var wordKeys = ['word', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 
                  'zero', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'comma', 'period', 'total', 'diseases']
  var wordObjects = getObjects(wordRange.getValues(), wordKeys);
  Logger.log('fifth');
  return wordObjects;
}

function getObjects(data, keys) {
  //creates an array of objects from the rows in the sheet
  //each object in the array is one row
  var objects = [];
  for (var i = 0; i < data.length; i++) {
    var object = {};
    var hasData = false;
    for (var j = 0; j < data[i].length; j++) {
      var cellData = data[i][j];
      if (isCellEmpty(cellData)) {
        continue;
      }
      object[keys[j]] = cellData;
      hasData = true;
    }
    if (hasData) {
      objects.push(object);
    }
  }
  return objects;
}

function isCellEmpty(cellData) {
  return typeof(cellData) == "string" && cellData == "";
}
