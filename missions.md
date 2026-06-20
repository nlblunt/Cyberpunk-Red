---
layout: default
title: Missions
permalink: /missions/
---

<div class="hero-banner" style="background-image: url('{{ "/assets/images/missions-banner.png" | relative_url }}');">
  <div class="hero-content">
    <h1>Operational Dossier: Missions</h1>
  </div>
</div>

<div class="missions-section">
  <h2 class="section-title active-title">Active Operations</h2>
  <div class="grid-container">
    {% assign active_missions = site.missions | where: "mission_status", "In Progress" %}
    {% if active_missions.size > 0 %}
      {% for mission in active_missions %}
        <div class="card mission-card active-card">
          <a href="{{ mission.url | relative_url }}" style="text-decoration: none; color: inherit; display: flex; flex-direction: column; height: 100%;">
            <div class="mission-header">
              <span class="badge active-badge">Active</span>
              <span class="mission-type">{{ mission.mission_type }}</span>
            </div>
            <h4>{{ mission.title }}</h4>
            <div class="excerpt-content">
              {{ mission.content | strip_html | truncatewords: 30 }}
            </div>
          </a>
        </div>
      {% endfor %}
    {% else %}
      <p class="no-missions">No active operations at this time.</p>
    {% endif %}
  </div>
</div>

<div class="missions-section" style="margin-top: 40px;">
  <h2 class="section-title completed-title">Completed Database</h2>
  <div class="grid-container">
    {% assign finished_missions = site.missions | where: "mission_status", "Finished" %}
    {% if finished_missions.size > 0 %}
      {% for mission in finished_missions %}
        <div class="card mission-card completed-card">
          <a href="{{ mission.url | relative_url }}" style="text-decoration: none; color: inherit; display: flex; flex-direction: column; height: 100%;">
            <div class="mission-header">
              <span class="badge completed-badge">Completed</span>
              <span class="mission-type">{{ mission.mission_type }}</span>
            </div>
            <h4>{{ mission.title }}</h4>
            <div class="excerpt-content">
              {{ mission.content | strip_html | truncatewords: 30 }}
            </div>
          </a>
        </div>
      {% endfor %}
    {% else %}
      <p class="no-missions">No completed operations archived.</p>
    {% endif %}
  </div>
</div>

<style>
.section-title {
  font-family: 'Courier New', Courier, monospace;
  font-size: 1.5rem;
  margin-bottom: 20px;
  border-bottom: 2px solid #333;
  padding-bottom: 8px;
}

.active-title {
  color: #f1c40f;
  border-color: rgba(241, 196, 15, 0.3);
}

.completed-title {
  color: #2ecc71;
  border-color: rgba(46, 204, 113, 0.3);
}

.mission-card {
  position: relative;
  display: flex;
  flex-direction: column;
  padding: 1.5rem;
  border: 1px solid #333;
  background: #151515;
  transition: all 0.3s ease;
}

.active-card:hover {
  border-color: #f1c40f;
  box-shadow: 0 0 10px rgba(241, 196, 15, 0.2);
}

.completed-card:hover {
  border-color: #2ecc71;
  box-shadow: 0 0 10px rgba(46, 204, 113, 0.2);
}

.mission-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
}

.badge {
  font-size: 0.75rem;
  text-transform: uppercase;
  font-weight: bold;
  padding: 2px 6px;
  border-radius: 3px;
}

.active-badge {
  background: rgba(241, 196, 15, 0.2);
  color: #f1c40f;
  border: 1px solid #f1c40f;
}

.completed-badge {
  background: rgba(46, 204, 113, 0.2);
  color: #2ecc71;
  border: 1px solid #2ecc71;
}

.mission-type {
  font-size: 0.8rem;
  color: #777;
}

.excerpt-content {
  font-size: 0.9rem;
  color: #aaa;
  line-height: 1.4;
  margin-top: 10px;
}

.no-missions {
  color: #666;
  font-style: italic;
}
</style>
