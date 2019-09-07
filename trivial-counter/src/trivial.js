const escomplex = require('escomplex');
const fs = require('fs')
const process = require('process')

var total_lines = 0
var total_cyclomatic = 0

function updateResult(){
  var result = {};
  result["check_id"] = "trivial";
  result["path"] = "";
  result["extra"] = {};
  result["extra"]["LOC"] = total_lines;
  result["extra"]["Cyclomatic"] = total_cyclomatic;
  var all_results = [];
  all_results.push(result);

  fs.writeFile("/analysis/output/output.json", JSON.stringify({"results": all_results}, null, 4), function(err){
    if(err){
      throw err;
    }
  });
}


function checkTrivial(path, index, final){
  fs.readFile(path, (err,data) => {
    if(err) throw err;

    data = data.toString();
    lines = data.split("\n");
    total_lines += lines.length - 1;
    cyclomatic = 0;
    lines.forEach(function(line){
      try{
        var complex_result = escomplex.analyse(line);
        cyclomatic += complex_result.aggregate.cyclomatic
      }
      catch(err){
      }
    });

    total_cyclomatic = cyclomatic;
    if(index == final){
      updateResult();
    }
  });
}

process.argv.forEach(
  function(value, index, array){
    if(index>=2){
      var final = process.argv.length - 1;
      checkTrivial(value, index, final);
    }
  }
);
