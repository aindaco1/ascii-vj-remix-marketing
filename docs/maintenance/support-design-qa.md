# Dust Wave Support design QA

Date: 2026-08-25

Historical review record; this result applies to the reviewed build and date.
See [Site Maintenance](README.md) for current support contracts and validation.

## Visual target

- Existing production design system: `https://asciivj.com/support/`
- Conceptual interaction reference: the supplied DCP-o-matic support screenshot
- Implementation: local English and Spanish support builds using the shared `dust_wave_support_v1` contract

The production page and implementation were captured in the in-app browser at the same 1024 × 900 viewport and reviewed together in one side-by-side comparison. The DCP-o-matic screenshot informed the clear maintainer introduction and the explicit one-time versus regular-support choice; its typography, color, and component styling were intentionally not copied.

## Checks

- The VCR display face, Inter body type, square borders, black panels, cyan/pink accents, header, search, and footer remain consistent with ASCIIVJ.
- The Dust Wave logo is a real existing brand asset and retains its intrinsic aspect ratio.
- Desktop layout was checked at 1024 × 900; mobile layout and both stacked payment cards were checked at 390 × 844.
- English and Spanish headings, checkout labels, attribution parameters, landmarks, and confirmation routes were checked.
- Checkout CTAs and external links remain first-party themed controls that continue to Stripe-hosted checkout in the same tab.
- No horizontal overflow, clipped controls, placeholder art, unreadable contrast, heading-name collisions, or accidental rounded styling was observed.

final result: passed
