function setFocusToTextBox(){
    document.getElementById("actual_no_of_pieces").focus();
}

function setFocusToTextBox_Slit(){
    document.getElementById("total_length").focus();
}

function for_packets_and_weight(table_id,table_row,fg_yes_no,thk,width,length){

   // var table = document.getElementById(table_id);
	var rowCount = table_row.offsetParent.parentElement.rowIndex;
	var last_row = document.getElementById(table_id).rows[rowCount];

    if(fg_yes_no == "WIP"){
        last_row.cells[3].lastChild.value = "0";
        last_row.cells[3].lastChild.readOnly = true;
    }
    else{
        last_row.cells[3].lastChild.readOnly = false;
    }
    var weight = (Number(thk) * Number(width) * Number(length) * Number(table_row.value) * 0.00000785)/1000;
    last_row.cells[5].lastChild.value = weight.toFixed(3);
    var total_processed_wt = Number(document.getElementById("total_processed_wt").value) + Number(weight.toFixed(3));
    document.getElementById("total_processed_wt").value = Number(total_processed_wt.toFixed(3));
    var cuts = Number(last_row.cells[3].lastChild.value) + Number(document.getElementById("total_cuts").value);
    document.getElementById("total_cuts").value = cuts;

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

function get_part_weight(){
    var total_length = Number(document.getElementById("total_length").value);
    var no_of_parts = Number(document.getElementById("actual_no_of_packets").value);
    var thickness = Number(document.getElementById("thickness").value);
    var width = Number(document.getElementById("width").value);

    var length_per_part = total_length/no_of_parts;

    var total_processed_wt = thickness * width * total_length * 0.00000785;

    document.getElementById("actual_no_of_pieces").value = length_per_part.toFixed(3);
    document.getElementById("processed_wt").value = total_processed_wt.toFixed(3);
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