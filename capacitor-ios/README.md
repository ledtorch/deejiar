# Deejiar App
This is Deejiar's user-facing front-end, developed using Vue 3.4 and Vite 5. It serves as the primary interface for users to interact with the map, accessible at deejiar.com.

## 🛠 Prerequisites
- Node.js
- Yarn
- Vite
- Vue3
- Mapbox token <a href="https://docs.mapbox.com/help/getting-started/access-tokens/">Tutorial</a>

```zsh
openssl req -x509 -newkey rsa:2048 -keyout localhost.key -out localhost.crt -days 365 -nodes
```

```zsh
yarn
```

```zsh
yarn dev
```

## Main Components
- Map.vue
  - BottomSheet.vue
- Details.vue
- Account.vue

### Map.vue
This component acts as the core of the application, enabling the main functionalities. It handles UI with the map, fetching stores data from a JSON file and passing this data to **BottomSheet**, which then displays the information about the selected store.

### BottomSheet.vue
A child component of **Map**, **BottomSheet** plays a role in providing users with a quick overview of store information. Dragging this component upwards leads users to a detailed page for the store, rendered by **Details**.

### Details.vue
This component fetches store data directly from a JSON file by decoding the URL. It ensures that store pages are directly accessible, maintaining functionality even when users do not navigate through clicking on the map but rather enter a URL or directly access a store's detail page.

### Account.vue
This page allows users to manage their settings and provides contact information for the author, along with links to related social media profiles.

### SCSS Standard
1. Positioning
2. Layout & Box Model
3. Typography
4. Visual & Colors
5. Interactions
6. Animations & Transitions
7. Other/Misc

