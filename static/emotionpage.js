var slider = document.getElementById("myRange");
var intensity = document.getElementById("intensity");

intensity.innerHTML = slider.value; // Display the default slider value


var reasonInput = document.getElementById("reasonInput");
// output.innherHTML = slider.value;
console.log(intensity)
// Update the current slider value (each time you drag the slider handle)
slider.oninput = function() {
    var intensity = document.getElementById("intensity");
    console.log(intensity)
    intensity.innerHTML = this.value;

}
