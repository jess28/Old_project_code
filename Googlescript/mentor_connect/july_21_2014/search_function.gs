var ss = SpreadsheetApp.openByUrl('https://docs.google.com/a/malonelab.com/spreadsheets/d/1Ao-QDb_9m0jQdXnYpTeat86r504zCJ4urOu-cxP6qGA/edit#gid=1345630848');

function doGet() {
  var html = HtmlService.createTemplateFromFile('Search').evaluate()
    .setTitle('Search')  
    .setSandboxMode(HtmlService.SandboxMode.NATIVE);
  return html;
}

function searchDisease(searchTerm, words) {
  Logger.log('start');
  //searches the human information sheet to get genes related to searched disease
  var humanObjects = getHumanData();
  var geneList = [];
  var longWords = [];
  var choiceList = [];
  var choiceObj = {};
  for (var i = 0; i < humanObjects.length; i++) {
    if (humanObjects[i].disease == searchTerm) { //needs exact match to info in table
      var genes = humanObjects[i].gene.split(', ');
      for (var j = 0; j < genes.length; j++) {
        geneList.push(genes[j]);
      }
      var frogs = frogSearch(geneList);
      return frogs;
    }
  }
  Logger.log('sending to fuzzy');
  words.sort(function(a,b) {
    return b.length - a.length;
  });
  if (words.length > 3) {     //EVENTUALLY FIGURE OUT HOW TO CONNECT USER CHOSEN CHOICE TO FROG GENES
    var longWords = words.slice(0,4);
    var choices = fuzzySearch(longWords);
    for (var m = 0; m < humanObjects.length; m++) {
      for (var n = 0; n < choices.length; n++) {
        if (choices[n] == humanObjects[m].disease) {
          choiceList.push(humanObjects[m].realName);
        }
      }
    }
  }else{
    var choices = fuzzySearch(words);
    for (var m = 0; m < humanObjects.length; m++) {
      for (var n = 0; n < choices.length; n ++) {
        if (choices[n] == humanObjects[m].disease) {
          choiceList.push(humanObjects[m].realName);
        }
      }
    }
  }
  return choiceList;
}
        
    
function searchGene(searchTerm) {
  Logger.log('start');
  //searches the human information sheet to get diseases related to searched gene
  var humanObjects = getHumanData();
  var diseaseList = [];
  var genes = [searchTerm];
  var success = false;
  for (var i = 0; i < humanObjects.length; i++) {
    var geneList = humanObjects[i].gene.split(', ');
    if (geneList.length > 1) {
      for (var j = 0; j < geneList.length; j++) {
        if (searchTerm == geneList[j]) {
          success = true;
          diseaseList.push(humanObjects[i].realName);
        }
      }
    }
  }
  if (success == true){
    var frogs = frogSearch(genes);
    Logger.log(frogs);
    Logger.log(diseaseList);
    return frogs, diseaseList;
  } else {
    throw "Unable to find gene in our database. Please try a different search.";
  }
}

