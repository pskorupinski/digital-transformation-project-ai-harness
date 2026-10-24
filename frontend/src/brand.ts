// Brand identity shown in the page header and browser tab.
// Values come from docs/01-brief.md §5, applied by /05-build-slice on the first slice with UI.
// Colours live in theme.css; this file holds only what CSS can't: text and the logo file.
export const BRAND = {
  name: 'Client',
  // Path under frontend/public/, e.g. '/logo.svg'; null = name with a generic logo mark
  logo: null as string | null,
}
