# PTFM-Reflex - Módulo Incidencias Rebuild

## Phase 1-9: Anteriores ✅
- [x] All previous phases completed (Login, Seguimiento, Proyectos, Métricas, Gantt)

## Phase 10: Incidencias - State & Data Layer ✅
- [x] Rebuild IncidenciasState with full CRUD: load history from Supabase with project name join, register new incidencias with JSONB detalles
- [x] Implement temp matrix (tmp_piezas / tmp_materiales) for adding items before submitting
- [x] Implement pieza form fields: descripcion, cantidad, ubicacion, material, rotacion, veta, no_veta, tapacantos (F, P, D, I)
- [x] Implement materiales form fields: descripcion, cantidad, observaciones
- [x] Implement semáforo audit: toggle fecha_almacen/fecha_solicitante/fecha_teowin with auto-timestamp dd/mm/yyyy HH:MM, obs_gestion text field
- [x] Implement project search/filter for registro with proyecto_id association

## Phase 11: Incidencias - UI Registration & History ✅
- [x] Build registration form with project selector, tipo/categoria selectors, pieza form with dimensions and tapacantos matrix
- [x] Build materiales form with description/quantity/observations fields
- [x] Build temp matrix preview table with "Añadir a Matriz" and "Enviar Requerimiento" buttons
- [x] Build history accordion with semáforo icons (🟩/🟥) based on fecha fields, expandable detail view
- [x] Build audit section inside each accordion item: 3 checkboxes + obs_gestion input
