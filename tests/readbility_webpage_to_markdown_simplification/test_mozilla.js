const jsdom = require("jsdom");
const { JSDOM } = jsdom;
doc = new jsdom.JSDOM("<body>Look at this cat: <img src='./cat.jpg'></body>");
const { Readability } = require('@mozilla/readability');
let reader = new Readability(doc.window.document);
article = reader.parse();
console.log(article);