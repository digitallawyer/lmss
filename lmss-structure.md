---
layout: page
title: LMSS Structure
description: An in-depth overview of the structure of LMSS
nav-menu: true
show_tile: true
image: assets/images/structure.jpg
---


# LMSS Structure (UNDER CONSTRUCTION)

## 1. Overview

The LMSS document is comprised of a Header and one or more Matters. The Header
and the Matter(s) are containers Each container has elements that may be of type Text,
Numeric, Enumeration or Container. Enumerations are stored in Text(250) fields to
accommodate multiple levels of specificity that are represented as concatenated codes.
Containers are pointers to other structures.

A well-formed Document is a structure that includes all required fields. (Note that the
concept of a well-formed document applies to instance but not templates or queries.) In
the tables below, “REQ” indicates whether the element is required (in an LMSS instance
but not a query), “MULT” indicates whether multiple values are permitted. A well-formed
document is required in the interchange of instances of matters between systems. A
well-formed document is not required when the LMSS is used in a query. In those
instances, a missing field matches all instances. See LMSS Queries below.

## 2 Document

The Document container is the top-level container in the LMSS instance. The Document
must have a Header and one or more Matters.
Document container elements
ELEMENT REQ MULT. TYPE COMMENTS
Header Y N Container The header information for the document
Matter Y Y Container The matters included in the document.

### 4.3 Document Header

The LMSS document header is describes the version, type, default language and
character set needed to for correctly read the LMSS document.
ELEMENT REQ MULT. TYPE COMMENTS
Title N N Text(250) An optional title for the document.
Version Y N Float The version of the LMSS standard being
encoded
Type Y N Enumeration:
SALI LMSS Type
The type of the document. Supported types
include "Instance", "Template", and "Query".


```
The default value is "Instance"
Language N N Enumeration:
IETF BCP 47
Languages follow the Internet Engineering
Task Force recommendation in BCP 47
Charset N N Text Default value is UTF- 8
Extension
Link
N Y Text: URI A link to an extension file
Extension N Y Container One or more extension definitions.
Declaration N Y Container Declarations are indexes of names that need
to be cross referenced in a specification.
NameIDs can be used in place of names
wherever names may appear.
```
#### 4.3.1 Title

An optional title for the document.

#### 4.3.2 Version

The LMSS version is defined and maintained by SALI. Published version of the
standard may be found at Sali.org

#### 4.3.3 Type

Type refers to the type of the Document. Permissible values include:
 Instance – An instance encodes a specific matter. Instances have required
containers and elements to be well formed.
 Template – A template encodes default settings of an instance. Parts of
templates that are not specified are assumed to accept all values. Templates
must adhere to the LMSS container structure, however required elements are
relaxed.
 Query – A query encodes a database query following a SQL-like structure.
Queries have select, where, order by and limit structures.

#### 4.3.4 Language

Language declares the default language of the LMSS structure. Languages follow the
Internet Engineering Task Force recommendation in BCP 47.


#### 4.3.5 Charset

The charset describes the encoding of the characters in the LMSS document. The
default encoding is UTF-8.

#### 4.3.6 Extension Link

A link to an extension file that conforms to the LMSS Extension file format.

### 4.4 Extension

An extension container is an in-document definition of an extension. A document may
include an array of these in the header. The scope applies to the document.
ELEMENT REQ. MULT. TYPE COMMENTS
Code Set Y N Text(40) The code of the code set being extended
Code Y N Text(40) The extension code. Must be unique in the
namespace.
Parent Y N Text(40) The parent code. This code must be defined
before this definition.
Name Y N Text(250) The short name of the extended code
A sample in-document extension is shown below
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

#### 4.4.1 Code Set

The LMSS Code of the code set. (See 6.1)

#### 4.4.2 Code

The code assigned to the extension. The code will have a "@" prepended to it when
used.

#### 4.4.3 Parent

The parent code. The parent code must be an existing standard code in the code set, or
a previously defined extension. Examples include "RES" or "@OFFICE".

#### 4.4.4 Name

The short name of extension code.


### 4.5 Declaration

