---
layout: default
title: Players
permalink: /players/
---

<div class="hero-banner" style="background-image: url('{{ "/assets/images/players-banner.png" | relative_url }}');">
  <div class="hero-content">
    <h1>The Crew</h1>
  </div>
</div>

<div class="grid-container">
{% for player in site.players %}
  <div class="card">
    <h3><a href="{{ player.url | relative_url }}">{{ player.title }}</a></h3>
    <p>{{ player.excerpt | strip_html | truncatewords: 20 }}</p>
  </div>
{% endfor %}
</div>
