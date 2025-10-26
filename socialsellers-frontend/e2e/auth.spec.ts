import { test, expect } from '@playwright/test';

test.describe('Authentication Flow', () => {
  test('should display login page', async ({ page }) => {
    await page.goto('/login');

    await expect(page.locator('text=Social Sellers')).toBeVisible();
    await expect(page.locator('input[type="email"]')).toBeVisible();
    await expect(page.locator('input[type="password"]')).toBeVisible();
    await expect(page.locator('button[type="submit"]')).toBeVisible();
  });

  test('should show error on invalid credentials', async ({ page }) => {
    await page.goto('/login');

    await page.fill('input[type="email"]', 'invalid@test.com');
    await page.fill('input[type="password"]', 'wrongpassword');
    await page.click('button[type="submit"]');

    // Esperar el mensaje de error (el backend debe estar corriendo para este test)
    await expect(page.locator('text=/error/i')).toBeVisible({ timeout: 5000 });
  });

  test('should redirect to dashboard after login', async ({ page }) => {
    // Nota: Este test requiere que el backend esté corriendo
    await page.goto('/login');

    // Mock del localStorage para simular sesión
    await page.evaluate(() => {
      localStorage.setItem('access_token', 'fake-token-for-test');
      localStorage.setItem('usuario', JSON.stringify({
        id: 1,
        nombre: 'Test User',
        email: 'test@test.com',
        rol: 'admin',
        activo: true
      }));
    });

    await page.goto('/dashboard');

    // Verificar que estamos en el dashboard
    await expect(page.locator('text=/bienvenido/i')).toBeVisible({ timeout: 5000 });
  });
});
