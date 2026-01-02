---
layout: default
title: Corporations
permalink: /corporations/
---

<div class="hero-banner" style="background-image: url('{{ "/assets/images/corporations-banner.png" | relative_url }}');">
  <div class="hero-content">
    <h1>Corporations</h1>
  </div>
</div>

<div class="grid-container">
{% for corporation in site.corporations %}
  <div class="card">
    <h3><a href="{{ corporation.url | relative_url }}">{{ corporation.title }}</a></h3>
    <p>{{ corporation.excerpt | strip_html | truncatewords: 20 }}</p>
  </div>
{% endfor %}
</div>