function frogSearch(genes) {
  Logger.log('frog');
  var bmax = [SpreadsheetApp.openByUrl('https://docs.google.com/a/malonelab.com/spreadsheets/d/1shM26UUKxPI5FrMg0S1bcGsWAD2AgPharJyIbDH89Ug/edit#gid=229480230'), 'Bmax'];
  var mant = [SpreadsheetApp.openByUrl('https://docs.google.com/a/malonelab.com/spreadsheets/d/1KCBWrytw1aca1eSvB8Fl1SfNc6HHqe653LM3_VV08uE/edit#gid=1440621495'), 'Mant'];
  var preg = [SpreadsheetApp.openByUrl('https://docs.google.com/a/malonelab.com/spreadsheets/d/1pt7ciX6pf70R2wmUYOJrSdLDHHcD86tKJc1N00G1wvg/edit#gid=2112850502'), 'Preg'];
  var pyxi = [SpreadsheetApp.openByUrl('https://docs.google.com/a/malonelab.com/spreadsheets/d/1KynPDPTnN9KvW5nCMQWDGyR9qXSANMIin_N1fOuaMmw/edit#gid=1341846056'), 'Pyxi'];
  var rcla = [SpreadsheetApp.openByUrl('https://docs.google.com/a/malonelab.com/spreadsheets/d/1u2b-VJT3YJfwJZcuaWmPc7Lb9fwtXrpXVuESA0Zzq4o/edit#gid=750327447'), 'Rcla'];
  var rpip = [SpreadsheetApp.openByUrl('https://docs.google.com/a/malonelab.com/spreadsheets/d/1oZFCVbLx5FTUIx8ezfwl5xFFvY0t4o0m8v7DYapjd9w/edit#gid=1701612046'), 'Rpip'];
  var rsnewb = [SpreadsheetApp.openByUrl('https://docs.google.com/a/malonelab.com/spreadsheets/d/1qWAE0HzIwy4XGvlRLgxYo1EbxiLcbT1Cw7BSC5vNEwg/edit#gid=1909228243'), 'RsNewb'];
  var rssoap = [SpreadsheetApp.openByUrl('https://docs.google.com/a/malonelab.com/spreadsheets/d/1Q4ppQUxskmyBlsYb7ou54FsyD3YFpF6PGg3diRjOfbI/edit#gid=1262432704'), 'RsSoap'];
  var xtro = [SpreadsheetApp.openByUrl('https://docs.google.com/a/malonelab.com/spreadsheets/d/1OeBba4G3KV0UECpJ_Ai7nC4UBDyZKHcpdlS-hXXozJg/edit#gid=493175684'), 'Xtro'];
  var data = [bmax, mant, preg, pyxi, rcla, rpip, rsnewb, rssoap, xtro];
  var frogMatch = [];
  for (var r = 0; r < data.length; r++) {
    var range = data[r][0].getRangeByName('all_data');
    var sheet = data[r][0].getSheetByName(data[r][1]);
    var frogObjects = getRowsData(sheet, range);
    for (var k = 0; k < frogObjects.length; k++) {
      for (var i = 0; i < genes.length; i++) {
        if (genes[i] == frogObjects[k].hsapSymbol) {
          frogObjects[k].frog = data[r][1];
          frogMatch.push(frogObjects[k]);
        }
      }
    }
  }
  return frogMatch;
}

function fuzzySearch(testWords) {
  Logger.log('fuzz');
  var wordObjects = getWordData();
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
    throw "Unable to find disease in our database. Please try a different search.";
  }
}

function matchLetters(word, wordObject) {
  Logger.log('match');
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
  if (comp < 4) {
    return true;
  }else{
    return false;
  }
}
  
function getHumanData() {
  //connects to the human gene/disease sheet and sends this information to getRowsData
  var humanSheet = ss.getSheetByName('disease_hgene');
  var humanRange = ss.getRangeByName('human_info');
  var humanObjects = getRowsData(humanSheet, humanRange);
  return humanObjects;    
}

function getWordData() {
  //connects to the word sheet and sends the info to getRowsData
  var wordSheet = ss.getSheetByName('word_search');
  var wordRange = ss.getRangeByName('word_counts');
  var wordObjects = getRowsData(wordSheet, wordRange);
  return wordObjects;
}
    
function getRowsData(sheet, range, columnHeadersRowIndex) {
  //collects the data from each row of the sheet and uses the headers as object keys
  columnHeadersRowIndex = columnHeadersRowIndex || range.getRowIndex() - 1;
  var numColumns = range.getLastColumn() - range.getColumn() + 1;
  var headersRange = sheet.getRange(columnHeadersRowIndex, range.getColumn(), 1, numColumns);
  var headers = headersRange.getValues()[0];
  return getObjects(range.getValues(), normalizeHeaders(headers));
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

function normalizeHeaders(headers) {
  //camelCases header from spreadsheet and removes non-alphnumeric characters
  //makes sure the header does not start with a number
  var keys = [];
  for (var i = 0; i < headers.length; i++) {
    var key = normalizeHeader(headers[i]);
    if (key.length > 0) {
      keys.push(key);
    }
  }
  return keys;
}

function normalizeHeader(header) {
  var key = "";
  var upperCase = false;
  for (var i = 0; i < header.length; i++) {
    var letter = header[i];
    if (letter == " " && key.length > 0) {
      upperCase = true;
      continue;
    }
    if (!isAlnum(letter)) {
      continue;
    }
    if (key.length == 0 && isDigit(letter)) {
      continue; // first character must be a letter
    }
    if (upperCase) {
      upperCase = false;
      key += letter.toUpperCase();
    } else {
      key += letter.toLowerCase();
    }
  }
  return key;
}

function isCellEmpty(cellData) {
  return typeof(cellData) == "string" && cellData == "";
}

function isAlnum(char) {
  return char >= 'A' && char <= 'Z' ||
    char >= 'a' && char <= 'z' ||
    isDigit(char);
}

function isDigit(char) {
  return char >= '0' && char <= '9';
}

