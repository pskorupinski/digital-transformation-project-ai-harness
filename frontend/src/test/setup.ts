import '@testing-library/jest-dom/vitest'
import { cleanup } from '@testing-library/react'
import { afterEach } from 'vitest'

// Unmount after every test: without vitest globals, Testing Library doesn't do it automatically,
// and a second render in the same file would see the previous page too.
afterEach(cleanup)
