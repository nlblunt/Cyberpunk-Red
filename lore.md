---
layout: default
title: Lore
permalink: /lore/
---

<div class="hero-banner" style="background-image: url('{{ "/assets/images/lore-banner.png" | relative_url }}');">
  <div class="hero-content">
    <h1>World Lore</h1>
  </div>
</div>

<div class="grid-container">
{% for item in site.lore %}
  <div class="card">
    <a href="{{ item.url | relative_url }}" style="text-decoration: none; color: inherit;">
      <h4>{{ item.title }}</h4>
      <p>{{ item.excerpt | strip_html | truncatewords: 20 }}</p>
    </a>
  </div>
{% endfor %}
</div>
