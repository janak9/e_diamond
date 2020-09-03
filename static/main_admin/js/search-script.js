function reset()
{
  if(typeof window._gaq !== 'undefined')
  {
    _gaq.push(['_trackEvent', 'Icons', 'Reset']);
  }

  $('#search').val('');
  $('#catagory').val('');
  $('#release').val('');
  $('ul.icons li').show();
  $('ul.icons li').removeClass('active');
  $('.list').removeClass('detailed');
  $('.details').slideUp('fast');
  window.scrollTo(0, 0);
  $('#search').focus();
}

// Search for matching icons
function find_icons(evt)
{
  // Ignore moving around in input field with arrows
  if (typeof evt !== 'undefined' && ( evt.keyCode === 27 || evt.keyCode === 37 || evt.keyCode === 38 || evt.keyCode === 39 || evt.keyCode === 40 ))
  {
    return false;
  }

  // Update GUI
  $('ul.icons li').removeClass('active');
  $('.list').removeClass('detailed');
  $('.details').slideUp('fast');

  // Fetch Search Terms
  var value = $('#search').val().toLowerCase();
  // Check if we have a search term only
  if(value !== '')
  {
    $('ul.icons li').hide();
    $("ul.icons li[data-id*='"+value+"']").show();
    $("ul.icons li[data-aliases*='"+value+"']").show();
    $("ul.icons li[data-other*='"+value+"']").show();
  }
  else
  {
    $("ul.icons li").show();
  }

  // Check if the enter key was pressed, and if there was only one result
  if (typeof evt !== 'undefined' && evt.keyCode === 13) {
    $('#search').autocomplete('close');

    if($( "ul.icons li:visible" ).length === 1)
    {
      $("ul.icons li:visible").trigger('click');
    }
  }

  return false;
}

// Listen for Key Presses on Body
function navigate(evt)
{
  var prev = null,
    next = null,
    escape = 27,
    left = 37,
    up = 38,
    right = 39,
    down = 40,
    active = $('ul.icons li.active'),
    tag = evt.target;

  // Exit if we're inside an input field
  if (tag === 'input' || tag === 'textarea')
  {
    return false;
  }

  // Check if nothing is selected and that we are using a known key
  if (active.length === 0 && ( evt.keyCode === left || evt.keyCode === up || evt.keyCode === right || evt.keyCode === down ))
  {
    // $('ul.icons li:visible').first().trigger('click');

    if(typeof window._gaq !== 'undefined')
    {
      _gaq.push(['_trackEvent', 'Icons', 'Moved', 'Initialized']);
    }
  }
  // Something is selected so lets move around based on what key is pressed
  else
  {
    // Reset GUI
    if(evt.keyCode === escape)
    {
      reset();
    }
    // Jump one back at a time ( some might be hidden, so figure out which are visible )
    if(evt.keyCode === left)
    {
      prev = ($(active).prev(':visible').length >= 1) ? $(active).prev(':visible') : $(active).prevUntil(':visible').last().prev();
      prev.trigger('click');

      if(typeof window._gaq !== 'undefined')
      {
        _gaq.push(['_trackEvent', 'Icons', 'Moved', 'Left']);
      }
    }
    // Jump three back at a time ( some might be hidden, so figure out which are visible )
    else if(evt.keyCode === up)
    {
      var prev1 = ($(active).prev(':visible').length >= 1) ? $(active).prev(':visible') : $(active).prevUntil(':visible').last().prev();
      var prev2 = ($(prev1).prev(':visible').length >= 1) ? $(prev1).prev(':visible') : $(prev1).prevUntil(':visible').last().prev();
      var prev3 = ($(prev2).prev(':visible').length >= 1) ? $(prev2).prev(':visible') : $(prev2).prevUntil(':visible').last().prev();
      prev3.trigger('click');

      if(typeof window._gaq !== 'undefined')
      {
        _gaq.push(['_trackEvent', 'Icons', 'Moved', 'Up']);
      }
    }
    // Jump one forward at a time ( some might be hidden, so figure out which are visible )
    else if(evt.keyCode === right)
    {
      next = ($(active).next(':visible').length >= 1) ? $(active).next(':visible') : $(active).nextUntil(':visible').last().next();
      next.trigger('click');

      if(typeof window._gaq !== 'undefined')
      {
        _gaq.push(['_trackEvent', 'Icons', 'Moved', 'Right']);
      }
    }
    // Jump three forward at a time ( some might be hidden, so figure out which are visible )
    else if(evt.keyCode === down)
    {
      var next1 = ($(active).next(':visible').length >= 1) ? $(active).next(':visible') : $(active).nextUntil(':visible').last().next();
      var next2 = ($(next1).next(':visible').length >= 1) ? $(next1).next(':visible') : $(next1).nextUntil(':visible').last().next();
      var next3 = ($(next2).next(':visible').length >= 1) ? $(next2).next(':visible') : $(next2).nextUntil(':visible').last().next();
      next3.trigger('click');

      if(typeof window._gaq !== 'undefined')
      {
        _gaq.push(['_trackEvent', 'Icons', 'Moved', 'Down']);
      }
    }
  }
}
function selectText(elm)
{
  var range;
  if (document.selection)
  {
    range = document.body.createTextRange();
    range.moveToElementText(document.getElementById(elm));
    range.select();
  }
  else if (window.getSelection)
  {
    range = document.createRange();
    range.selectNode(document.getElementById(elm));
    window.getSelection().addRange(range);
  }
}


