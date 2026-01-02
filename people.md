---
layout: default
title: People
permalink: /people/
---

<div class="hero-banner" style="background-image: url('{{ "/assets/images/people-banner.png" | relative_url }}');">
  <div class="hero-content">
    <h1>People</h1>
  </div>
</div>

<div class="grid-container">
{% for person in site.people %}
  <div class="card">
    <a href="{{ person.url | relative_url }}" style="text-decoration: none; color: inherit;">
      {% if person.name %}
        <h4>{{ person.name }}</h4>
        <p><strong>{{ person.title }}</strong></p>
        {% if person.corporation %}
        <p><em>{{ person.corporation }}</em></p>
        {% endif %}
      {% else %}
        <h4>{{ person.title }}</h4>
        <p>{{ person.excerpt | strip_html | truncatewords: 20 }}</p>
      {% endif %}
    </a>
  </div>
{% endfor %}
</div>