.comprehensive-example {
  /* 1. POSITIONING */
  position: absolute;
  top: 0;
  right: 0;
  bottom: 0;
  left: 0;
  z-index: 1000;
  clip: rect(0, 0, 0, 0);
  clip-path: circle(50%);

  /* 2. LAYOUT & BOX MODEL */
  // Display & Flow
  display: flex;
  visibility: visible;
  overflow: hidden;
  overflow-x: hidden;
  overflow-y: auto;
  overflow-wrap: break-word;
  overflow-anchor: none;
  
  // Flexbox
  flex-direction: row;
  flex-wrap: nowrap;
  flex-flow: row nowrap;
  flex: 1 1 auto;
  flex-grow: 1;
  flex-shrink: 1;
  flex-basis: auto;
  order: 0;
  align-content: stretch;
  align-items: center;
  align-self: auto;
  justify-content: flex-start;
  justify-items: start;
  justify-self: auto;
  place-content: center;
  place-items: center;
  place-self: auto;
  gap: 16px;
  row-gap: 16px;
  column-gap: 16px;
  
  // Grid
  grid: none;
  grid-area: auto;
  grid-template: none;
  grid-template-areas: none;
  grid-template-rows: none;
  grid-template-columns: 1fr 2fr;
  grid-auto-rows: auto;
  grid-auto-columns: auto;
  grid-auto-flow: row;
  grid-row: auto;
  grid-row-start: auto;
  grid-row-end: auto;
  grid-column: auto;
  grid-column-start: auto;
  grid-column-end: auto;
  
  // Float & Clear
  float: none;
  clear: both;
  
  // Dimensions
  width: 100%;
  height: 100vh;
  min-width: 320px;
  min-height: 200px;
  max-width: 1200px;
  max-height: 800px;
  box-sizing: border-box;
  
  // Spacing
  margin: 16px;
  margin-top: 16px;
  margin-right: 16px;
  margin-bottom: 16px;
  margin-left: 16px;
  padding: 12px;
  padding-top: 12px;
  padding-right: 12px;
  padding-bottom: 12px;
  padding-left: 12px;
  
  // Borders
  border: 1px solid #ccc;
  border-top: 1px solid #ccc;
  border-right: 1px solid #ccc;
  border-bottom: 1px solid #ccc;
  border-left: 1px solid #ccc;
  border-width: 1px;
  border-style: solid;
  border-color: #ccc;
  border-radius: 8px;
  border-top-left-radius: 8px;
  border-top-right-radius: 8px;
  border-bottom-right-radius: 8px;
  border-bottom-left-radius: 8px;
  border-image: none;
  border-image-source: none;
  border-image-slice: 100%;
  border-image-width: 1;
  border-image-outset: 0;
  border-image-repeat: stretch;
  border-collapse: separate;
  border-spacing: 0;
  
  // Tables
  table-layout: auto;
  caption-side: top;
  empty-cells: show;
  
  // Columns
  columns: auto;
  column-count: auto;
  column-width: auto;
  column-gap: normal;
  column-rule: none;
  column-rule-width: medium;
  column-rule-style: none;
  column-rule-color: currentColor;
  column-span: none;
  column-fill: balance;
  break-before: auto;
  break-after: auto;
  break-inside: auto;

  /* 3. TYPOGRAPHY */
  font: normal normal 400 16px/1.5 'Geist', sans-serif;
  font-family: 'Geist', system-ui, sans-serif;
  font-size: 16px;
  font-weight: 400;
  font-style: normal;
  font-variant: normal;
  font-variant-caps: normal;
  font-variant-numeric: normal;
  font-variant-alternates: normal;
  font-variant-ligatures: normal;
  font-variant-east-asian: normal;
  font-variant-position: normal;
  font-stretch: normal;
  font-size-adjust: none;
  font-synthesis: weight style;
  font-kerning: auto;
  font-optical-sizing: auto;
  font-feature-settings: normal;
  font-variation-settings: normal;
  line-height: 1.5;
  letter-spacing: normal;
  word-spacing: normal;
  text-align: left;
  text-align-last: auto;
  text-decoration: none;
  text-decoration-line: none;
  text-decoration-color: currentColor;
  text-decoration-style: solid;
  text-decoration-thickness: auto;
  text-underline-offset: auto;
  text-underline-position: auto;
  text-transform: none;
  text-indent: 0;
  text-justify: auto;
  text-overflow: clip;
  text-shadow: none;
  text-emphasis: none;
  text-emphasis-style: none;
  text-emphasis-color: currentColor;
  text-emphasis-position: over right;
  white-space: normal;
  white-space-collapse: collapse;
  text-wrap: wrap;
  word-wrap: normal;
  word-break: normal;
  hyphens: manual;
  hyphenate-character: auto;
  tab-size: 8;
  direction: ltr;
  unicode-bidi: normal;
  writing-mode: horizontal-tb;
  text-orientation: mixed;
  text-combine-upright: none;

  /* 4. VISUAL & COLORS */
  // Colors
  color: #333;
  opacity: 1;
  
  // Backgrounds
  background: transparent;
  background-color: transparent;
  background-image: none;
  background-position: 0% 0%;
  background-position-x: 0%;
  background-position-y: 0%;
  background-size: auto;
  background-repeat: repeat;
  background-origin: padding-box;
  background-clip: border-box;
  background-attachment: scroll;
  background-blend-mode: normal;
  
  // Shadows & Effects
  box-shadow: none;
  text-shadow: none;
  filter: none;
  backdrop-filter: none;
  
  // Masks & Clipping
  mask: none;
  mask-image: none;
  mask-mode: match-source;
  mask-repeat: repeat;
  mask-position: center;
  mask-clip: border-box;
  mask-origin: border-box;
  mask-size: auto;
  mask-composite: add;
  
  // Lists
  list-style: none;
  list-style-type: disc;
  list-style-position: outside;
  list-style-image: none;
  
  // Generated Content
  content: normal;
  quotes: none;
  counter-reset: none;
  counter-increment: none;
  counter-set: none;

  /* 5. INTERACTIONS */
  cursor: pointer;
  pointer-events: auto;
  user-select: none;
  user-drag: auto;
  user-zoom: zoom;
  touch-action: manipulation;
  scroll-behavior: smooth;
  scroll-snap-type: none;
  scroll-snap-align: none;
  scroll-snap-stop: normal;
  scroll-margin: 0;
  scroll-margin-top: 0;
  scroll-margin-right: 0;
  scroll-margin-bottom: 0;
  scroll-margin-left: 0;
  scroll-padding: auto;
  scroll-padding-top: auto;
  scroll-padding-right: auto;
  scroll-padding-bottom: auto;
  scroll-padding-left: auto;
  scrollbar-width: auto;
  scrollbar-color: auto;
  scrollbar-gutter: auto;
  overscroll-behavior: auto;
  overscroll-behavior-x: auto;
  overscroll-behavior-y: auto;

  /* 6. ANIMATIONS & TRANSITIONS */
  transition: all 0.3s ease;
  transition-property: all;
  transition-duration: 0.3s;
  transition-timing-function: ease;
  transition-delay: 0s;
  
  transform: none;
  transform-origin: 50% 50% 0;
  transform-style: flat;
  perspective: none;
  perspective-origin: 50% 50%;
  backface-visibility: visible;
  
  animation: none;
  animation-name: none;
  animation-duration: 0s;
  animation-timing-function: ease;
  animation-delay: 0s;
  animation-iteration-count: 1;
  animation-direction: normal;
  animation-fill-mode: none;
  animation-play-state: running;
  animation-timeline: auto;
  animation-range: normal;
  
  will-change: auto;
  contain: none;
  contain-intrinsic-size: none;
  contain-intrinsic-width: none;
  contain-intrinsic-height: none;

  /* 7. OTHER/MISC */
  all: unset;
  appearance: none;
  aspect-ratio: auto;
  resize: none;
  outline: none;
  outline-width: medium;
  outline-style: none;
  outline-color: invert;
  outline-offset: 0;
  
  // Accessibility
  speak: auto;
  speak-as: auto;
  
  // Page/Print
  page-break-before: auto;
  page-break-after: auto;
  page-break-inside: auto;
  page: auto;
  orphans: 2;
  widows: 2;
  
  // Ruby (East Asian typography)
  ruby-align: space-around;
  ruby-merge: separate;
  ruby-position: over;
  
  // Shapes
  shape-outside: none;
  shape-margin: 0;
  shape-image-threshold: 0;
  
  // Object fitting (for replaced elements)
  object-fit: fill;
  object-position: 50% 50%;
  
  // Isolation
  isolation: auto;
  mix-blend-mode: normal;
  
  // Image rendering
  image-rendering: auto;
  image-orientation: from-image;
  
  // Input specific
  ime-mode: auto;
  text-security: none;
}