# PTFM-Reflex - Fix Seguimiento Table Rendering

## Phase 1-12: Previous Phases ✅
- [x] All previous phases completed

## Phase 13: Fix Seguimiento Table Stability ✅
- [x] Remove bulk-mark checkbox buttons from table headers (the ones that trigger `bulk_mark_hito`) to eliminate insertBefore DOM conflicts
- [x] Ensure all filtering (group_by, sin_hito_X, sin_avance, primary_filter, refinement_filter) happens entirely in the backend State computed var, not in frontend rendering
- [x] Simplify the table row rendering to use flat, predictable structure without nested rx.cond conflicts
- [x] Verify the milestone_cell component uses stable keys and minimal conditional DOM changes
