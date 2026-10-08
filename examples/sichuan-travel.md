# Western Sichuan Travel Example

This example shows how Connected Photo Grid can be applied to a travel photography series from Western Sichuan (川西).

## Goal

Turn a large collection of Western Sichuan travel photographs into one coherent 3×3 photographic composition.

The objective is not simply to select nine beautiful photographs. The objective is to make the nine photographs behave like one visual work.

## Input

Example input:
- a collection of travel photographs from Western Sichuan
- landscapes, roads, rivers, mountains, grassland, architecture, cultural details, animals, flowers, and people
- multiple photographs with different compositions and lighting

The actual source photographs do not need to be included in the public repository.

## Visual Direction

A possible art direction for this case study:
- photographic realism
- black and dark red as the dominant global direction
- preserve selected original colors such as yellow, green, blue, and white
- strong Tibetan plateau / Western Sichuan identity
- restrained editing
- no generic surreal-pop treatment unless explicitly requested

The color direction is an example, not a mandatory requirement of the core Skill.

## Candidate Visual Anchors

Potential authentic visual anchors include:
- snow mountains
- mountain ridges
- rivers
- waterfalls
- grassland
- roads
- prayer flags
- white stupas
- temples
- yaks
- Gesang flowers
- clouds
- rock formations

These are examples of possible anchors. The agent should only use elements actually present in the supplied photographs or explicitly requested by the user.

## Example Connection Chain

A possible visual chain could be:

    mountain ridge
          ↓
      prayer flag
          ↓
         river
          ↓
      waterfall
          ↓
          road
          ↓
       grassland

This is an illustration of the reasoning pattern, not a fixed layout.

## Example 3×3 Planning

Before producing the final grid, the agent should create a planning map:

    A  B  C
    D  E  F
    G  H  I

For each tile, record:
- primary subject
- dominant color
- strongest directional line
- incoming anchor
- outgoing anchor
- visual weight
- negative space

Then evaluate all twelve neighboring boundaries.

## Example

A hypothetical planning table:

| Tile | Role | Possible anchor |
| --- | --- | --- |
| A | landscape anchor | mountain ridge |
| B | transition | prayer flags |
| C | color punctuation | red architectural detail |
| D | directional image | road |
| E | central connector | river |
| F | movement | waterfall |
| G | quiet transition | grassland |
| H | local detail | yak / flower |
| I | closing image | temple / mountain |

This table is only an example. The actual roles must be determined from the supplied photographs.

## What the Agent Should Avoid

Do not automatically:
- select the first nine photographs
- put the most beautiful image in the center
- make every tile equally dramatic
- force every boundary to be visually obvious
- add stereotypical Tibetan symbols that are not present
- turn the project into a generic surreal collage
- replace photographic reality with synthetic scenery
- use decorative elements to hide a weak layout

## Quality Goal

The final result should satisfy this test:

> When the grid is viewed from a distance or at small size, it should feel like one photographic composition. When viewed tile by tile, each photograph should still retain its own identity.

That dual requirement is the central challenge of the example.

## Why This Example Matters

This case demonstrates that Connected Photo Grid is not tied to a single location or visual style.

The same workflow can later be applied to:
- Tibet
- Xinjiang
- Japan
- Iceland
- urban photography
- architecture
- portrait series
- editorial photo stories

The location and style change. The underlying connection and composition logic remains the same.