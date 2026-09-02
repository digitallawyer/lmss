---
layout: page
title: Talk to us
description: Questions about the standard, or about this site.
---
This site is built and maintained by [Legal.io](https://www.legal.io). We are not
the SALI Alliance — for questions about the standard itself, or to get involved in
its development, go to [sali.org](https://sali.org).

For anything about **this site** — a wrong tag page, a bad crosswalk match, an API
question, or a correction — get in touch.

{% if site.formspree_id %}
<form action="https://formspree.io/f/{{ site.formspree_id }}" method="POST">
  <p><label for="name">Name</label><br>
     <input type="text" name="name" id="name" required></p>
  <p><label for="email">Email</label><br>
     <input type="email" name="email" id="email" required></p>
  <p><label for="message">Message</label><br>
     <textarea name="message" id="message" rows="6" required></textarea></p>
  <p><button type="submit">Send</button></p>
</form>
{% else %}
**Email:** [contact@legal.io](mailto:contact@legal.io?subject=lmss.io)

Bugs and corrections are best filed as an
[issue]({{ site.github_url }}/issues) — that way they are public and trackable.
{% endif %}

You can also open a pull request; see
[CONTRIBUTING]({{ site.github_url }}/blob/master/CONTRIBUTING.md).
