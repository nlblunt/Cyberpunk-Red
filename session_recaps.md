---
layout: default
title: Session Recaps
permalink: /session_recaps/
---

<div class="hero-banner" style="background-image: url('{{ "/assets/images/recaps-banner.png" | relative_url }}');">
  <div class="hero-content">
    <h1>Session Recaps</h1>
  </div>
</div>

<div class="grid-container">
{% assign sorted_recaps = site.session_recaps | sort: 'real_date' | reverse %}
{% for recap in sorted_recaps %}
  <div class="card">
    <a href="{{ recap.url | relative_url }}" style="text-decoration: none; color: inherit;">
      <h4>{{ recap.title }}</h4>
      <p><strong>{{ recap.real_date | date: "%m/%d/%Y" }}</strong></p>
      <p><em>
        {% if recap.mission.size > 0 %}
          {{ recap.mission | join: ", " }}
        {% else %}
          {{ recap.mission }}
        {% endif %}
      </em></p>
      <div class="excerpt">
        <div class="excerpt-content">
          {% if recap.excerpt %}
            {{ recap.excerpt | strip_html }}
          {% else %}
            {{ recap.content | strip_html | truncatewords: 30 }}
          {% endif %}
        </div>
      </div>
    </a>
  </div>
{% endfor %}
</div>

<style>
.card {
    position: relative;
    overflow: hidden;
    min-height: 280px;
    display: flex;
    flex-direction: column;
}

.excerpt {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0, 0, 0, 0.95);
    backdrop-filter: blur(10px);
    display: flex;
    flex-direction: column;
    opacity: 0;
    transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    z-index: 10;
    pointer-events: none;
    border: 1px solid var(--accent-color, #00ff00);
    overflow-y: auto;
    box-sizing: border-box;
}

.excerpt-content {
    margin: auto;
    padding: 1.5rem;
    text-align: center;
    color: #00ff00; /* Cyberpunk Green */
    font-size: 0.95rem;
    line-height: 1.4;
}

/* Cyberpunk Scrollbar */
.excerpt::-webkit-scrollbar {
    width: 4px;
}
.excerpt::-webkit-scrollbar-track {
    background: rgba(0, 0, 0, 0.3);
}
.excerpt::-webkit-scrollbar-thumb {
    background: var(--accent-color, #00ff00);
    box-shadow: 0 0 5px var(--accent-color, #00ff00);
}

.card:hover .excerpt {
    opacity: 1;
    pointer-events: auto;
}
</style>
