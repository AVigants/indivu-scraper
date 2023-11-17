const csv = require("csv-parser");
const fs = require("fs");
let arr = [];
// ----- variables & general functions -----
function readFile(path) {
  let input = fs.readFileSync("rimi2.json", "utf8");
  let data = JSON.parse(input);

  return data;
}
function writeFile(path, data) {
  if (typeof data !== "object") {
    data = JSON.stringify(data);
  }
  fs.writeFileSync(path, JSON.stringify(arr));
}

// ----- data cleaning in steps -----

//step 0: turn csv to JSON

function csv2Json(input, outputFile) {
  const output = [];

  fs.createReadStream(input)
    .pipe(csv())
    .on("data", (row) => {
      output.push(row);
    })
    .on("end", () => {
      fs.writeFileSync(outputFile, JSON.stringify(output, null, 2));
      console.log("CSV to JSON conversion complete.");
    });
}
// csv2Json('rimi.csv','rimi.json')

// step 1: remove Null objects
function removeNulls(input, output) {
  let inputArr = readFile(input);
  for (let i = 0; i < inputArr.length; i++) {
    let obj = inputArr[i];
    let discard = false;

    for (const [key, value] of Object.entries(obj)) {
      if (value === null || value === "null" || value === "") {
        discard = true;
        break;
      }
    }

    if (!discard) {
      arr.push(obj);
    }
  }

  writeFile(output, arr);
}
// removeNulls("rimi.json", "rimi2.json");

// step 2

//step 3: clean data
function combDetails(input, output) {
  let inputArr = readFile(input);
  for (let i = 0; i < inputArr.length; i++) {
    let obj = inputArr[i];

    let details = obj["product details raw"];
    let priceRaw = obj["product price raw"];
    if (/\d[\s\S]*€/.test(priceRaw)) {
      priceRaw.replace(/\n/g, ";;");
    }

    obj["product price"] = null;
    obj["product measured in"] = null;
    obj["country"] = null;
    obj["brand"] = null;
    obj["producer"] = null;
    obj["amount"] = null;
    obj["ingredients"] = null;
    obj["nutrition facts"] = null;

    // product price
    let priceMatch = /(\d+)\n(\d+)\n€ \/([a-z]+)/.exec(priceRaw);
    if (priceMatch) {
      obj["product price"] = `${priceMatch[1]}.${priceMatch[2]}`;
      obj["product measured in"] = priceMatch[3];
    }

    //country
    if (details.includes("Country of origin")) {
      obj["country"] = /Country of origin\n(.*)\n/.exec(details)[1];
    }

    //brand
    if (details.includes("\nBrand\n")) {
      obj["brand"] = /Brand\n(.*)\n/.exec(details)[1];
    }

    //producer
    if (details.includes("\nProducer\n")) {
      obj["producer"] = /Producer\n(.*)\n/.exec(details)[1];
    }

    //amount
    if (details.includes("\nAmount\n")) {
      obj["amount"] = /Amount\n(.*)\n/.exec(details)[1];
    }

    //ingredients
    if (details.includes("\nIngredients\n")) {
      obj["ingredients"] = /Ingredients\n(.*)\n/.exec(details)[1];
    }

    //nutrition facts
    if (details.includes("\nNutrition Facts\n")) {
      obj["nutrition facts"] = /Nutrition Facts\n([\s\S]*)/.exec(details)[1];
    }

    // remove quotes
    for (let key in obj) {
      if (typeof obj[key] === "string") {
        obj[key] = obj[key].replace(/"/g, "'");
      }
    }

    // remove raw fields
    delete obj["product price raw"];
    delete obj["product details raw"];

    arr.push(obj);
  }

  writeFile(output, arr);
}
combDetails("rimi2.json", "rimi3.json");
