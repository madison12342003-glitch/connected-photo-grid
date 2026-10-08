# Connected Photo Grid Agent Guide

This file describes how an AI agent should execute the Connected Photo Grid Skill.

The agent should treat SKILL.md as the primary contract and use the reference documents as decision support.

## 1. Receive the Task

Identify:
- how many photographs were provided
- whether the user wants exactly 3×3
- desired visual style
- desired color direction
- geographic or cultural context
- whether photographic realism must be preserved
- whether the user supplied a reference image
- whether the user wants selection, composition, editing, or all of them

If the user supplied a reference image, first determine what is important about the reference: composition, grid structure, cross-boundary continuity, color, texture, typography, editing style, or subject treatment.

Do not copy unrelated visual details from the reference.

## 2. Inventory All Photographs

Never assume that the first nine photographs are the final nine.

For each image, identify:
- subject
- dominant colors
- strongest lines
- strongest shapes
- foreground
- background
- horizon
- direction of movement
- visual weight
- negative space
- cultural or geographic elements
- possible incoming anchor
- possible outgoing anchor

Useful roles include anchor landscape, directional image, quiet image, focal subject, cultural detail, transition image, color bridge, and texture bridge.

## 3. Select Candidate Images

Remove obvious weak candidates such as technically poor photographs, duplicates, distracting accidental crops, images with little visual variety, and images that cannot connect naturally.

Create a candidate pool larger than nine when possible.

Do not optimize only for individual photographic quality. An excellent isolated photograph may be a poor grid tile if it has no useful connections.

## 4. Select the Final Nine

Choose nine photographs that collectively provide:
- strong individual quality
- subject diversity
- visual variety
- connection potential
- color coherence
- directional variety
- useful negative space
- narrative potential

Prefer a set where each image can perform a compositional role.

## 5. Build the Connection Graph

Represent the proposed layout as:

    A B C
    D E F
    G H I

Evaluate the twelve main neighboring relationships:
- A-B, B-C, D-E, E-F, G-H, H-I
- A-D, D-G, B-E, E-H, C-F, F-I

For each relationship, look for direction, shape, color, object, texture, spatial position, and narrative.

Read references/connection-rules.md when more detailed judgment is needed.

## 6. Find the Best Layout

Do not stop at the first plausible arrangement.

Consider several candidate layouts and evaluate connection quality, visual flow, visual weight, center quality, edge quality, color coherence, subject diversity, narrative coherence, visual conflicts, and repetition.

Read references/composition.md when evaluating the full grid.

The best layout is the one that makes the nine images function as one composition.

## 7. Optimize the Center

The center tile E touches four neighbors.

Prefer a center photograph with multiple compatible anchors, useful directional lines, flexible negative space, and balanced visual weight.

Do not automatically place the most dramatic image in the center.

## 8. Optimize Edges and Corners

Use corners for visual punctuation when appropriate.

Use edge tiles to control entry, exit, horizontal movement, vertical movement, and color transitions.

Avoid having too many strong lines point out of the composition.

## 9. Use Crop as a Compositional Tool

Before changing the selected images, consider whether a different crop improves the relationship.

Preserve connection anchors, important subjects, directional lines, and useful negative space.

Do not center every subject automatically.

## 10. Decide Whether Editing Is Necessary

Prefer solving problems through:
1. image selection
2. image order
3. crop
4. subtle tonal/color adjustments
5. minimal compositing
6. stronger image generation or transformation only when explicitly requested

Do not use AI generation to compensate for a weak layout.

## 11. Preserve Reality by Default

Unless the user explicitly asks for stylization:
- preserve photographic texture
- preserve plausible lighting
- preserve recognizable subjects
- preserve geographic authenticity
- avoid invented objects
- avoid generic AI scenery
- avoid excessive smoothing
- avoid plastic textures

If the project has a local cultural context, use only elements supported by the supplied photographs or clearly requested by the user.

## 12. Apply User-Specified Style

User instructions override the default visual treatment when they do not conflict with the core composition principle.

For example, a user may request a black and dark red palette, film-like texture, high contrast, muted colors, or editorial photography.

Apply the requested style globally where possible.

Do not destroy the underlying connection structure merely to achieve a stronger style.

## 13. Quality Gate

Before delivery, perform four checks.

### Grid Check
- exactly nine images?
- clear 3×3 structure?
- whole grid reads as one composition?

### Connection Check
- all twelve boundaries inspected?
- strongest connections intentional?
- weakest connections acceptable?
- no unnecessary artificial bridges?

### Photography Check
- subjects recognizable?
- photographic realism preserved?
- no obvious AI artifacts?
- no accidental distortions?

### Small-Screen Check

View the composition as a small thumbnail.

Ask: If the grid is seen for only a few seconds, does it read as one visual work?

If not, revise the layout.

## 14. Revision Order

When the result is weak, revise in this order:
1. change layout
2. replace one weak image
3. adjust crop
4. adjust color relationship
5. make subtle edits
6. regenerate or heavily transform only if requested

Do not immediately regenerate the entire composition.

## 15. User Communication

When the user asks for reasoning, explain the result in practical terms:
- why the nine images were selected
- what the main visual route is
- which boundaries have the strongest connections
- how the center functions
- how the color direction supports the grid

Do not expose hidden chain-of-thought.
Give concise, observable design reasons instead.

## 16. Completion Condition

The task is complete only when:
- the nine-image selection is defensible
- the arrangement has a clear visual logic
- cross-grid continuity is visible
- the composition remains photographically credible
- the requested style has been applied
- the final grid passes the whole-image and small-screen tests