A declaration may be used to assign and index to an item to ensure accurate cross
referencing. Declarations are typically used for legal entities but can be used in place of
a Name (See 4.10.1, 4.11.1 and 4.11.2).
A legal person or entity is any human or non-human entity, in other words, any human
being, firm, or government agency that is recognized as having privileges and
obligations, such as having the ability to enter into contracts, to sue, and to be sued.
Entities are used to maintain referential integrity across LMSS structure. For example, if
the matter includes two processes that refer to the same legal entity as in the example,
"Review and negotiate project labor agreement for Jane Smith." The matter may be
encoded to have two processes – one for review and another of negotiation. But the
review and negotiation are the same legal entity. An entity declaration should be used in
this instance and the entity NameID should be used in each process to ensure that it is
understood that the objects of both process are the same.
ELEMENT REQ. MULT. TYPE COMMENTS
NameID Y N Text(40) The NameID of the entity. Must be of the
regular expression form \^[A-Za-z0-9_-]{1,39}
Name Y N Text(250) Name to be inserted wherever the NameID
appears

#### 4.5.1 NameID

The ID to be used in place of a name. NameIDs must begin with a caret symbol. (e.g.
^102 or ^EntityXYZ).

#### 4.5.2 Name

The name to be used in place of the NameID.

### 4.6 Matter

The Matter container encapsulates the information for a matter. There may be more
than one matter per document. The matter must have a title, a human readable
description, a locale and one or more processes. The locale may restrict the types of
the processes. For example, certain bankruptcy processes are limited to the US
because those processes a defined by US Bankruptcy law.


Matter container elements
ELEMENT REQ MULT. TYPE COMMENTS
Title Y N Text( 250 ) The title of the matter.
Locale Y N Enumeration: ISO
3166 - 2
The location of the matter.
Process Y Y Container The process or processes for this matter.
Narrative Y N Container The description of the matter.

#### 4.6.1 Title

A required title for the process.

#### 4.6.2 Locale

A required locale for the matter. The locale is an enumeration.

### 4.7 Narrative

A narrative holds a group of related matter descriptions. It includes a required type
which is an enumerated list, an optional usage tag, and an optional source. Each
narrative can have a specified usage so a Matter can have multiple narratives based on
the audience. each narrative is intended to capture a logically unique matter
interpretation of the matter. Formatting and language variants are accommodated in the
description container.


Narrative container elements
ELEMENT REQ. MULT. TYPE COMMENTS
Type Y N Enumeration:
SALI Narrative
Type
The type of the narrative.

Usage (^) N N Text( 250 ) Descriptions of the intended audience or
other usage of the narrative
Description Y Y Container One or more descriptions of a narrative.
Source N Y Text( 250 ) The source of the narrative

#### 4.7.1 Type

The narrative type is an enumerated list intended to capture the sensitivity of the
narrative. Values include: public, confidential, private, generic, etc.

#### 4.7.2 Usage

Usage is an optional human readable field that should capture the audience or usage of
the narrative. Examples for the same matter might be: "Narrative written for pitches to
lenders," "Narrative written for pitches to borrowers," and "Narrative written for generic
finance pitches."

#### 4.7.3 Source

The source is an optional element that describe the source of the narrative. You may
provide multiple sources. Examples include: "2015 litigation department compensation
memo," and "2017 environmental practice Chambers submission."

### 4.8 Description

The description is an container encapsulates the specific text of a specific narrative. The
description has text, a format and a language. If the language is not specified, it is
inherited from the matter. For example, if a firm keeps French and English versions of
the same narrative, or plain text and HTML formatted versions of the same narrative,
these would be accommodated in the description container.
ELEMENT REQ. MULT. TYPE COMMENTS


```
Text Y N Text(4000) The description of the matter.
Format Y N Enumeration of
Narrative
Formats
Text or HTML
Language N N Enumeration:
IETF BCP 47
The language of the description. If omitted, it
is assumed to be the same as that of the
matter.
```
#### 4.8.1 Text

The text holds the characters of the description. The format of the text is interpreted
based on the description type.

#### 4.8.2 Format

Two formats are supported: Text and HTML.

#### 4.8.3 Language

Language is optionally specified by using BCP 47.

