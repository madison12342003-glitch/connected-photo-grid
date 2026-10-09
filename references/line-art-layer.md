# Line Art Layer

## Purpose
Line art creates a quiet bridge between photographs and the graphic background. It should support the images rather than compete with them.

## Style
- Default stroke: fine black or charcoal.
- Accent stroke: muted red, used sparingly.
- Keep line weight consistent across assets.
- Prefer simple contour drawings, botanical studies, mountain contours, road traces, topographic lines, or textile-inspired geometry when relevant.
- Avoid excessive detail that disappears on a phone screen.

## Placement
- Place line art in negative space where it remains legible.
- Allow a line to approach or cross a tile boundary only when it is deliberately mapped across the full 3×3 canvas.
- Do not run lines through a key subject's face, sign, temple detail, or other important content.
- Keep a safe margin from tile edges unless cross-grid continuation is intentional.

## Continuity
Define cross-grid paths in global-canvas coordinates before splitting into nine tiles. Store each path's start point, end point, stroke, color, and intended tiles. Check alignment after export; separate tile exports can introduce small shifts.

## Quality check
At phone size, the line art should remain clean, not resemble compression noise, and not create accidental tangencies with photo edges.
