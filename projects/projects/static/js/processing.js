
// This function is to set the focus when the page loads for CTL, NCTL and Reshearing operations
function setFocusToTextBox(operation){
    if(operation == "CTL" || operation == "Narrow CTL"){
        document.getElementById("output_length").focus();
    }
    if(operation == "Reshearing"){
        document.getElementById("output_width").focus();
    }
}


// This function is to set the focus when the page loads for slitting operation
function setFocusToTextBox_Slit(){

        document.getElementById("total_length").focus();

}


// This function calculates the weight for CTL, NCTL and Reshearing functions
function for_packets_and_weight(table_id,table_row,operation){

   // Get the row where the change was made and calculate the weight of the processed material
	var rowCount = table_row.offsetParent.parentElement.rowIndex;
	var last_row = document.getElementById(table_id).rows[rowCount];
	var numbers = Number(last_row.cells[4].lastChild.value);
	var thk = Number(document.getElementById('thickness').value);
	var weight_pos = 6;

    var width =  Number(last_row.cells[0].lastChild.value);
    var length =  Number(last_row.cells[1].lastChild.value);

    numbers =  Number(last_row.cells[4].lastChild.value);
    weight_pos = 6;

    var weight = (thk * width * length * numbers * 0.00000785)/1000;
    last_row.cells[weight_pos].lastChild.value = weight.toFixed(3);
    var rm_weight = Number(document.getElementById("weight").value);

    calculate_wt_and_cuts(table_id);
}

// To calculate processed weight and no of cuts every time numbers are changed
function calculate_wt_and_cuts(table_id){
    var table = document.getElementById(table_id);
    var total_processed_wt =0;
    var total_cuts = 0;
    for (var i = 1, row; row = table.rows[i]; i++) {
        total_processed_wt += Number(row.cells[6].lastChild.value);
        total_cuts += Number(row.cells[4].lastChild.value);
    }
    document.getElementById("total_processed_wt").value = Number(total_processed_wt.toFixed(3));
    document.getElementById("total_cuts").value = total_cuts;
}

function time_taken(){
   var t1 = document.getElementById("start_time").value;
   var t2 = document.getElementById("end_time").value;
   var parts = t1.split(':');
   var d1 = Number(parts[0])*60 + Number(parts[1]);
   parts = t2.split(':');
   var d2 = Number(parts[0])*60 + Number(parts[1]);
   // this would also work
   // d2.toTimeString().substr(0, d2.toTimeString().indexOf(' '));
   if(d2>d1){
    var diff =  d2 - d1;
    document.getElementById("processing_time").value = diff;
   }
   else{
    document.getElementById("end_time").value = "";
    alert("Please re-enter the time. End time must be greater than start time");
    document.getElementById("start_time").focus();
   }
}

function time_taken_setting(){
   var t1 = document.getElementById("setting_start_time").value;
   var t2 = document.getElementById("setting_end_time").value;
   var parts = t1.split(':');
   var d1 = Number(parts[0])*60 + Number(parts[1]);
   parts = t2.split(':');
   var d2 = Number(parts[0])*60 + Number(parts[1]);
   // this would also work
   // d2.toTimeString().substr(0, d2.toTimeString().indexOf(' '));
   if(d2>=d1){
    var diff =  d2 - d1;
    document.getElementById("setting_time").value = diff;
   }
   else{
    document.getElementById("setting_end_time").value = "";
    alert("Please re-enter the time. End time must be greater than start time");
    document.getElementById("setting_start_time").focus();
   }
}

//Calculates processed weight for slitting
function get_part_weight(){
    var total_length = Number(document.getElementById("total_length").value);

    var thickness = Number(document.getElementById("thickness").value);
    var input_material = (document.getElementById("input_material").value);
    input_material = input_material.split("x");

    var width = Number(input_material[0]);
    incoming_wt = Number(document.getElementById("inc_weight").value);

    var total_processed_wt = thickness * width * total_length * 0.00000785;
    var coil_length = incoming_wt/thickness/width/0.00000785;
    if ((coil_length > 0.9*total_length) && (coil_length < 1.1*total_length))
    {
        document.getElementById("processed_wt").value = incoming_wt;
    }else{
        document.getElementById("processed_wt").value = total_processed_wt.toFixed(3);
    }


}

function addRow(tableID)
	 {

			var table = document.getElementById(tableID);

			var rowCount = table.rows.length;
			var row = table.insertRow(rowCount);

			var last_row = document.getElementById(tableID).rows[rowCount-1];

			var colCount = table.rows[1].cells.length;

			for(var i=0; i<colCount; i++) {

				var newcell	= row.insertCell(i);

				newcell.innerHTML = table.rows[1].cells[i].innerHTML;
				//alert(newcell.childNodes);
				switch(newcell.childNodes[0].type) {
					case "text":
							newcell.childNodes[0].value = "";
							break;
					case "checkbox":
							newcell.childNodes[0].checked = false;
							break;
					case "select-one":
							newcell.childNodes[0].selectedIndex = 0;
							break;
				}
			}
		}