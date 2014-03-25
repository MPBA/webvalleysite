/*
  Example:
  <script type="text/javascript" src="marks_widget.js"></script>
  <script type="text/javascript">
  mw_params.mandatory = ["mate","ing","inf"];
  mw_params.optional = ["ita","scie","geo","sto","bio"];
  mw_params.allow_other = true;
  $(marks_widget_init);
  </script>

  <form action="#" method="post" enctype="multipart/form-data">
  Name: <input type="text" name="name"/><br/>
  <span name="sem_1" id="sem_1" class="marks_widget"></span><br/>
  <!-- Don't forget to specify name and id in .marks_widget elements -->
  <input type="submit"/>
  </form>
*/

var mw_params = {
    other_text: "Other",
    other_suggestion: "Type the subject name",
    select_text: "[Choose]",
    remove_button: "<span class='close' style='float:none;'> &times;</span>",
    add_button: "<span class='btn btn-small'>Add field</span>"
}
var mw_globals = {
    'counter': 0,
    'prev_val': null
};

function toplaceholder(container_id){
    return container_id + '_placeholder';
}
function id_to_name(container_id){
    return $("#"+container_id).attr('name');
}

function option_focused(){
    //console.log(this.value)
    mw_globals['prev_val'] = this.value;
}
function option_changed(){
    var val = $(this).find("option:selected").get(0).value;
    if (val !== mw_params.other_text){
	var container = $(this).parent().parent();
	// remove the selected value from every other possible list
	if (val !== '' && val !== mw_params.other_text){
	    container.find("select option[value='"+val+"']").not(":selected").hide();
	}
	// restore my old value in the other selects
	var prev_val = mw_globals['prev_val'];
	mw_globals['prev_val'] = null;
	if (prev_val !== '' && prev_val !== null){
	    container.find("select option[value='"+prev_val+"']").show();
	}
    }
    else{ // val == mw_params.other_text
	var id = this.id;
	var name = this.name;
	//var br = $(this).parent().next('br');
	//$(this).parent().parent().find(".mw_placeholder").before($(this));
	//$(this).parent().after(br);
	$(this).replaceWith("<input id='"+id+"' name='"+name+"' type='text' class='marks_widget_key' value='"+mw_params.other_suggestion+"' />");
    }
}

function mw_add_optional_field(container_id){
    // adds the field and returns the span id
    var placeholder_id = toplaceholder(container_id);
    var container_name = id_to_name(container_id);
    var i = mw_globals['counter']++;
    var id = container_id + "_" + i;
    var kid = id + "_key";
    var vid = id + "_val";
    var name = container_name + "_" + i;
    var kname = name + "_key";
    var vname = name + "_val";
    
    $('#'+placeholder_id)
	.before("<span id='"+id+"' class='marks_widget_optional'>" +
		"<select id='"+kid+"' name='"+kname+"' class='marks_widget_key'>" +
		// <option>s attached later
		"</select> " +
		"<input type='text' id='"+vid+"' name='"+vname+"' class='marks_widget_val'>" +
		"</span><br/>");
    // Add options
    var sel_tag = $('#'+kid);
    sel_tag.append("<option value=''>"+mw_params.select_text+"</option>");
    for (var i in mw_params[container_name].optional){
	sel_tag.append("<option value='"+mw_params[container_name].optional[i]+"'>"+mw_params[container_name].optional[i]+"</option>");
    }	
    $("#"+container_id+" .marks_widget_optional option:selected").each(function(i, elem){
	if(elem.value !== ''){
	    sel_tag.find("option[value='"+elem.value+"']").hide();
	}
    });
    if (mw_params[container_name].allow_other){
	sel_tag.append("<option class='other' value='"+mw_params.other_text+"'>"+mw_params.other_text+"</option>");
    }
    sel_tag.focus(option_focused).change(option_changed);
    // Add remove button
    $('#'+id).append("<span class='marks_widget_del'>"+mw_params.remove_button+"</span>").
	find(".marks_widget_del").click(function(){
	    var sel_tag = $(this).siblings("select").find("option:selected");
	    if (sel_tag.length !== 0){ //there is a select tag, i.e this is not an "other" line
		var val = sel_tag.get(0).value;
		var container = $(this).parent().parent();
		if (val !== '' && val !== null){
		    container.find("select option[value='"+val+"']").show();
		}
	    }
	    $(this).parent().next("br").remove();
	    $(this).parent().remove();
	});
    return id;
}