### 4.9 Process

The Process container describes the process, service or product being delivered.
Every process must have a single process type. Top-level process types are
transactions, disputes, regulatory proceedings, bankruptcy/restructurings, and advisory.
If we think of the process as a sentence, the process type reprints the “verb.” They
describe the action that is being taken.
The players are the legal entities involved in the process. These should be thought of
the subject (Joe Smith) and object (Company X) in the sentence “Joe Smith sued
Company X for $500,000 for breach of contract.”
The process predicate contains the predecessors or outcomes of the process. In the
sentence above, “for $500,000” and “for breach of contract.”
The Area of Law provides context to the process. The area of law should be thought of
the primary subject of law for the process — think the class that’s the attorney was in
when she learned about the applicable law. The area of law is provided primarily for
context as in the examples, “He prosecuted the defendant” and “She prosecuted the
patent.” The first is criminal law, the second is intellectual property law.


Process container elements
ELEMENT REQ. MULT. TYPE COMMENTS
Title N N Text(100) The title of the process.
Description N N Text(4000) An optional description of the process.
Process
Type
Y N Enumeration:
SALI Process
Type
The type of the process. The process
should be thought of a verb.
Area of
Law
Y Y Enumeration:
SALI Area of
Law
The primary area of law for the process.
Area of Law provides context for
interpreting other elements of the
process.
Player Y Y Container The players involved in a process.
Process
Object
N Y Container The process object hold information
specific to each kind of process. See the
discussion below.

#### 4.9.1 Title

The optional title of the process. Examples include: "LLC formation in California", and
"License of technology to French company.".

#### 4.9.2 Description

An optional field to store additional information about the process.

#### 4.9.3 Process Type

A SALI enumerated value. Top-level process types are transactions, disputes,
regulatory proceedings, bankruptcy/restructurings, and advisory. If we think of the
process as a sentence, the process type reprints the “verb.” They describe the action
that is being taken.

#### 4.9.4 Area of Law

The Area of Law is a SALI enumerated value that provides context to the process. The
area of law should be thought of the primary subject of law for the process — think the
class that’s the attorney was in when she learned about the applicable law. The area of
law is provided primarily for context as in the examples, “He prosecuted the defendant”


and “She prosecuted the patent.” The first is criminal law, the second is intellectual
property law. There can be multiple areas of law.

### 4.10 Player

The players are the subject of the sentence and sometimes the object. Primary players
are the primary parties involved in a legal process. The Player container has the
following fields:
Player container elements
ELEMENT REQ. MULT. TYPE COMMENTS
Name Y* N Text(250) The name of the player. This is usually a
company name or individual name. May use
a Name or a declared ID.
Player Role N Y Enumeration:
SALI Player Role
The contextual role that the player has in the
process. (e.g. Plaintiff, Licensee, etc.)
Industry N N Enumeration:
SALI Industry
The industry that the player is in. This often
provides context for how the process is
executed.
Legal Entity Y N Enumeration:
SALI Legal Entity
The type of legal entity that the player is. A
corporation, a partnership, a person, etc.
Governmental
Authority
N N Enumeration:
SALI
Governmental
Authority
Used when the player is a governmental
authority
Counsel N Y Container The legal representatives of the player
*Either a Name or a NameID is required.

#### 4.10.1 Name

The name is the name of player in human readable form. If a NameID is used, an Name
is not required.

#### 4.10.2 Player Role

The Player Role is an optional element that provides context. Examples of roles are
Plaintiff, Defendant, Acquiror, etc. .The Roles span both legal roles and functional roles.
Play is an enumerated value.


#### 4.10.3 Industry

The industry is an optional field that describes the industry of the player. Industry is an
enumerated value.

#### 4.10.4 Legal Entity

Legal entity describes the type of the player. In law, a "legal person" or "legal entity" is
any human or non-human entity, in other words, any human being, firm, or government
agency that is recognized as having privileges and obligations, such as having the
ability to enter into contracts, to sue, and to be sued. Legal Entity is an enumerated
value.

#### 4.10. 5 Governmental Authority

The enumerated identification of the governmental authority if the player is a
governmental authority.

