---
layout: page
title: LMSS Structure
description: An in-depth overview of the structure of LMSS
nav-menu: true
show_tile: true
image: assets/images/structure.jpg
---

<p style="font-size:0.75em"><a href="/">Home</a>&nbsp;&nbsp;>&nbsp;&nbsp;LMSS Structure</p>
<div id="main" class="alt">
	<!-- One -->
	<section>
		<header class="major">
			<h1>LMSS Structure</h1>
		</header>
		<h3>1. Overview</h3>
		<p>The LMSS document is comprised of a Header and one or more Matters. The Header and the Matter(s) are containers. Each container has elements that may be of type Text, Numeric, Enumeration or Container. Enumerations are stored in Text(250) fields to accommodate multiple levels of specificity that are represented as concatenated codes. Containers are pointers to other structures.
		</p>
		<p>A well-formed Document is a structure that includes all required fields. (Note that the concept of a well-formed document applies to instance but not templates or queries.) In the tables below, “REQ” indicates whether the element is required (in an LMSS instance but not a query), “MULT” indicates whether multiple values are permitted. A well-formed document is required in the interchange of instances of matters between systems. A well-formed document is not required when the LMSS is used in a query. In those instances, a missing field matches all instances. See LMSS Queries below.
		</p>
		<h3>2. Document</h3>
		<p>The Document container is the top-level container in the LMSS instance. The Document must have a Header and one or more Matters.</p>
		<b>Document container elements</b>
		<table>
			<tr>
				<th>ELEMENT<br></th>
				<th>REQ</th>
				<th>MULT</th>
				<th>TYPE</th>
				<th>COMMENTS</th>
			</tr>
			<tr>
				<td>Header</td>
				<td>Y</td>
				<td>N</td>
				<td>Container</td>
				<td>The header information for the document.</td>
			</tr>
			<tr>
				<td>Matter</td>
				<td>Y</td>
				<td>Y</td>
				<td>Container</td>
				<td>The matters included in the document.</td>
			</tr>
		</table>
		<h3>3. Document Header</h3>
		<p>The LMSS document header is describes the version, type, default language and character set needed to for correctly read the LMSS document.
		</p>
		<table>
			<tr>
				<th>ELEMENT<br></th>
				<th>REQ</th>
				<th>MULT</th>
				<th>TYPE</th>
				<th>COMMENTS</th>
			</tr>
			<tr>
				<td>Title</td>
				<td>N</td>
				<td>N</td>
				<td>Text(250)</td>
				<td>An optional title for the document.</td>
			</tr>
			<tr>
				<td>Version</td>
				<td>Y</td>
				<td>N</td>
				<td>Float</td>
				<td>The version of the LMSS standard being encoded</td>
			</tr>
			<tr>
				<td>Type</td>
				<td>Y</td>
				<td>N</td>
				<td>Enumeration:<br>SALI LMSS Type</td>
				<td>The type of the document. Supported types<br>include "Instance", "Template", and "Query". The default value is "Instance"</td>
			</tr>
			<tr>
				<td>Language</td>
				<td>N</td>
				<td>N</td>
				<td>Enumeration:<br>IETF BCP 47</td>
				<td>Languages follow the Internet Engineering<br>Task Force recommendation in BCP 47</td>
			</tr>
			<tr>
				<td>Charset</td>
				<td>N</td>
				<td>N</td>
				<td>Text</td>
				<td>Default value is UTF-8</td>
			</tr>
			<tr>
				<td>Extension<br>Link</td>
				<td>N</td>
				<td>Y</td>
				<td>Text: URI</td>
				<td>A link to an extension file</td>
			</tr>
			<tr>
				<td>Extension</td>
				<td>N</td>
				<td>Y</td>
				<td>Container</td>
				<td>One or more extension definitions.</td>
			</tr>
			<tr>
				<td>Declaration</td>
				<td>N</td>
				<td>Y</td>
				<td>Container</td>
				<td>Declarations are indexes of names that need<br>to be cross referenced in a specification.<br>NameIDs can be used in place of names<br>wherever names may appear.</td>
			</tr>
		</table>
		<h4>3.1. Title</h4>
		<p>An optional title for the document.</p>
		<h4>3.2. Version</h4>
		<p>The LMSS version is defined and maintained by SALI. Published version of the standard may be found at Sali.org.</p>
		<h4>3.3. Type</h4>
		<p>Type refers to the type of the Document. Permissible values include:</p>
		<ul>
			<li>Instance – An instance encodes a specific matter. Instances have required containers and elements to be well formed.</li>
			<li>Template – A template encodes default settings of an instance. Parts of templates that are not specified are assumed to accept all values. Templates must adhere to the LMSS container structure, however required elements are relaxed.
			</li>
			<li>Query – A query encodes a database query following a SQL-like structure. Queries have select, where, order by and limit structures.
			</li>
		</ul>
		<h4>3.4. Language</h4>
		<p>Language declares the default language of the LMSS structure. Languages follow the Internet Engineering Task Force recommendation in BCP 47.
		</p>
		<h4>3.5. Charset</h4>
		<p>The charset describes the encoding of the characters in the LMSS document. The default encoding is UTF-8.
		</p>
		<h4>3.6. Extension Link</h4>
		<p>A link to an extension file that conforms to the LMSS Extension file format.</p>
		<h3>4. Extension</h3>
		<p>An extension container is an in-document definition of an extension. A document may include an array of these in the header. The scope applies to the document.
		</p>
		<table>
			<tr>
				<th>ELEMENT<br></th>
				<th>REQ</th>
				<th>MULT</th>
				<th>TYPE</th>
				<th>COMMENTS</th>
			</tr>
			<tr>
				<td>Code Set</td>
				<td>Y</td>
				<td>N</td>
				<td>Text(40)</td>
				<td>The code of the code set being extended</td>
			</tr>
			<tr>
				<td>Code</td>
				<td>Y</td>
				<td>N</td>
				<td>Text(40)</td>
				<td>The extension code. Must be unique in the namespace.</td>
			</tr>
			<tr>
				<td>Parent</td>
				<td>Y</td>
				<td>N</td>
				<td>Text(40)</td>
				<td>The parent code. This code must be defined,before this definition.</td>
			</tr>
			<tr>
				<td>Name</td>
				<td>Y</td>
				<td>N</td>
				<td>Text(40)</td>
				<td>The short name of the extended code</td>
			</tr>
		</table>
		<p>A sample in-document extension is shown below</p>
		<pre><code>
			{
				"document" : {
				"header" : {
				"lmss version" : "1.02" //Draft LMSS 1.0 Rev 2
				,"lmss type" : "INST" //Instance
				,"language" : "en-us"
				,"charset" : "UTF-8"
				,"extension" : [{
				"code set" : "SALI-IND"
				,"code" : "@MULFAM"
				,"parent" : "RES"
				,"name" : "Multi-Family Residential"
			}
			,{
			"code set" : "SALI-IND"
			,"code" : "@OFFICE"
			,"parent" : "RES"
			,"name" : "Office"
				}
				,{
				"code set" : "SALI-IND"
				,"code" : "@INDUST"
				,"parent" : "RES"
				,"name" : "Industrial"
			}
			,{
			"code set" : "SALI-IND"
			,"code" : "@RESIDL"
			,"parent" : "RES"
			,"name" : "Residential"
		}]
		}
		}
		}
		</code></pre>
		<h4>4.1. Code Set</h4>
		<p>The LMSS Code of the code set.</p>
		<h4>4.2. Code</h4>
		<p>The code assigned to the extension. The code will have a “@” prepended to it when used.</p>
		<h4>4.3. Parent</h4>
		<p>The parent code. The parent code must be an existing standard code in the code set, or a previously defined extension. Examples include “RES” or “@OFFICE”.</p>
		<h4>4.4. Name</h4>
		<p>The short name of extension code.</p>
		<h2>5. Declaration</h2>
		<p>A declaration may be used to assign and index to an item to ensure accurate cross referencing. Declarations are typically used for legal entities but can be used in place of a Name (See 4.10.1, 4.11.1 and 4.11.2).</p>
		<p>A legal person or entity is any human or non-human entity, in other words, any human being, firm, or government agency that is recognized as having privileges and obligations, such as having the ability to enter into contracts, to sue, and to be sued.</p>
		<p>Entities are used to maintain referential integrity across LMSS structure. For example, if the matter includes two processes that refer to the same legal entity as in the example, “Review and negotiate project labor agreement for Jane Smith.” The matter may be encoded to have two processes – one for review and another of negotiation. But the review and negotiation are the same legal entity. An entity declaration should be used in this instance and the entity NameID should be used in each process to ensure that it is understood that the objects of both process are the same.</p>
		<table>
			<thead>
				<tr>
					<th>ELEMENT</th>
					<th>REQ.</th>
					<th>MULT.</th>
					<th>TYPE</th>
					<th>COMMENTS</th>
					<th>&nbsp;</th>
				</tr>
			</thead>
			<tbody>
				<tr>
					<td>NamelD</td>
					<td>Y</td>
					<td>N</td>
					<td>Text(40)</td>
					<td>The NamelD of the entity. Must be of the regular expression form \^[A-Za-z0-9_-]{1,39}</td>
					<td>&nbsp;</td>
				</tr>
				<tr>
					<td>Name</td>
					<td>Y</td>
					<td>N</td>
					<td>Text(250)</td>
					<td>Name to be inserted wherever the NamelD appears</td><td>&nbsp;</td>
				</tr>
			</tbody>
		</table>
		<h4>5.1. NameID</h4>
		<p>The ID to be used in place of a name. NameIDs must begin with a caret symbol. (e.g. ^102 or ^EntityXYZ).</p>
		<h4>5.2. Name</h4>
		<p>The name to be used in place of the NameID.</p>
		<h3>6. Matter</h3>
		<p>The Matter container encapsulates the information for a matter. There may be more than one matter per document. The matter must have a title, a human readable description, a locale and one or more processes. The locale may restrict the types of the processes. For example, certain bankruptcy processes are limited to the US because those processes a defined by US Bankruptcy law.</p>
		<table class="tableizer-table">
			<thead><tr class="tableizer-firstrow"><th>ELEMENT</th><th>REQ</th><th>MULT.</th><th>TYPE</th><th>COMMENTS</th><th>&nbsp;</th></tr></thead><tbody>
				<tr><td>Title</td>		 			<td>Y</td>
					<td>N</td><td>Text(250)</td><td>The title of the matter.</td><td>&nbsp;</td></tr>
					<tr><td>Locale</td>		 			<td>Y</td>
						<td>N</td><td>Enumeration: ISO 3166-2</td><td>The location of the matter.</td><td>&nbsp;</td></tr>
						<tr><td>Process</td>		 			<td>Y</td>
							<td>Y</td><td>Container</td><td>The process or processes for this matter.</td><td>&nbsp;</td></tr>
							<tr><td>Narrative</td>		 			<td>Y</td>
								<td>N</td><td>Container</td><td>The description of the matter.</td><td></td></tr>
							</tbody></table>
							<h4>6.1. Title</h4>
							<p>A required title for the process.</p>
							<h4>6.2. Locale</h4>
							<p>A required locale for the matter. The locale is an enumeration.</p>
							<h3>7. Narrative</h3>
							<p>A narrative holds a group of related matter descriptions. It includes a required type which is an enumerated list, an optional usage tag, and an optional source. Each narrative can have a specified usage so a Matter can have multiple narratives based on the audience. each narrative is intended to capture a logically unique matter interpretation of the matter. Formatting and language variants are accommodated in the description container.</p>
							<p>Narrative container elements</p>
							<table class="tableizer-table">
								<thead><tr class="tableizer-firstrow"><th>ELEMENT</th><th>REQ</th><th>MULT.</th><th>TYPE</th><th>COMMENTS</th><th>&nbsp;</th></tr></thead><tbody>
									<tr><td>Type</td><td>Y</td><td>N</td><td>Enumeration: SALI Narrative</td><td>The type of the narrative.</td><td>&nbsp;</td></tr>
									<tr><td>Usage</td><td>N</td><td>N</td><td>Text(250)</td><td>Descriptions of the intended audience or other usage of the narrative</td><td>&nbsp;</td></tr>
									<tr><td>Description</td><td>Y</td><td>Y</td><td>Container</td><td>One or more descriptions of a narrative.</td><td>&nbsp;</td></tr>
									<tr><td>Source</td><td>N</td><td>Y</td><td>Text(250)</td><td>The source of the narrative</td><td></td></tr>
								</tbody></table>
								<h4>7.1. Type</h4>
								<p>The narrative type is an enumerated list intended to capture the sensitivity of the narrative. Values include: public, confidential, private, generic, etc.</p>
								<h4>7.2. Usage</h4>
								<p>Usage is an optional human readable field that should capture the audience or usage of the narrative. Examples for the same matter might be: “Narrative written for pitches to lenders,” “Narrative written for pitches to borrowers,” and “Narrative written for generic finance pitches.”</p>
								<h4>7.3. Source</h4>
								<p>The source is an optional element that describe the source of the narrative. You may provide multiple sources. Examples include: “2015 litigation department compensation memo,” and “2017 environmental practice Chambers submission.”</p>
								<h3>8. Description</h3>
								<p>The description is an container encapsulates the specific text of a specific narrative. The description has text, a format and a language. If the language is not specified, it is inherited from the matter. For example, if a firm keeps French and English versions of the same narrative, or plain text and HTML formatted versions of the same narrative, these would be accommodated in the description container.
								</p>
								<table>
									<thead>
										<tr>
											<th>ELEMENT</th>
											<th>REQ</th>
											<th>MULT.</th>
											<th>TYPE</th>
											<th>COMMENTS</th>
										</tr>
									</thead>
									<tbody>
										<tr>
											<td>Text</td>
											<td>Y</td>
											<td>N</td>
											<td>Text(4000)</td>
											<td>The description of the matter.</td>
										</tr>
										<tr>
											<td>Format</td>
											<td>Y</td>
											<td>N</td>
											<td>Enumeration of Narrative Formats</td>
											<td>Text or HTML</td>
										</tr>
										<tr>
											<td>Language</td>
											<td>N</td>
											<td>N</td>
											<td>Enumeration: IETF BCP 47</td>
											<td>The language of the description. If omitted, it is assumed to be the same as that of the matter.</td>
										</tr>
									</tbody>
								</table>
								<h4>8.1. Text</h4>
								<p>The text holds the characters of the description. The format of the text is interpreted based on the description type.</p>
								<h4>8.2. Format</h4>
								<p>Two formats are supported: Text and HTML.</p>
								<h4>8.3. Language</h4>
								<p>Language is optionally specified by using BCP 47.</p>
								<h3>9. Process</h3>
								<p>The Process container describes the process, service or product being delivered. Every process must have a single process type. Top-level process types are transactions, disputes, regulatory proceedings, bankruptcy/restructurings, and advisory. If we think of the process as a sentence, the process type reprints the “verb.” They describe the action that is being taken.</p><p> The players are the legal entities involved in the process. These should be thought of the subject (Joe Smith) and object (Company X) in the sentence “Joe Smith sued Company X for $500,000 for breach of contract.” The process predicate contains the predecessors or outcomes of the process. In the sentence above, “for $500,000” and “for breach of contract.”</p><p>The Area of Law provides context to the process. The area of law should be thought of the primary subject of law for the process — think the class that’s the attorney was in when she learned about the applicable law. The area of law is provided primarily for context as in the examples, “He prosecuted the defendant” and “She prosecuted the patent.” The first is criminal law, the second is intellectual property law.</p>
								<table border="1" cellpadding="0" cellspacing="0">
									<tbody>
										<tr>
											<td>
												<p><strong>ELEMENT</strong></p>
											</td>
											<td>
												<p><strong>REQ.</strong></p>
											</td>
											<td>
												<p><strong>MULT.</strong></p>
											</td>
											<td>
												<p><strong>TYPE</strong></p>
											</td>
											<td>
												<p><strong>COMMENTS</strong></p>
											</td>
										</tr>
										<tr>
											<td>
												<p><strong>Title</strong></p>
											</td>
											<td>
												<p>N</p>
											</td>
											<td>
												<p>N</p>
											</td>
											<td>
												<p>Text(100)</p>
											</td>
											<td>
												<p>The title of the process.</p>
											</td>
										</tr>
										<tr>
											<td>
												<p><strong>Description</strong></p>
											</td>
											<td>
												<p>N</p>
											</td>
											<td>
												<p>N</p>
											</td>
											<td>
												<p>Text(4000)</p>
											</td>
											<td>
												<p>An optional description of the process.</p>
											</td>
										</tr>
										<tr>
											<td>
												<p><strong>Process Type</strong></p>
											</td>
											<td>
												<p>Y</p>
											</td>
											<td>
												<p>N</p>
											</td>
											<td>
												<p>Enumeration: SALI Process Type</p>
											</td>
											<td>
												<p>The type of the process. The process should be thought of a verb.</p>
											</td>
										</tr>
										<tr>
											<td>
												<p><strong>Area of Law</strong></p>
											</td>
											<td>
												<p>Y</p>
											</td>
											<td>
												<p>Y</p>
											</td>
											<td>
												<p>Enumeration: SALI Area of Law</p>
											</td>
											<td>
												<p>The primary area of law for the process. Area of Law provides context for interpreting other elements of the process.</p>
											</td>
										</tr>
										<tr>
											<td>
												<p><strong>Player</strong></p>
											</td>
											<td>
												<p>Y</p>
											</td>
											<td>
												<p>Y</p>
											</td>
											<td>
												<p>Container</p>
											</td>
											<td>
												<p>The players involved in a process.</p>
											</td>
										</tr>
										<tr>
											<td>
												<p><strong>Process Object</strong></p>
											</td>
											<td>
												<p>N</p>
											</td>
											<td>
												<p>Y</p>
											</td>
											<td>
												<p>Container</p>
											</td>
											<td>
												<p>The process object hold information specific to each kind of process. See the discussion below.</p>
											</td>
										</tr>
									</tbody>
								</table>
								<h4>9.1. Title</h4>
								<p>The optional title of the process. Examples include: “LLC formation in California”, and “License of technology to French company.”.</p>
								<h4>9.2. Description</h4>
								<p>An optional field to store additional information about the process.</p>
								<h4>9.3. Process Type</h4>
								<p>A SALI enumerated value. Top-level process types are transactions, disputes, regulatory proceedings, bankruptcy/restructurings, and advisory. If we think of the process as a sentence, the process type reprints the “verb.” They describe the action that is being taken.</p>
								<h4>4.9.4 Area of Law</h4>
								<p>The Area of Law is a SALI enumerated value that provides context to the process. The area of law should be thought of the primary subject of law for the process — think the class that’s the attorney was in when she learned about the applicable law. The area of law is provided primarily for context as in the examples, “He prosecuted the defendant” and “She prosecuted the patent.” The first is criminal law, the second is intellectual property law. There can be multiple areas of law.</p>
								<h3>10. Player</h3>
								<p>The players are the subject of the sentence and sometimes the object. Primary players are the primary parties involved in a legal process. The Player container has the following fields:<p>
									<b>Player container elements</b>
									<table border="1" cellpadding="0" cellspacing="0">
										<tbody>
											<tr>
												<td valign="top" width="17.088607594936708%">
													<p><strong>ELEMENT</strong></p>
												</td>
												<td valign="top" width="7.9113924050632916%">
													<p><strong>REQ.</strong></p>
												</td>
												<td valign="top" width="11.075949367088608%">
													<p><strong>MULT.</strong></p>
												</td>
												<td valign="top" width="19.145569620253166%">
													<p><strong>TYPE</strong></p>
												</td>
												<td valign="top" width="44.778481012658226%">
													<p><strong>COMMENTS</strong></p>
												</td>
											</tr>
											<tr>
												<td valign="top" width="17.088607594936708%">
													<p><strong>Name</strong></p>
												</td>
												<td valign="top" width="7.9113924050632916%">
													<p>Y*</p>
												</td>
												<td valign="top" width="11.075949367088608%">
													<p>N</p>
												</td>
												<td valign="top" width="19.145569620253166%">
													<p>Text(250)</p>
												</td>
												<td valign="top" width="44.778481012658226%">
													<p>The name of the player. This is usually a company name or individual name. May use a Name or a declared ID.</p>
												</td>
											</tr>
											<tr>
												<td valign="top" width="17.088607594936708%">
													<p><strong>Player Role</strong></p>
												</td>
												<td valign="top" width="7.9113924050632916%">
													<p>N</p>
												</td>
												<td valign="top" width="11.075949367088608%">
													<p>Y</p>
												</td>
												<td valign="top" width="19.145569620253166%">
													<p>Enumeration: SALI Player Role</p>
												</td>
												<td valign="top" width="44.778481012658226%">
													<p>The contextual role that the player has in the process. (e.g. Plaintiff, Licensee, etc.)</p>
												</td>
											</tr>
											<tr>
												<td valign="top" width="17.088607594936708%">
													<p><strong>Industry</strong></p>
												</td>
												<td valign="top" width="7.9113924050632916%">
													<p>N</p>
												</td>
												<td valign="top" width="11.075949367088608%">
													<p>N</p>
												</td>
												<td valign="top" width="19.145569620253166%">
													<p>Enumeration: SALI Industry</p>
												</td>
												<td valign="top" width="44.778481012658226%">
													<p>The industry that the player is in. This often provides context for how the process is executed.</p>
												</td>
											</tr>
											<tr>
												<td valign="top" width="17.088607594936708%">
													<p><strong>Legal Entity</strong></p>
												</td>
												<td valign="top" width="7.9113924050632916%">
													<p>Y</p>
												</td>
												<td valign="top" width="11.075949367088608%">
													<p>N</p>
												</td>
												<td valign="top" width="19.145569620253166%">
													<p>Enumeration: SALI Legal Entity</p>
												</td>
												<td valign="top" width="44.778481012658226%">
													<p>The type of legal entity that the player is. A corporation, a partnership, a person, etc.</p>
												</td>
											</tr>
											<tr>
												<td valign="top" width="17.088607594936708%">
													<p><strong>Governmental&nbsp;</strong><strong>Authority</strong></p>
												</td>
												<td valign="top" width="7.9113924050632916%">
													<p>N</p>
												</td>
												<td valign="top" width="11.075949367088608%">
													<p>N</p>
												</td>
												<td valign="top" width="19.145569620253166%">
													<p>Enumeration:&nbsp;SALI</p>
													<p>Governmental&nbsp;Authority</p>
												</td>
												<td valign="top" width="44.778481012658226%">
													<p>Used when the player is a governmental authority</p>
												</td>
											</tr>
											<tr>
												<td valign="top" width="17.088607594936708%">
													<p><strong>Counsel</strong></p>
												</td>
												<td valign="top" width="7.9113924050632916%">
													<p>N</p>
												</td>
												<td valign="top" width="11.075949367088608%">
													<p>Y</p>
												</td>
												<td valign="top" width="19.145569620253166%">
													<p>Container</p>
												</td>
												<td valign="top" width="44.778481012658226%">
													<p>The legal representatives of the player</p>
												</td>
											</tr>
										</tbody>
									</table>  
									<h4>10.1. Name</h4>
									<p>The name is the name of player in human readable form. If a NameID is used, an Name is not required.</p>
									<h4>10.2. Player Role</h4>
									<p>The Player Role is an optional element that provides context. Examples of roles are Plaintiff, Defendant, Acquiror, etc. .The Roles span both legal roles and functional roles. Play is an enumerated value.</p>
									<h4>10.3 Industry</h4>
									<p>The industry is an optional field that describes the industry of the player. Industry is an enumerated value.</p>
									<h4>10.4. Legal Entity</h4>
									<p>Legal entity describes the type of the player. In law, a “legal person” or “legal entity” is any human or non-human entity, in other words, any human being, firm, or government agency that is recognized as having privileges and obligations, such as having the ability to enter into contracts, to sue, and to be sued. Legal Entity is an enumerated value.</p>
									<h4>10. 5 Governmental Authority</h4>
									<p>The enumerated identification of the governmental authority if the player is a governmental authority.</p>
									<h3>4.11 Counsel</h3>
									<p>The counsel container includes all of the legal representatives of the player. The fields of the counsel container are described below:</p>
									<b>Counsel container elements</b>
									<table border="1" cellpadding="0" cellspacing="0">
										<tbody>
											<tr>
												<td valign="top" width="18.066561014263076%">
													<p><strong>ELEMENT</strong></p>
												</td>
												<td valign="top" width="10.45958795562599%">
													<p><strong>REQ.</strong></p>
												</td>
												<td valign="top" width="10.45958795562599%">
													<p><strong>MULT.</strong></p>
												</td>
												<td valign="top" width="16.164817749603802%">
													<p><strong>TYPE</strong></p>
												</td>
												<td valign="top" width="44.84944532488114%">
													<p><strong>COMMENTS</strong></p>
												</td>
											</tr>
											<tr>
												<td valign="top" width="18.066561014263076%">
													<p><strong>Name</strong></p>
												</td>
												<td valign="top" width="10.45958795562599%">
													<p>Y*</p>
												</td>
												<td valign="top" width="10.45958795562599%">
													<p>N</p>
												</td>
												<td valign="top" width="16.164817749603802%">
													<p>Text(250)</p>
												</td>
												<td valign="top" width="44.84944532488114%">
													<p>The name of the legal representative. May use a Name or a declared ID.</p>
												</td>
											</tr>
											<tr>
												<td valign="top" width="18.066561014263076%">
													<p><strong>Firm Name</strong></p>
												</td>
												<td valign="top" width="10.45958795562599%">
													<p>N*</p>
												</td>
												<td valign="top" width="10.45958795562599%">
													<p>N</p>
												</td>
												<td valign="top" width="16.164817749603802%">
													<p>Text(250)</p>
												</td>
												<td valign="top" width="44.84944532488114%">
													<p>The firms of the legal representative. May use a Name or a declared ID.</p>
												</td>
											</tr>
											<tr>
												<td valign="top" width="18.066561014263076%">
													<p><strong>Representation&nbsp;</strong><strong>Role</strong></p>
												</td>
												<td valign="top" width="10.45958795562599%">
													<p>Y</p>
												</td>
												<td valign="top" width="10.45958795562599%">
													<p>N</p>
												</td>
												<td valign="top" width="16.164817749603802%">
													<p>Enumeration</p>
												</td>
												<td valign="top" width="44.84944532488114%">
													<p>The role of the legal representative</p>
												</td>
											</tr>
										</tbody>
									</table>
								</p>*Either a Name or a NameID is required.</p>
								<h4>11.1. Name</h4>
								<p>The name is the name of counsel in human readable form. If a NameID is used, an Name is not required. (NameIDs are indicated by prefixing them with a caret “^” symbol. e.g. “^103”.)</p>
								<h4>11.2. Firm Name</h4>
								<p>The firm name is the name of firm that the counsel is part of in human readable form. If a NameID is used, an Firm Name is not required.</p>
								<h4>11.3. Representation Role</h4>
								<p>The role of the legal representative. Role is an enumerated value.</p>
								<h3>12. Process Object</h3>
								<p>The process object encapsulates important elements of the process. A process can have multiple process object. The process object can simply be a summary of key attributes of the overall process. Additional process objects can be attached to describe the preconditions and post conditions of a process. For example, for a merger, there optionally can be individual process objects describing the predecessor entities and resulting entity. 
								<table border="0" cellspacing="0" cellpadding="0">
									<tbody>
									<tr>
									<td>
									<p>
									<a
									href="http://sali.legal/codetype.php?s_ct_name=sali&amp;amp;ct_id=1&amp;amp;bb_codetypeOrder=Sorter_ct_name&amp;amp;bb_codetypeDir=ASC"
									>
									<strong>Code Set</strong>
									</a>
									<strong></strong>
									</p>
									</td>
									<td>
									<p>
									<a
									href="http://sali.legal/codetype.php?s_ct_name=sali&amp;amp;ct_id=1&amp;amp;bb_codetypeOrder=Sorter2&amp;amp;bb_codetypeDir=ASC"
									>
									<strong>Code</strong>
									</a>
									<strong></strong>
									</p>
									</td>
									<td>
									<p>
									<a
									href="http://sali.legal/codetype.php?s_ct_name=sali&amp;amp;ct_id=1&amp;amp;bb_codetypeOrder=Sorter_ct_description&amp;amp;bb_codetypeDir=ASC"
									>
									<strong>Description</strong>
									</a>
									<strong></strong>
									</p>
									</td>
									<td>
									</td>
									</tr>
									<tr>
									<td>
									<p>
									<strong>SALI Areas of Law</strong>
									<strong></strong>
									</p>
									</td>
									<td>
									<p>
									SALI-AOL:2
									</p>
									</td>
									<td>
									<p>
									SALI Area of Law/Practice
									</p>
									</td>
									<td>
									<p>
									<a
									href="https://sali.legal/code.php?s_keyword&amp;amp;ct=17&amp;amp;lvl&amp;amp;psize=1000"
									>
									View
									</a>
									</p>
									</td>
									</tr>
									<tr>
									<td>
									<p>
									<strong>SALI Court</strong>
									<strong></strong>
									</p>
									</td>
									<td>
									<p>
									SALI-COURT
									</p>
									</td>
									<td>
									<p>
									Codes for courts. Currently limited to
									</p>
									</td>
									<td>
									<p>
									<a
									href="https://sali.legal/code.php?s_keyword&amp;amp;ct=3&amp;amp;lvl&amp;amp;psize=1000"
									>
									View
									</a>
									</p>
									</td>
									</tr>
									<tr>
									<td>
									</td>
									<td>
									</td>
									<td>
									<p>
									U.S. courts.
									</p>
									</td>
									<td>
									</td>
									</tr>
									<tr>
									<td>
									<p>
									<strong>SALI Currency (ISO 4217)</strong>
									<strong></strong>
									</p>
									</td>
									<td>
									<p>
									ISO-4217
									</p>
									</td>
									<td>
									<p>
									List of world currencies
									</p>
									</td>
									<td>
									<p>
									<a href="https://sali.legal/browser.php?ct_id=19">
									View
									</a>
									</p>
									</td>
									</tr>
									<tr>
									<td>
									<p>
									<strong>SALI Format</strong>
									<strong></strong>
									</p>
									</td>
									<td>
									<p>
									SALI-FMT
									</p>
									</td>
									<td>
									<p>
									The format of a description
									</p>
									</td>
									<td>
									<p>
									<a
									href="https://sali.legal/code.php?s_keyword&amp;amp;ct=12&amp;amp;lvl&amp;amp;psize=1000"
									>
									View
									</a>
									</p>
									</td>
									</tr>
									<tr>
									<td>
									<p><strong>SALI LMSS Type</strong></p>
									</td>
									<td>
									<p>SALI-LMST</p>
									</td>
									<td>
									<p>The types of LMSS documents</p>
									</td>
									<td>
									<p>
									<a href="https://sali.legal/code.php?s_keyword&amp;ct=10&amp;lvl&amp;psize=1000">View</a>
									</p>
									</td>
									</tr>
									<tr>
									<td>
									<p><strong>SALI Location</strong></p>
									</td>
									<td>
									<p>SALI-ISO31662</p>
									</td>
									<td>
									<p>World locations to the state/province</p>
									</td>
									<td>
									<p>
									<a href="https://sali.legal/browser.php?ct_id=6">View</a>
									</p>
									</td>
									</tr>
									<tr>
									<td>
									<p>&nbsp;</p>
									</td>
									<td>
									<p>&nbsp;</p>
									</td>
									<td>
									<p>level</p>
									</td>
									<td>
									<p>&nbsp;</p>
									</td>
									</tr>
									<tr>
									<td>
									<p><strong>SALI Matter Narrative</strong></p>
									</td>
									<td>
									<p>SALI-MATNAR</p>
									</td>
									<td>
									<p>Codes used to identify the type of</p>
									</td>
									<td>
									<p>
									<a href="https://sali.legal/code.php?s_keyword&amp;ct=9&amp;lvl&amp;psize=1000">View</a>
									</p>
									</td>
									</tr>
									<tr>
									<td>
									<p>&nbsp;</p>
									</td>
									<td>
									<p>&nbsp;</p>
									</td>
									<td>
									<p>narrative.</p>
									</td>
									<td>
									<p>&nbsp;</p>
									</td>
									</tr>
									<tr>
									<td>
									<p><strong>SALI Player Role</strong></p>
									</td>
									<td>
									<p>SALI-PROLE</p>
									</td>
									<td>
									<p>The types of player roles that can be</p>
									</td>
									<td>
									<p>
									<a href="https://sali.legal/code.php?s_keyword&amp;ct=7&amp;lvl&amp;psize=1000">View</a>
									</p>
									</td>
									</tr>
									<tr>
									<td>
									<p>&nbsp;</p>
									</td>
									<td>
									<p>&nbsp;</p>
									</td>
									<td>
									<p>applied to a matter.</p>
									</td>
									<td>
									<p>&nbsp;</p>
									</td>
									</tr>
									<tr>
									<td>
									<p><strong>SALI Process</strong></p>
									</td>
									<td>
									<p>SALI-PROC</p>
									</td>
									<td>
									<p>Codes used to define a legal service</p>
									</td>
									<td>
									<p>
									<a href="https://sali.legal/browser.php?ct_id=22">View</a>
									</p>
									</td>
									</tr>
									<tr>
									<td>
									<p>&nbsp;</p>
									</td>
									<td>
									<p>&nbsp;</p>
									</td>
									<td>
									<p>process</p>
									</td>
									<td>
									<p>&nbsp;</p>
									</td>
									</tr>
									<tr>
									<td>
									<p><strong>SALI Process Status</strong></p>
									</td>
									<td>
									<p>SALI-PROCSTAT</p>
									</td>
									<td>
									<p>Codes for the status of a process</p>
									</td>
									<td>
									<p>
									<a href="https://sali.legal/code.php?s_keyword&amp;ct=2&amp;lvl&amp;psize=1000">View</a>
									</p>
									</td>
									</tr>
									<tr>
									<td>
									<p><strong>SALI Representation Role</strong></p>
									</td>
									<td>
									<p>SALI-RROLE</p>
									</td>
									<td>
									<p>The types of representation roles for a player.</p>
									</td>
									<td>
									<p>
									<a href="https://sali.legal/code.php?s_keyword&amp;ct=13&amp;lvl&amp;psize=1000">View</a>
									</p>
									</td>
									</tr>
									<tr>
									<td>
									<p><strong>SALI Trial Type</strong></p>
									</td>
									<td>
									<p>SALI-TRITYP</p>
									</td>
									<td>
									<p>The type of trial format</p>
									</td>
									<td>
									<p>
									<a href="https://sali.legal/browser.php?ct_id=20">View</a>
									</p>
									</td>
									</tr>
									</tbody>
									</table>
									<table border="0" cellspacing="0" cellpadding="0">
									<tbody>
									<tr>
									<td>
									<p>
									<strong>SALI Governmental </strong>
									SALI-GOVT
									</p>
									<p>
									<strong>Body</strong>
									<strong></strong>
									</p>
									</td>
									<td>
									<p>
									Government codes. Currently U.S. federal only
									</p>
									</td>
									<td>
									<p>
									<a
									href="https://sali.legal/code.php?s_keyword&amp;amp;ct=14&amp;amp;lvl&amp;amp;psize=1000"
									>
									View
									</a>
									</p>
									</td>
									</tr>
									</tbody>
									</table>
		</p>
	</section>
</div>
