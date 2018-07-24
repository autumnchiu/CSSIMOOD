var slider = document.getElementById("myRange");
var output = document.getElementById("demo");

output.innerHTML = slider.value; // Display the default slider value


var reasonInput = document.getElementById("reasonInput");
// output.innerHTML = slider.value;
print(reasonInput)
// Update the current slider value (each time you drag the slider handle)
slider.oninput = function() {
    output.innerHTML = this.value;
    // var slider = document.getElementById("myRange");
    var output = document.getElementById("reasonInput");
    // output.innerHTML = slider.value;
    print(output)

}