### 4.11 Counsel

The counsel container includes all of the legal representatives of the player. The fields
of the counsel container are described below:
Counsel container elements
ELEMENT REQ. MULT. TYPE COMMENTS

Name (^) Y* N Text(250) The name of the legal representative. May
use a Name or a declared ID.
Firm Name N* N Text(250) The firms of the legal representative. May
use a Name or a declared ID.
Representation
Role
Y N Enumeration The role of the legal representative
*Either a Name or a NameID is required.

#### 4.11.1 Name

The name is the name of counsel in human readable form. If a NameID is used, an
Name is not required. (NameIDs are indicated by prefixing them with a caret "^" symbol.
e.g. "^103".)


#### 4.11.2 Firm Name

The firm name is the name of firm that the counsel is part of in human readable form. If
a NameID is used, an Firm Name is not required.

#### 4.11.3 Representation Role

The role of the legal representative. Role is an enumerated value.

### 4.12 Process Object

The process object encapsulates important elements of the process. A process can
have multiple process object. The process object can simply be a summary of key
attributes of the overall process. Additional process objects can be attached to describe
the preconditions and post conditions of a process. For example, for a merger, there
optionally can be individual process objects describing the predecessor entities and
resulting entity.
ELEMENT REQ. MULT. TYPE COMMENTS
Description N N Text(4000) The description the Process Object
Status N N Enumeration An enumerated status: Open, closed,
Canceled
Cross-Border N N Boolean Is the process cross border?
Filing Date N N Date The filing date, if appropriate
Term Sheet
Date
N N Date The term sheet date, if appropriate
Effective Date N N Date The effective date of the process
Closing Date N N Date Closing date, if appropriate
Announce date N N Date The date process was announced, if
appropriate

Asset Location (^) N N Text(4000) Location of the transaction - esp. for real
property
Asset
Description
N N Text(4000) Description of the asset such as asset type,
asset size, etc.
Monetary Value (^) N N Container The monetary value of the transaction,
dispute or object


ELEMENT REQ. MULT. TYPE COMMENTS
Non-Monetary
Value
N N Text(400) The non-monetary value of the transaction,
dispute or object.
Transaction:
Consideration
N Y Text(4000) Description of the consideration for the deal -
Stock, Cash, Real Estate, etc.
Transaction:
Deal Type
N Y Text(4000) Type of deal.
Transaction:
Location
N Y Text(4000) Location of the transaction.
Transaction:
Legal Entity
N Y Enumerated
Value: Legal
Entity
If a formation or dissolution, the kind of legal
entity formed or destroyed.
Regulatory:
Authority
N Y Enumerated
Value:
Governmental
Authority
Regulator. A public authority or government
agency responsible for exercising
autonomous authority over some area of
human activity in a regulatory or supervisory
capacity.
Regulatory:
Authority Other
N Y Text(250) Regulatory authority not included in the
enumeration values
Dispute: Venue N Y Enumerated
Value: Court
The venue of the dispute.
Dispute: Venue
Other
N Y Text(250) Dispute venue not fully covered by the
enumerated values.
Dispute: Trial
Type
N N Enumerated
Value: Trial Type
The type of the trial.
Dispute: Case
Name
N N Text(250) Name of the case.
Dispute:
Resolution
N N Text(250) Enumeration TBD
Dispute:
Resolution
Date
N N Date Date of the dispute resolution
Dispute:
Duration
(Months)
N N Integer Duration of the dispute in months
Dispute: Multi-
Jurisdictional
N N Boolean Set if the dispute is multijurisdictional


ELEMENT REQ. MULT. TYPE COMMENTS
Dispute:
Number of
Depositions
N N Integer Number of depositions
Dispute:
Number of
Experts
N N Integer Number of experts
See the table above for descriptions.

### 4.13 Monetary Value

Monetary Value encapsulates a financial value attribute. It consists of a floating point
number and a currency code.
Monetary value container elements
ELEMENT REQ. MULT. TYPE COMMENTS
Currency Y N Enumeration:
Currency
A currency code a defined by ISO 4217
Value Y N Float A floating point number that represents the value


</div>
</section>

	</section>
</div>