function mw_add_mandatory_field(container_id, field_name){
    var placeholder_id = toplaceholder(container_id);
    var m = field_name;
    var i = mw_globals['counter']++;
    var id = container_id + "_" + i;
    var kid = id + "_key";
    var vid = id + "_val";
    var name = id_to_name(container_id) + "_" + i;
    var kname = name + "_key";
    var vname = name + "_val";
    $('#'+placeholder_id)
	.before("<span id='"+id+"' class='marks_widget_mandatory'>" +
		//"<select id='"+kid+"' name='"+kid+"' class='marks_widget_key' readonly='readonly'>" +
		//"<option value='"+m+"'>"+m+"</option>" +
		//"</select>" +
		"<input type='text' id='"+kid+"' name='"+kname+"' class='marks_widget_key' value='"+m+"' readonly='readonly'> " +
		"<input type='text' id='"+vid+"' name='"+vname+"' class='marks_widget_val'>" +
		"</span>" +
		"<br/>");
}

function mw_init(container_id){
    var container = $('#'+container_id);
    var container_name = id_to_name(container_id);
    var value = container.find(".field_content").text(); // contains initial data info
    container.empty();
    container.append("<span id='"+toplaceholder(container_id)+"' class='mw_placeholder'>"+mw_params.add_button+"</span>");
    $('#'+toplaceholder(container_id)).click(function(){
	mw_add_optional_field(container_id);
    });
    for (var m in mw_params[container_name].mandatory){
	mw_add_mandatory_field(container_id, mw_params[container_name].mandatory[m]);
    }
    // SET INITIAL VALUES
    // parse input data
    var data = $.parseJSON(value);
    console.log(data);
    keys = data[0];  vals = data[1];
    dict = {};
    for (var i in keys){
	// add the key[i]:val[i] pair only if both are not empty
	if (keys[i] && (i in vals))
	    if (vals[i])
		dict[keys[i]] = vals[i];
    }
    console.log(dict);
    // set mantatory field values
    $.each(mw_params[container_name].mandatory, function(i, elem){
	if (elem in dict){ 
	    container.find(".marks_widget_key[value='"+elem+"']").
		parent().find(".marks_widget_val").attr('value',dict[elem]);
	    delete dict[elem];
	}
    });
    console.log(dict);
    // set optional field values
    $.each(dict, function(key, val){
	var new_id = mw_add_optional_field(container_id);
	var new_field = $("#"+new_id);
	if ($.inArray(key, mw_params[container_name].optional) !== -1){ // if it's optional 
	    new_field.find(".marks_widget_key").val(key);
	    new_field.find(".marks_widget_val").val(val);
	}
	else if (mw_params[container_name].allow_other){
	    new_field.find(".marks_widget_key").val(mw_params.other_text);
	    mw_globals.prev_val = null;
	    new_field.find(".marks_widget_key").change();
	    new_field.find(".marks_widget_key").val(key);
	    new_field.find(".marks_widget_val").val(val);
	}
    });
}

function marks_widget_init(container_name) {
    if (!('mandatory' in mw_params[container_name] &&
	  'optional' in mw_params[container_name] &&
	  'allow_other' in mw_params[container_name])){
	console.log("marks_widget: error: unspecified required argument(s).");
	console.log("marks_widget: info:  required arduments are mw_params[container_name].mandatory, .optional and .allow_other");
    }
    containers = $(".marks_widget[name="+container_name+"]"); //sould be only one
    containers.each(function(c_index, elem){
	if(elem.id){
	    mw_init(elem.id);
	}
	else{
	    console.log("marks_widget: error: got a .marks_widget container without id.");
	}
    });

}
