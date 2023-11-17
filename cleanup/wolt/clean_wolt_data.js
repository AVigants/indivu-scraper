const fs = require("fs");
const readline = require("readline");
const stream = fs.createReadStream("./wolt.ndjson", "utf8");
const rl = readline.createInterface({ input: stream });
const outputFile = "final_wolt_data.json";
const outputWriteStream = fs.createWriteStream(outputFile, {
  flags: "a",
  encoding: "utf8",
});

const normalizedString = (str) => {
  // Normalize accents and diacritics
  str = str.normalize("NFD").replace(/[\u0300-\u036f]/g, "");
  // Remove emojis
  str = str.replace(
    /[\u{1F600}-\u{1F64F}\u{1F300}-\u{1F5FF}\u{1F680}-\u{1F6FF}\u{1F900}-\u{1F9FF}\u{1F700}-\u{1F77F}\u{1F780}-\u{1F7FF}\u{1F800}-\u{1F8FF}\u{2600}-\u{26FF}\u{2700}-\u{27BF}\u{1F1E6}-\u{1F1FF}\u{1F191}-\u{1F251}\u{1F004}\u{1F0CF}\u{1F170}-\u{1F171}\u{1F17E}-\u{1F17F}\u{1F18E}]/gu,
    ""
  );
  // Replace multiple spaces and trailing spaces with one space
  str = str.replace(/\s+/g, " ").trim();
  // Convert to lowercase
  str = str.toLowerCase();
  // Replace spaces with dashes
  str = str.replace(/ /g, "-");

  return str;
};

const processRestaurant = (venue) => {
  return {
    bannerImage: venue.image_url,
    restaurantName: venue.name,
    description: venue.description,
    rating: venue.rating,
    openingTimesSchedule: venue.opening_times_schedule,
    deliveryTimesSchedule: venue.delivery_times_schedule,
    link: venue.share_url,
    deliveryMethods: venue.delivery_methods,
    address: venue.address,
    phone: venue.phone,
    deliveryBasePrice: venue.delivery_base_price,
  };
};

const processItems = (items, restaurantLink) => {
  return items.map((item) => ({
    name: item.name,
    price: item.baseprice,
    id: item.id,
    desc: item.description,
    img: item.image,
    link: `${restaurantLink}/${normalizedString(item.name)}-itemid-${
      item.id
    }`.replace(/\-\-/g, "-"),
  }));
};

rl.on("line", (line) => {
  const json = JSON.parse(line);
  let queries = JSON.parse(json.decoded_script).queries;

  let data = { restaurant: null, products: [] };
  let restaurantLink = "";

  // First pass: Find and form data.restaurant
  for (const query of queries) {
    if (query.state.data.venue) {
      data.restaurant = processRestaurant(query.state.data.venue);
      restaurantLink = data.restaurant.link;
      break; // Break after finding the first restaurant
    }
  }

  // Second pass: Form products data using restaurantLink
  for (const query of queries) {
    if (query.state.data.items && query.state.data.items.length > 0) {
      const products = processItems(query.state.data.items, restaurantLink);
      data.products.push(...products); // Append products to data.products array
    }
  }

  // Write processed data to output file
  if (data.restaurant || data.products.length > 0) {
    outputWriteStream.write(JSON.stringify(data) + "\n");
  }
});
rl.on("close", () => {
  outputWriteStream.end();
  console.log("Finished processing file");
});

outputWriteStream.on("error", (error) => {
  console.error("Error writing to output file:", error);
});
