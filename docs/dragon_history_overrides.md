# Silverwing y Sheepstealer

## Causa y corrección

El antiguo `zz_segrellion_dragon_history_overrides.txt` volvía a definir los dos personajes, pero dejaba cargado `00_agot_char_dragons.txt` de AGOT. Sus muertes originales seguían presentes: Silverwing en 142 AC y Sheepstealer en 130 AC. Una bandera añadida en la misma fecha no borra una muerte.

El mod sustituye ahora `history/characters/00_agot_char_dragons.txt` por su misma ruta. Contiene las historias originales de los otros 69 dragones y las dos versiones de Segrellion. El archivo `zz_` duplicado se ha eliminado.

## Fechas conservadas del mod

- Silverwing: Alysanne como primera jinete; Rhaenys Segrellion desde 141; muerte el 14 de noviembre de 168, la fecha que comparte con Rhaenys en la guerra civil. Se eliminan del archivo cargado la vinculación con Ulf y la muerte de 142.
- Sheepstealer: Nettles como primera jinete; Alison desde 157; muerte a manos de Silverwing el 1 de marzo de 158, en Connington. Se elimina la desaparición mortal de 130.

La progresión mensual ya usa esas mismas fechas. En 144 y 157 ambos deben estar vivos; en 160 solo Silverwing; en 170 ambos han muerto según la historia del mod.

La corrección se aplica al crear una partida. Una muerte ya almacenada en una partida guardada no se revierte al modificar los archivos de historia. No se crean copias de los dragones ni se alteran guardados.

Al actualizar AGOT, hay que trasladar las dos historias modificadas a la nueva versión de su archivo. El submod debe cargarse después de AGOT y de cualquier otro mod que sustituya ese mismo archivo.
