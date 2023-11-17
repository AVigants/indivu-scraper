const csv = require("csv-parser");
const fs = require("fs");
let arr = [];
// ----- variables & general functions -----
function readFile(path) {
  let input = fs.readFileSync(path, "utf8");
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

// step 1: remove objects with no nutritional information
function removeNutInfoNulls(input, output) {
  let inputArr = readFile(input);
  for (let i = 0; i < inputArr.length; i++) {
    let obj = inputArr[i];
    if (obj.data["nutritional information"]) {
      arr.push(obj);
    }
  }

  writeFile(output, arr);
}
// removeNutInfoNulls("barbora.json", "barbora2.json");

// step 2 - clean data
function combDetails(input, output) {
  let inputArr = readFile(input);
  for (let i = 0; i < inputArr.length; i++) {
    let obj = inputArr[i];

    // product price
    obj.data["product price"] = Number(
      obj.data["product price"].replace(/,/g, ".").replace(/€/g, "")
    );

    // measured in
    obj.data["product measured in"] = /\/.*|Depozīts/
      .exec(obj.data["product measured in raw"])[0]
      .replaceAll("/", "");

    let amount = "";
    let title = obj.data["product name"].toLowerCase().replaceAll(",", ".");

    const match = title.match(/(\d+(\.\d+)?\s*[gmlL]{1,2}(?=\s|$))|(\bkg\b)/);
    if (match) {
      if (match[0] === "kg") {
        amount = "1kg";
      } else {
        amount = match[0];
      }
    }

    if (!amount && title.includes("1kg")) {
      amount = "1kg";
    }

    // remove quotes
    for (let key in obj.data) {
      if (typeof obj.data[key] === "string") {
        obj.data[key] = obj.data[key].replace(/"/g, "'");
      }
    }

    // format data so its more like rimi json
    obj["product name"] = obj.data["product name"];
    obj["prodict link"] = obj.link;
    obj["product picture"] = obj.data["product picture"];
    obj["product price"] = obj.data["product price"];
    obj["product measured in"] = obj.data["product measured in"];
    obj["ingredients"] = obj.data["product ingredients"];
    obj["nutrition facts"] = obj.data["nutritional information"];
    obj["amount"] = amount;

    // remove data obj
    delete obj.data;
    delete obj.link;

    arr.push(obj);
  }

  writeFile(output, arr);
}
combDetails("barbora2.json", "barbora3.json");
