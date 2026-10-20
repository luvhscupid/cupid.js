# Website project guidance

This is the starter website for work in this workspace. It uses React, TypeScript, Vite, Tailwind CSS, GSAP, Lenis, and the React Bits component registry.

## Working here

- Use `pnpm` from this directory. Keep dependencies local to this app.
- Use `useGSAP()` from `@gsap/react` for component animations and register GSAP plugins once.
- Reuse the app-level Lenis instance in `src/components/smooth-scroll-provider.tsx`; it already synchronizes with GSAP ScrollTrigger and skips smooth scrolling for reduced-motion users.
- Add React Bits components individually with `pnpm exec shadcn add @react-bits/<Component>-TS-TW`. The registry alias is configured in `components.json`; component source belongs in this repository and can be adapted to the design.
- Check required peer dependencies and follow each component's setup notes. Avoid adding components or packages without a need in the requested site.
- Preserve keyboard access, native anchors, reduced-motion preferences, and responsive behavior when adding motion or scroll effects.

## Commands

- `pnpm dev` — run the local development server.
- `pnpm run build` — type-check and build for production.
