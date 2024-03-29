---
layout: page
title: LMSS UX API
description: Integrate the LMSS in your applications
nav-menu: false
show_tile: false
image: assets/images/api.jpg
---

<p style="font-size:0.75em"><a href="/">Home</a>&nbsp;&nbsp;>&nbsp;&nbsp;<a href="/api">API</a>&nbsp;&nbsp;>&nbsp;&nbsp;LMSS UX API
</p>
<!-- Main -->
<div id="main" class="alt">
	<!-- One -->
	<section>
		<header class="major">
			<h1>API</h1>
		</header>
		<h3>LMSS UX API</h3>
		<p>A series of static JSON API's that provide read-only access to the most up-to-date version of the LMSS Codes. Useful when you want to integrate LMSS in your own legal applications.</p>
	</section>
	
<input type="text" class="light-table-filter" data-table="order-table" placeholder="Enter one or more keywords to search the codes">
		<p>
		<div class="table-responsive">
		    <table class="table-wrapper order-table table">
		      <tbody>
		      <tr>
		        <th>
		        <span>Code Set</span></th>
		        <th>
		        <span>Code</span></th>
		        <th>API Endpoint</th>
		      </tr>
		      <tr>
		        <td><a href="/SALI-areas-of-law">SALI Area of Law</a></td> 
		        <td>SALI-AOL:2</td> 
		        <td><a href="/api/v1/SALI-AOL.json">lmss.io/api/v1/SALI-AOL.json 
		          </a></td> 
		      </tr>
		      <tr>
		        <td><a href="/SALI-court">SALI Court</a></td> 
		        <td>SALI-COURT</td> 
		        <td><a href="/api/v1/SALI-COURT.json">lmss.io/api/v1/SALI-COURT.json 
		          </a></td> 
		      </tr>
		      <tr>
		        <td><a href="/SALI-currency">SALI Currency (ISO 4217)</a></td> 
		        <td>ISO-4217</td> 
		        <td><a href="/api/v1/ISO-4257.json">lmss.io/api/v1/ISO-4257.json 
		          </a></td> 
		      </tr>
		      <tr>
		        <td><a href="/SALI-format">SALI Format</a></td> 
		        <td>SALI-FMT</td> 
		        <td><a href="/api/v1/SALI-FMT.json">lmss.io/api/v1/SALI-FMT.json 
		          </a></td> 
		      </tr>
		      <tr>
		        <td><a href="/SALI-governmental-body">SALI Governmental Body</a></td> 
		        <td>SALI-GOVT</td> 
		        <td><a href="/api/v1/SALI-GOVT.json">lmss.io/api/v1/SALI-GOVT.json 
		          </a></td> 
		      </tr>
		      <tr>
		        <td><a href="/SALI-industry">SALI Industry</a></td> 
		        <td>SALI-IND</td> 
		        <td>lmss.io/api/v1/SALI-AOL.json   
		          </td> 
		      </tr>
		      <tr>
		        <td><a href="/SALI-legal-entity">SALI Legal Entity</a></td> 
		        <td>SALI-LEGENT:2</td> 
		        <td><a href="/api/v1/SALI-LEGENT.json">lmss.io/api/v1/SALI-LEGENT.json 
		          </a></td> 
		      </tr>
		      <tr>
		        <td><a href="/SALI-LMSS-type">SALI LMSS Type</a></td> 
		        <td>SALI-LMST</td> 
		        <td><a href="/api/v1/SALI-LMST.json">lmss.io/api/v1/SALI-LMST.json 
		          </a></td> 
		      </tr>
		      <tr>
		        <td><a href="/SALI-LMSS-version">SALI LMSS Version</a></td> 
		        <td>SALI-VERS</td> 
		        <td><a href="/api/v1/SALI-VERS.js.io/api/v1/SALI-VERS.json"> lmss.io/api/v1/SALI-VERS.json </a></td>  
		      </tr>
		      <tr>
		        <td><a href="/SALI-location">SALI Location (Adapted ISO 3166-2)</a></td>
		        <td>SALI-ISO31662</td> 
		        <td><a href="/api/v1/SALI-ISO31662.json">lmss.io/api/v1/SALI-ISO31662.json 
		          </a></td>  
		      </tr>
		      <tr>
		        <td><a href="/SALI-matter-narrative">SALI Matter Narrative</a></td> 
		        <td>SALI-MATNAR</td> 
		        <td><a href="/api/v1/SALI-MATNAR.json">lmss.io/api/v1/SALI-MATNAR.json 
		          </a></td>  
		      </tr>
		      <tr>
		        <td><a href="/SALI-player-role">SALI Player Role</a></td> 
		        <td>SALI-PROLE</td> 
		        <td><a href="/api/v1/SALI-PROLE.json">lmss.io/api/v1/SALI-PROLE.json 
		          </a></td>  
		      </tr>
		      <tr>
		        <td><a href="/SALI-process">SALI Process</a></td> 
		        <td>SALI-PROC</td> 
		        <td><a href="/api/v1/SALI-PROC.json">lmss.io/api/v1/SALI-PROC.json 
		          </a></td> 
		      </tr>
		      <tr>
		        <td><a href="/SALI-process-status">SALI Process Status</a></td> 
		        <td>SALI-PROCSTAT</td> 
		        <td><a href="/api/v1/SALI-PROCSTAT.json">lmss.io/api/v1/SALI-PROCSTAT.json 
		          </a></td> 
		      </tr>
		      <tr>
		        <td><a href="/SALI-representation-role">SALI Representation Role</a></td>  
		        <td>SALI-RROLE</td> 
		        <td><a href="/api/v1/SALI-RROLE.json">lmss.io/api/v1/SALI-RROLE.json 
		          </a></td> 
		      </tr>
		      <tr>
		        <td><a href="/SALI-trial-type">SALI Trial Type</a></td>  
		        <td>SALI-TRITYP</td> 
		        <td><a href="/api/v1/SALI-TRITYP.json">lmss.io/api/v1/SALI-TRITYP.json 
		          </a></td> 
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

