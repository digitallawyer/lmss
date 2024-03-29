---
layout: page
title: Matter API
description: Integrate the LMSS in your applications
nav-menu: false
show_tile: false
image: assets/images/api.jpg
---

<p style="font-size:0.75em"><a href="/">Home</a>&nbsp;&nbsp;>&nbsp;&nbsp;<a href="/api">API</a>&nbsp;&nbsp;>&nbsp;&nbsp;Legal.io Matter API
</p>
<!-- Main -->
<div id="main" class="alt">
	<!-- One -->
	<section>
		<header class="major">
			<h1>API</h1>
		</header>
		<h3>Legal.io Matter API</h3>
		<p>A LMSS Instance API to create LMSS-conforming matters in the Legal.io network. Useful for legal departments and law firms to find high-quality lawyers and legal professionals. <em style="color:orange">Work in progress: check back soon!</em></p>
	</section>
</div>
<div>
	<div class="row 200%">
		<div class="6u 12u$(medium)">
			<form name="test_form">
				<br>
		        <div class="">
		            <div class="field" style="display: none;">
		            	<label for="given_name">Community API token</label>
		            	<input name="api_token" pattern=".+" required="animated-label" type="text" disabled="disabled" value="7b69c2e4-c1aa-4b69-888c-0a30f55556d2">
		            </div>
		            <div class="field">
		            	<label for="summary">Title *</label>
		            	<input  id="title_input" name="summary" pattern=".+" required="required" type="text" onkeyup="titleUpdateFunction()">
		            </div>
		            <div class="field">
		            	<label for="location">Location *</label>
		            	<input name="location" pattern=".+" required="animated-label" type="text">
		            </div>
		            <div class="field">
		            	<label for="content">Description *</label>
		            	<input name="content" pattern=".+" required="animated-label" type="text">
					</div>
					<div class="12u$ field">
						<label>Area of law *</label>
						<div class="select-wrapper">
							<select id="#PracticeAreas" class="multiselect" name="practice_areas"  data-placeholder="Select">
								<option value="CORP">Corporate Law    </option>
								<option value="CORP-BIZO">- Business Organizations</option>
							</select>
						</div>
					</div>
					<hr>
					<div class="field half first">
						<label for="given_name">First name *</label>
						<input id="given_name_input" name="given_name" pattern=".+" required="animated-label" type="text" onkeyup="myFunction()">
					</div>
		            <div class="field half">
		            	<label for="family_name">Last name</label>
		            	<input name="family_name" pattern=".+" required="animated-label" type="text">
		            </div>
		            <div class="field half first">
		            	<label for="email">Email</label>
		            	<input name="email" pattern=".+" required="animated-label" type="text">
		            </div>
		            <div class="field half">
		            	<label for="telephone">Telephone *</label>
		            	<input name="telephone" pattern=".+" required="animated-label" type="text">
		            </div>
					<div class="field pull-right">
		            	<button name="send_data" type="test" disabled="disabled">Next</button>
		            </div>
		            <div id="post_data">
		            <div id="response">
				        </div>
				    </div>
				</div>
			</form>
		</div>
		<div class="6u 12u$(medium)">
		<br>
		<label for="given_name">LMSS Representation</label>
		<pre><code>
{
   "document" : {
      "header" : {
         "lmss type" : "INST",
         "lmss version" : "1.02",
         "title" : "<span id="title_result">...</span>",
         "language" : "en-us",
         "charset" : "UTF-8"
      },
      "matter" : {
         "title" : "<span id="title_result2">...</span>",
         "locale" : "NAM-US-US+GA",
         "process" : {
            "process type" : "A",
            "description" : "...",
            "area of law" : "LEMP-WGHR",
            "player" : [{
               "name" : "<span id="given_name_result">...</span>",
               "industry" : "FAG"
            }]
         }
      }
   }
}
		</code></pre>
		</div>
	</div>



</div>
<script src="https://cdnjs.cloudflare.com/ajax/libs/jquery/3.4.1/jquery.min.js" integrity="sha256-CSXorXvZcTkaix6Yvo6HppcZGetbYMGWSFlBw8HfCJo=" crossorigin="anonymous"></script>
<script>

function titleUpdateFunction()
	{
    	var input = document.getElementById('title_input')
    	var div = document.getElementById('title_result');
    	var div2 = document.getElementById('title_result2');
    	div.innerHTML = input.value;
    	div2.innerHTML = input.value;
	}

function myFunction()
	{
    	var input = document.getElementById('given_name_input')
    	var div = document.getElementById('given_name_result');
    	div.innerHTML = input.value;
	}
jQuery(function() {
        var $form = jQuery('form[name="test_form"]')

        $form.find('button[name="send_data"]').on('click', function(e) {
            jQuery('#post_data').html('')
            jQuery('#response').html('')
            e.preventDefault()


            var data = {
                version: '1',
                inquiry: {
                    summary: $form.find('input[name="summary"]').val(),
                    content: $form.find('input[name="content"]').val(),
                    practice_areas: [],
                    location: $form.find('input[name="location"]').val(),
                },
                buyer: {
                    given_name: $form.find('input[name="given_name"]').val(),
                    family_name: $form.find('input[name="family_name"]').val(),
                    email: $form.find('input[name="email"]').val(),
                    telephone: $form.find('input[name="telephone"]').val(),
                    inquiry_location: $form.find('input[name="inquiry_location"]').val(),
                    /* address: {
                        address1: $form.find('input[name="address1"]').val(),
                        address2: $form.find('input[name="address2"]').val(),
                        city: $form.find('input[name="city"]').val(),
                        state: $form.find('input[name="state"]').val(),
                        zipcode: $form.find('input[name="zipcode"]').val(),
                        country: $form.find('input[name="country"]').val(),
                        county: $form.find('input[name="county"]').val(),
                    }, */
                },
            }

            jQuery('select[name="practice_areas"] option:selected').each(function() {
                data.inquiry.practice_areas.push(jQuery(this).text())
            })

            var json = JSON.stringify(data)
            var community_token = $form.find('input[name="api_token"]').val()
            var url = 'https://app.legal.io/api/v1/intake/new'
            var headers = {
                'X-LEGALIO-TOKEN': community_token,
                'Content-Type': 'application/json',
            }


            var nl = "<br/>\n"
            jQuery('#post_data').html(
                '<strong>Making api call</strong>' + nl +
                'Sending data to ' + url + nl
            )

            function output(data, textStatus) {
                if (textStatus === 'nocontent') {
                    jQuery('#response').html(
                        '<strong>Success reported</strong>' + nl
                    )
                } else {
                    jQuery('#response').html(
                        '<strong>API Response</strong>' + nl +
                        'Text status: ' + textStatus + '(' + data.status + ')' + nl +
                        'Output: ' + JSON.stringify(data.responseText)
                    )
                }
            }

            jQuery.ajax({
                type: 'post',
                url: url,
                data: json,
                headers: headers,
                success: output,
                error: output,
                dataType: 'json'
            })
        })
    });
</script>