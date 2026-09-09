# White Shadow: organización de archivos

Alcance final reducido a reorganización, según la última indicación del usuario.
Se mantienen la lógica, los namespaces, los IDs y los registros de on_actions.
No se crean ni ejecutan tests. No se añaden eventos, cambios de ruta ni overrides de AGOT.

## Distribución

- `events/white_shadow/alex/segrellion_intro_events.txt`: introducción y campaña existentes, sin cambios de contenido.
- `events/white_shadow/tristan/`: eventos existentes de Sentinel y Vladwyn, sin cambios de contenido.
- `common/decisions/white_shadow/`: decisiones existentes de Vladwyn, sin cambios de contenido.
- `common/on_action/white_shadow/segrellion_white_shadow_on_actions.txt`: seis callbacks extraídos del archivo general, conservando sus nombres y contenido. Los registros de hooks permanecen en el archivo general.
- `common/bookmarks/bookmarks/segrellion_white_shadow.txt`: definición extraída de `iaf_bookmarks.txt`, con el mismo ID y personajes.
- `common/game_rules/segrellion_white_shadow_game_rules.txt`: borrador de regla que ya había añadido el usuario, separado del archivo de noticias.
- `localization/english/events/white_shadow/alex/`: los cuatro YAML anteriormente en `106_white_shadow`, sin cambios de contenido.
- `localization/english/events/white_shadow/tristan/`: los textos existentes de Sentinel y Vladwyn, sin cambios de contenido.
- `localization/english/interface/white_shadow/`: textos del borrador de regla del usuario.

Se eliminan los archivos de origen de los movimientos, sin duplicar definiciones.
Las carpetas de eventos y on_actions tienen precedentes de carga recursiva en AGOT.
La bookmark y la regla permanecen en sus directorios habituales de definiciones.

## Observaciones para un trabajo posterior

Se consultó la dependencia instalada AGOT 0.5.2.1 en Workshop (2962333032).
Su campaña usa `daemon_stepstones_first_war`, `daemon_stepstones_second_war`
y `triarchy_anti_daemon_war`; el ciclo `story_agot_scenario_trp` gestiona el cierre.
El dispatcher original inicializa el escenario en 8106.4.18, mientras White Shadow empieza el día 19.

La conexión completa de Alex con esa campaña y la aplicación de la regla de Tristan
quedan pendientes. La regla se conserva como estaba al comenzar esta tarea: este
trabajo de organización no sustituye la selección de ruta existente ni cambia el arranque.