$(function() {

	var versions = [];
	var categories = [];
  var i;
  var option;

	function compare(a,b) {
		if (a.name.toLowerCase() < b.name.toLowerCase())
    {
      return -1;
    }
		if (a.name.toLowerCase() > b.name.toLowerCase())
    {
      return 1;
    }
		return 0;
	}

	icons.sort(compare);

	$.each(icons, function(index, value) {

		if(versions.indexOf(value.created) === -1)
		{
			versions.push(value.created);
		}

		var aliases = '';
		if(value.aliases)
		{
			$.each(value.aliases, function(alias_index, alias) {
				aliases += alias;
				if((alias_index + 1) < value.aliases.length)
				{
					aliases += ', ';
				}
			});
		}
    if(value.filter)
    {
      $.each(value.filter, function(alias_index, alias) {
        aliases += alias;
        if((alias_index + 1) < value.filter.length)
        {
          aliases += ', ';
        }
      });
    }

		var other_aliases = '';
		if(fa_icon_aliases[value.id])
		{
			for(i=0; i<fa_icon_aliases[value.id].length; i++)
			{
				other_aliases += fa_icon_aliases[value.id][i];
				if((i+1) < fa_icon_aliases[value.id].length)
				{
					other_aliases += ', ';
				}
			}
		}

		var icon_categories = '';
		for(i=0; i<value.categories.length; i++)
		{
			icon_categories += value.categories[i];
			if((i+1) < value.categories.length)
			{
				icon_categories += ', ';
			}

			if(categories.indexOf(value.categories[i]) === -1)
			{
				categories.push(value.categories[i]);
			}
		}

		var html = '<li data-order="'+index+'" data-member="'+value.member+'" data-id="'+value.id+'" data-aliases="'+aliases+'" data-other="'+other_aliases+'" data-unicode="'+value.unicode+'" data-categories="'+icon_categories+'" data-release="'+value.created+'">' +
			'<i class="'+value.member+' fa-'+value.id+'"></i>' +
			'<span>'+value.name+'<\/span>' +
			'<\/li>';
		$('.icons').append(html);
	});

	$('body').keyup(navigate);
	$('#search').keyup(find_icons);
	$('#release').change(find_icons);
	$('#catagory').change(find_icons);
	$('#reset').click(reset);

	versions.sort();
	versions.reverse();

	for(i=0; i<versions.length; i++)
	{
		option = '<option value="'+versions[i]+'">Version '+versions[i]+'</option>';
		$('#release').append(option);
	}

	categories.sort();

	for(i=0; i<categories.length; i++)
	{
		option = '<option value="'+categories[i]+'">'+categories[i]+'</option>';
		$('#catagory').append(option);
	}

	$( '#search' ).autocomplete({
		delay: 0,
		minLength: 2,
		source: function(request, response)
		{
			var availableTags = $.map(icons, function(icon)
			{
				return {
					label: icon.name,
					value: icon.id,
					member: icon.member
				};
			});

			response(
				$.ui.autocomplete.filter( availableTags, request.term )
			);
		},
		select: function(){
			setTimeout(find_icons, 100);

			setTimeout(function(){
				if($( 'ul.icons li:visible' ).length === 1)
				{
					 $('ul.icons li:visible').trigger('click');
				}
			}, 300);
		}
	}).autocomplete( 'instance' )._renderItem = function( ul, item ) {
		return $( '<li>' )
			.append( "<a><i class='"+item.member+" fa-fw fa-" + item.value + "'></i>&nbsp; " + item.label + "</a>" )
			.appendTo( ul );
	};

	$('ul.icons li').click(function(){
    const row_id = $("#social_link_id").val();
    if (row_id) {
      const data = $(this).data();
      const icon = `${data.member} fa-${data.id}`;
      console.log('icon: ', icon);
      console.log($('#'+row_id).find('i'));
      console.log($('#'+row_id).find('input[type=hidden]'));
      $('#'+row_id).find('i')[0].className = icon;
      $('#'+row_id).find('input[type=hidden]')[0].value = icon;
    } else {
      alert('please select link no');
    }
	});
});
