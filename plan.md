# PTFM-Reflex - Supervisor Restrictions & Proyectos Enhancements

## Phase 1-14: Previous Phases ✅
- [x] All previous phases completed

## Phase 15: Supervisor Role Restrictions & Project Listing Tab ✅
- [x] Add "Listado de Proyectos" tab to Proyectos page showing: código, nombre, cliente, responsable (nombre), nro productos, % avance, estatus
- [x] Fix supervisor_id display in Gestión y Edición tab (Eliza showing no responsable despite having supervisor_id=3 in DB)
- [x] Restrict Supervisors: hide "Registrar Proyecto", "Matriz de Productos", "Gestión y Edición" tabs — only show "Listado de Proyectos"
- [x] Filter projects for Supervisors: only show projects where supervisor_id matches logged-in user's ID (across all modules: Proyectos, Seguimiento, Métricas, Incidencias)

## Phase 16: Product Editing in Matriz de Productos ✅
- [x] Add edit button (pencil icon) next to each product row in "Listado de Productos" table
- [x] Implement modal edit for product fields (ubicación, tipo, ctd, ml)
- [x] Save edits to Supabase and refresh the product list
