import { describe, expect, it } from 'vitest'
import { BUILD_MARKER, SPEC_VERSION } from '../../src/app/build-label'

describe('M0 starter contract', () => {
  it('exposes a nonempty stable M0 deployment marker', () => {
    expect(BUILD_MARKER).toMatch(/^M0-[A-Z0-9-]{3,64}$/)
  })
  it('preserves the frozen V1 specification version', () => {
    expect(SPEC_VERSION).toBe('1.0')
  })
})
