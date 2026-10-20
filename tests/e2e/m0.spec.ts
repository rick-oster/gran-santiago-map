import { expect, test } from '@playwright/test'

test('M0 placeholder is intentionally not a fake map', async ({ page }) => {
  await page.goto('./')
  await expect(page.getByRole('heading', { name: 'Gran Santiago Map' })).toBeVisible()
  await expect(page.getByText('Sin geometría ficticia')).toBeVisible()
  await expect(page.getByTestId('build-marker')).toHaveText(/^M0-[A-Z0-9-]{3,64}$/)
  await expect(page.locator('.leaflet-container')).toHaveCount(0)
})

test('responsive screen has no horizontal overflow', async ({ page }) => {
  await page.goto('./')
  const hasHorizontalOverflow = await page.evaluate(() => document.documentElement.scrollWidth > window.innerWidth + 1)
  expect(hasHorizontalOverflow).toBe(false)
})
