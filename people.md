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

<div id="people-list">
  <div class="controls" style="margin: 20px 0; display: flex; gap: 10px; align-items: center; flex-wrap: wrap;">
    <input class="search" placeholder="Search people..." style="padding: 10px; font-size: 16px; border: 1px solid #444; background: #222; color: white; border-radius: 4px; flex-grow: 1;">
    <button class="sort" data-sort="name" style="padding: 10px 20px; cursor: pointer; background: #b00; color: white; border: none; font-family: 'Oxanium', sans-serif;">Sort by Name</button>
    <button class="sort" data-sort="title" style="padding: 10px 20px; cursor: pointer; background: #333; color: white; border: none; font-family: 'Oxanium', sans-serif;">Sort by Title</button>
    <button class="sort" data-sort="corporation" style="padding: 10px 20px; cursor: pointer; background: #333; color: white; border: none; font-family: 'Oxanium', sans-serif;">Sort by Corp</button>
    <button class="sort" data-sort="contact-sort" style="padding: 10px 20px; cursor: pointer; background: #333; color: white; border: none; font-family: 'Oxanium', sans-serif;">Sort by Contact</button>
  </div>

  <div class="grid-container list">
  {% for person in site.people %}
    {% unless person.known == false %}
    <div class="card" style="position: relative;">
      <a href="{{ person.url | relative_url }}" style="text-decoration: none; color: inherit;">
        <!-- Sort helper -->
        <span class="contact-sort" style="display:none;">{% if person.contact == true %}1{% else %}0{% endif %}</span>

        <div style="display: flex; justify-content: space-between; align-items: start;">
          {% if person.name %}
            <h4 class="name" style="margin-top: 0;">{{ person.name }}</h4>
          {% else %}
             <h4 class="title" style="margin-top: 0;">{{ person.title }}</h4>
             <span class="name" style="display:none;">{{ person.title }}</span>
          {% endif %}
          
          {% if person.contact == true %}
            <span style="background: #efce3b; color: #000; padding: 2px 6px; font-size: 0.8em; font-weight: bold; border-radius: 2px;">CONTACT</span>
          {% endif %}
        </div>

        {% if person.name %}
          <p><strong class="title">{{ person.title }}</strong></p>
          {% if person.corporation %}
          <p><em class="corporation">{{ person.corporation }}</em></p>
          {% else %}
           <p style="display:none;"><em class="corporation"></em></p>
          {% endif %}

          {% if person.contact == true %}
          <div class="stats" style="margin-top: 10px; border-top: 1px solid #333; padding-top: 8px;">
            <div class="stat-row" style="margin-bottom: 5px;">
              <div style="display: flex; justify-content: space-between; font-size: 0.8em; margin-bottom: 2px;">
                <span>Loyalty</span>
                <span>{{ person.loyalty }}/10</span>
              </div>
              <div style="background: #333; height: 6px; border-radius: 3px; overflow: hidden;">
                <div style="background: #e74c3c; height: 100%; width: {{ person.loyalty | times: 10 }}%;"></div>
              </div>
            </div>
            <div class="stat-row">
              <div style="display: flex; justify-content: space-between; font-size: 0.8em; margin-bottom: 2px;">
                <span>Connection</span>
                <span>{{ person.connection }}/10</span>
              </div>
              <div style="background: #333; height: 6px; border-radius: 3px; overflow: hidden;">
                <div style="background: #3498db; height: 100%; width: {{ person.connection | times: 10 }}%;"></div>
              </div>
            </div>
          </div>
          {% endif %}

        {% else %}
          {% if person.title %}
           <!-- If no name, title is header, so maybe don't show title again? logic in original was different -->
           <!-- Original logic: if person.name ... else ... h4 title ... -->
             <!-- If name is missing, we used title as header. -->
           <p class="excerpt">{{ person.excerpt | strip_html | truncatewords: 20 }}</p>
           {% else %}
              <p class="excerpt">{{ person.excerpt | strip_html | truncatewords: 20 }}</p>
           {% endif %}
        {% endif %}
      </a>
    </div>
    {% endunless %}
  {% endfor %}
  </div>
</div>

<script src="https://cdnjs.cloudflare.com/ajax/libs/list.js/2.3.1/list.min.js"></script>
<script>
  var options = {
    valueNames: [ 'name', 'title', 'corporation', 'excerpt', 'contact-sort' ]
  };
  var userList = new List('people-list', options);
</script>
