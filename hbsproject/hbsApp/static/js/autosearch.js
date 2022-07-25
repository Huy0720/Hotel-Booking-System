$.widget( "ui.autocomplete", $.ui.autocomplete, {
	options: {
		maxItems: 9999
	},
	_renderMenu: function( ul, items ) {
		var that = this,
			count = 0;
		$.each( items, function( index, item ) {
			if ( count < that.options.maxItems ) {
				that._renderItemData( ul, item );
			}
			count++;
		});
	} 
});



var data = [];
$.getJSON('http://127.0.0.1:5500/destinations_filtered.json', function(result) {
	$.each(result, function(index, val) {
		data.push(val.term)
	});
});


$("#destination").autocomplete({
	source: data,
	maxItems: 20
}).data("ui-autocomplete")._renderItem = function( ul, item ) {
	let txt = String(item.value).replace(new RegExp(this.term, "gi"), "<span class='highlight'>$&</span>");;
	return $("<li></li>")
		.data("ui-autocomplete-item", item)
		.append("<div>" + txt + "</div>")
		.appendTo(ul);
};



