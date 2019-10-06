---
layout: page-wide
title: SALI Representation Role
nav-menu: false
show_tile: false
---

<!-- Main -->
<div id="main" class="alt">
	<!-- One -->
	<section>
		<header class="major">
			<h1>SALI Representation Role</h1>
		</header>
		<input type="text" class="light-table-filter" data-table="order-table" placeholder="Enter one or more keywords to search the codes">
		<p>
		<div class="table-responsive">
    <table class="table-wrapper order-table table">
      <tbody>
      <tr>
        <th class="text-right" scope="col">#</th>
 
        <th scope="col">
        <span class="Sorter"><a href="code.php?s_keyword=&amp;ct=13&amp;lvl=&amp;psize=1000&amp;gridOrder=Sorter_ct_name&amp;gridDir=ASC" id="gridSorter_ct_name">Code Set</a> 
        
        </span></th>
 
        <th scope="col">
        <span class="Sorter"><a href="code.php?s_keyword=&amp;ct=13&amp;lvl=&amp;psize=1000&amp;gridOrder=Sorter_bb_level&amp;gridDir=ASC" id="gridSorter_bb_level">Level</a> 
        
        </span></th>
 
        <th scope="col">
        <span class="Sorter"><a href="code.php?s_keyword=&amp;ct=13&amp;lvl=&amp;psize=1000&amp;gridOrder=Sorter_bb_code&amp;gridDir=ASC" id="gridSorter_bb_code">Code</a> 
        
        </span></th>
 
        <th scope="col">
        <span class="Sorter"><a href="code.php?s_keyword=&amp;ct=13&amp;lvl=&amp;psize=1000&amp;gridOrder=Sorter1&amp;gridDir=ASC" id="gridSorter1">Full Code</a> 
        
        </span>&nbsp;</th>
 
        <th scope="col">
        <span class="Sorter"><a href="code.php?s_keyword=&amp;ct=13&amp;lvl=&amp;psize=1000&amp;gridOrder=Sorter_bb_shortname&amp;gridDir=ASC" id="gridSorter_bb_shortname">Short Name</a> 
        
        </span></th>
 
        <th scope="col">
        <span class="Sorter"><a href="code.php?s_keyword=&amp;ct=13&amp;lvl=&amp;psize=1000&amp;gridOrder=Sorter_bb_name&amp;gridDir=ASC" id="gridSorter_bb_name">Name</a> 
        
        </span>&nbsp;</th>
 
        <th scope="col">
        <span class="Sorter"><a href="code.php?s_keyword=&amp;ct=13&amp;lvl=&amp;psize=1000&amp;gridOrder=Sorter_bb_description&amp;gridDir=ASC" id="gridSorter_bb_description">Description</a> 
        
        </span></th>
 
        <th scope="col">
        <div class="pull-right">
          
        </div>
        </th>
      </tr>
 
      
      <tr>
        <td class="text-right">1&nbsp;</td> 
        <td>SALI Representation Role&nbsp;</td> 
        <td>1&nbsp;</td> 
        <td>BARR&nbsp;</td> 
        <td>BARR&nbsp;</td> 
        <td>Barrister&nbsp;</td> 
        <td>Barrister&nbsp;</td> 
        <td>A barrister represents clients in open court and may appear at the bar.<br>
          </td> 
        <td>
          <div class="pull-right">
            
          </div>
        </td>
      </tr>
 
      <tr>
        <td class="text-right">2&nbsp;</td> 
        <td>SALI Representation Role&nbsp;</td> 
        <td>1&nbsp;</td> 
        <td>COUN&nbsp;</td> 
        <td>COUN&nbsp;</td> 
        <td>Counsel/Attorney&nbsp;</td> 
        <td>Counsel/Attorney&nbsp;</td> 
        <td>The attorney or attorneys representing the player. A counsel or a counsellor at law is a person who gives advice and deals with various issues, particularly in legal matters. It is a title often used interchangeably with the title of lawyer.<br><strong>Tags:</strong> attorney; counsellor<br>
          </td> 
        <td>
          <div class="pull-right">
            
          </div>
        </td>
      </tr>
 
      <tr>
        <td class="text-right">3&nbsp;</td> 
        <td>SALI Representation Role&nbsp;</td> 
        <td>1&nbsp;</td> 
        <td>LCOUN&nbsp;</td> 
        <td>LCOUN&nbsp;</td> 
        <td>Local Counsel&nbsp;</td> 
        <td>Local Counsel&nbsp;</td> 
        <td>Local Counsel is a local attorney hired in a particular jurisdiction for the purposes of supporting a pro hac vice admission. Admission Pro Hac Vice (for this occasion only) means temporary admission of an out-of-state lawyer to practice before a court in a specific case or a set of cases. In almost all U.S. jurisdictions, attorneys who practice pro hac vice must do so with a local lawyer acting as local counsel.<br>
          </td> 
        <td>
          <div class="pull-right">
            
          </div>
        </td>
      </tr>
 
      <tr>
        <td class="text-right">4&nbsp;</td> 
        <td>SALI Representation Role&nbsp;</td> 
        <td>1&nbsp;</td> 
        <td>SOLI&nbsp;</td> 
        <td>SOLI&nbsp;</td> 
        <td>Solicitor&nbsp;</td> 
        <td>Solicitor&nbsp;</td> 
        <td>A solicitor meets prospective clients, hears the client's problems, gives legal advice, drafts letters and documents, negotiates on the client's behalf, and prepares the client's case for trial.<br>
          </td> 
        <td>
          <div class="pull-right">
            
          </div>
        </td>
      </tr>
 
      
      <tr>
        <td class="text-center" colspan="9">
          <nav aria-label="Page navigation">
          <ul class="pagination">
            
          </ul>
          </nav>
        </td>
      </tr>
    </tbody></table>
  </div>
<script type="text/javascript">
	
(function(document) {
	'use strict';

	var LightTableFilter = (function(Arr) {

		var _input;

		function _onInputEvent(e) {
			_input = e.target;
			var tables = document.getElementsByClassName(_input.getAttribute('data-table'));
			Arr.forEach.call(tables, function(table) {
				Arr.forEach.call(table.tBodies, function(tbody) {
					Arr.forEach.call(tbody.rows, _filter);
				});
			});
		}

		function _filter(row) {
			var text = row.textContent.toLowerCase(), val = _input.value.toLowerCase();
			row.style.display = text.indexOf(val) === -1 ? 'none' : 'table-row';
		}

		return {
			init: function() {
				var inputs = document.getElementsByClassName('light-table-filter');
				Arr.forEach.call(inputs, function(input) {
					input.oninput = _onInputEvent;
				});
			}
		};
	})(Array.prototype);

	document.addEventListener('readystatechange', function() {
		if (document.readyState === 'complete') {
			LightTableFilter.init();
		}
	});

})(document);

</script>