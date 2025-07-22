//this is a java script file
const fileInput = document.getElementById('pic');
const previewSection = document.getElementById('preview');
const previewImage = document.getElementById('previewImage');
const loadingSection = document.getElementById('load');
const resultsSection = document.getElementById('results');
const uploadArea = document.querySelector('.upl-area');

let detectionActive = false;
let uplimgpath = null;
